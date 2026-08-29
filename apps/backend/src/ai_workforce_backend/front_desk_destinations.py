"""Test-only tenant-admin lifecycle API for Front Desk destinations."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from datetime import UTC, datetime, timedelta
from typing import Protocol, cast

from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class DestinationStore(Protocol):
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: ...

    def list(self, scope: TenantScope, kind: str, limit: int = 25) -> list[VersionedRecord]: ...

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None: ...

    def compare_and_swap_versioned(
        self, scope: TenantScope, kind: str, record: VersionedRecord, expected_version: int
    ) -> bool: ...

    def activate_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool: ...

    def suspend_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool: ...

    def withdraw_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool: ...


class FrontDeskDestinationsApi:
    """Manage synthetic destination configuration with trusted tenant scope."""

    path = "/v1/front-desk/destinations"
    route_ref = "platform.front-desk-destination-configuration.v1"
    required_permission = "platform.front-desk.configure"
    _allowed_pairs = {
        ("support", "support_worker"),
        ("human_support", "human_support_route"),
        ("human_sales", "human_sales_route"),
    }

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: DestinationStore,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
        destination_factory: Callable[[], str] = lambda: f"dst_{uuid.uuid4().hex}",
        now_factory: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._store = store
        self._correlation_factory = correlation_factory
        self._destination_factory = destination_factory
        self._now_factory = now_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            scope = TenantScope(membership.tenant_ref, identity.environment_ref, correlation_ref)
            status, body = self._dispatch(environ, scope, correlation_ref)
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except AuthorizationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        except (TypeError, ValueError) as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "400 Bad Request", headers, {"error": "invalid_request"})
        self._audit_sink.record(
            AuditEvent("allowed", "configuration_changed", correlation_ref, self.route_ref, identity.principal_ref, membership.tenant_ref)
        )
        return self._respond(start_response, status, headers, body)

    def _dispatch(
        self, environ: Mapping[str, object], scope: TenantScope, correlation_ref: str
    ) -> tuple[str, dict[str, object]]:
        method = environ.get("REQUEST_METHOD")
        path = environ.get("PATH_INFO")
        if method == "GET" and path == self.path:
            items = [
                self._public(record.payload)
                for record in self._store.list(scope, "routing", limit=100)
                if record.payload.get("record_type") == "front_desk_destination"
            ]
            return "200 OK", {"destinations": items, "correlation_ref": correlation_ref}
        if method == "POST" and path == self.path:
            request = self._create_request(environ)
            destination_ref = self._destination_factory()
            payload: dict[str, object] = {
                "record_type": "front_desk_destination",
                "destination_ref": destination_ref,
                "route_purpose": request["route_purpose"],
                "destination_type": request["destination_type"],
                "channel_scope": request["channel_scope"],
                "lifecycle_state": "draft",
                "configuration_version": 1,
                "health_state": "unknown",
                "health_expires_at": None,
            }
            self._store.save(scope, "routing", VersionedRecord(destination_ref, "v1", payload))
            return "201 Created", {**self._public(payload), "correlation_ref": correlation_ref}
        if method == "POST" and isinstance(path, str) and path.startswith(f"{self.path}/"):
            suffix = path.removeprefix(f"{self.path}/")
            destination_ref, separator, operation = suffix.partition("/")
            if not separator or operation not in {"validate", "activate", "renew", "suspend", "withdraw"}:
                return "404 Not Found", {"error": "not_found"}
            record = self._store.get(scope, "routing", destination_ref)
            if record is None or record.payload.get("record_type") != "front_desk_destination":
                return "404 Not Found", {"error": "not_found"}
            payload = dict(record.payload)
            expected_version = self._expected_version(environ)
            if payload.get("configuration_version") != expected_version:
                return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
            previous = payload.get("lifecycle_state")
            if operation == "validate":
                if previous != "draft" or not self._valid_destination(payload):
                    return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
                payload["lifecycle_state"] = "validated"
                payload["health_state"] = "healthy"
                payload["health_expires_at"] = (
                    self._now_factory() + timedelta(minutes=5)
                ).isoformat()
            elif operation == "activate":
                if (
                    previous != "validated"
                    or not self._healthy_and_fresh(payload)
                ):
                    return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
                payload["lifecycle_state"] = "active"
            elif operation == "renew":
                if previous != "active":
                    return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
                payload["health_state"] = "healthy"
                payload["health_expires_at"] = (
                    self._now_factory() + timedelta(minutes=5)
                ).isoformat()
            elif operation == "suspend":
                if previous != "active":
                    return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
                payload["lifecycle_state"] = "suspended"
            elif previous == "active":
                payload["lifecycle_state"] = "withdrawn"
            elif previous in {"draft", "validated", "suspended"}:
                payload["lifecycle_state"] = "withdrawn"
            else:
                return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
            payload["configuration_version"] = expected_version + 1
            next_record = VersionedRecord(destination_ref, "v1", payload)
            changed = (
                self._store.activate_front_desk_destination(scope, next_record, expected_version)
                if operation == "activate"
                else self._store.suspend_front_desk_destination(scope, next_record, expected_version)
                if operation == "suspend"
                else self._store.withdraw_front_desk_destination(scope, next_record, expected_version)
                if operation == "withdraw" and previous == "active"
                else self._store.compare_and_swap_versioned(scope, "routing", next_record, expected_version)
            )
            if not changed:
                return "409 Conflict", {"error": "state_conflict", "correlation_ref": correlation_ref}
            return "200 OK", {**self._public(payload), "correlation_ref": correlation_ref}
        return "404 Not Found", {"error": "not_found"}

    def _create_request(self, environ: Mapping[str, object]) -> dict[str, object]:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = cast(object, environ.get("wsgi.input"))
        if not hasattr(raw, "read") or content_length < 2:
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"route_purpose", "destination_type", "channel_scope"}:
            raise ValueError("invalid_request")
        purpose, destination_type, channels = (
            payload["route_purpose"], payload["destination_type"], payload["channel_scope"]
        )
        if (
            not isinstance(purpose, str)
            or not isinstance(destination_type, str)
            or (purpose, destination_type) not in self._allowed_pairs
            or not isinstance(channels, list)
            or channels != ["web_chat"]
        ):
            raise ValueError("invalid_request")
        return cast(dict[str, object], payload)

    @staticmethod
    def _expected_version(environ: Mapping[str, object]) -> int:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = cast(object, environ.get("wsgi.input"))
        if not hasattr(raw, "read") or content_length < 2:
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"expected_configuration_version"}:
            raise ValueError("invalid_request")
        expected_version = payload["expected_configuration_version"]
        if not isinstance(expected_version, int) or expected_version < 1:
            raise ValueError("invalid_request")
        return expected_version

    def _valid_destination(self, payload: Mapping[str, object]) -> bool:
        return (
            (payload.get("route_purpose"), payload.get("destination_type")) in self._allowed_pairs
            and payload.get("channel_scope") == ["web_chat"]
            and payload.get("configuration_version") == 1
        )

    def _healthy_and_fresh(self, payload: Mapping[str, object]) -> bool:
        expiry = payload.get("health_expires_at")
        if payload.get("health_state") != "healthy" or not isinstance(expiry, str):
            return False
        try:
            parsed_expiry = datetime.fromisoformat(expiry)
            return parsed_expiry.tzinfo is not None and parsed_expiry > self._now_factory()
        except ValueError:
            return False

    @staticmethod
    def _public(payload: Mapping[str, object]) -> dict[str, object]:
        purpose = payload["route_purpose"]
        return {
            "destination_ref": payload["destination_ref"],
            "route_purpose": purpose,
            "destination_type": payload["destination_type"],
            "channel_scope": payload["channel_scope"],
            "public_display": {
                "support": "Support",
                "human_support": "Human support",
                "human_sales": "Human Sales",
            }[cast(str, purpose)],
            "lifecycle_state": payload["lifecycle_state"],
            "configuration_version": payload["configuration_version"],
            "health_state": payload["health_state"],
            "health_expires_at": payload["health_expires_at"],
        }

    @staticmethod
    def _respond(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: object,
    ) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

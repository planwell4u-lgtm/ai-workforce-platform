"""Protected support-ticket flow spanning identity, PostgreSQL, and Jira."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from typing import Protocol, cast

from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord
from ai_workforce_integration.support_ticket import JiraSupportTicketAction, SupportTicketRequest

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class TicketStore(Protocol):
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: ...

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None: ...


class SupportTicketApi:
    route_ref = "integration.support-ticket.create.v1"
    required_permission = "integration.support-ticket.create"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: TicketStore,
        action: JiraSupportTicketAction,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._store = store
        self._action = action
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if (
            environ.get("REQUEST_METHOD") != "POST"
            or environ.get("PATH_INFO") != "/v1/support-tickets"
        ):
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if self.required_permission not in membership.permissions:
                raise AuthorizationError("insufficient_permission")
            if self.required_permission not in identity.granted_permissions:
                raise AuthorizationError("token_missing_permission")
            request = self._parse_request(environ, membership.tenant_ref)
        except AuthenticationError as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

        scope = TenantScope(membership.tenant_ref, identity.environment_ref, correlation_ref)
        existing = self._store.get(scope, "action", request.idempotency_ref)
        if existing is not None:
            return self._respond(start_response, "200 OK", headers, existing.payload)
        self._store.save(
            scope, "action", VersionedRecord(request.idempotency_ref, "v1", {"outcome": "pending"})
        )
        result = self._action.request(request, membership.permissions)
        body: dict[str, object] = {
            "outcome": result.outcome,
            "idempotency_ref": result.idempotency_ref,
            "ticket_ref": result.ticket_ref,
            "correlation_ref": correlation_ref,
        }
        self._store.save(scope, "action", VersionedRecord(request.idempotency_ref, "v1", body))
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                result.outcome,
                correlation_ref,
                self.route_ref,
                identity.principal_ref,
                membership.tenant_ref,
            )
        )
        return self._respond(start_response, "201 Created", headers, body)

    @staticmethod
    def _parse_request(environ: Mapping[str, object], tenant_ref: str) -> SupportTicketRequest:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = cast(object, environ.get("wsgi.input"))
        if not hasattr(raw, "read"):
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("invalid_request")
        values = tuple(
            payload.get(name) for name in ("conversation_ref", "idempotency_ref", "summary")
        )
        if not all(isinstance(value, str) and value for value in values):
            raise ValueError("invalid_request")
        return SupportTicketRequest(
            tenant_ref, cast(str, values[0]), cast(str, values[1]), cast(str, values[2])
        )

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

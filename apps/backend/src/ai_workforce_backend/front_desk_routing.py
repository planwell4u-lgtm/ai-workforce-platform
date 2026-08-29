"""Test-only, tenant-scoped Front Desk route-request API.

This boundary records a routing outcome only.  It cannot transfer a call,
assign a person, notify a provider, or create a ticket.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, Protocol, cast

from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)

RoutePurpose = Literal["support", "human_support", "human_sales"]


class RoutingStore(Protocol):
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: ...

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None: ...

    def list(self, scope: TenantScope, kind: str, limit: int = 25) -> list[VersionedRecord]: ...


class RouteDestinationRegistry(Protocol):
    def destination_for(
        self, scope: TenantScope, route_purpose: RoutePurpose, expected_destination_ref: str | None = None
    ) -> "RouteDestination | None": ...


@dataclass(frozen=True)
class RouteDestination:
    destination_ref: str


class ActiveDestinationRegistry:
    """Resolve only an active, tenant-scoped synthetic web-chat destination."""

    def __init__(
        self, store: RoutingStore, now_factory: Callable[[], datetime] = lambda: datetime.now(UTC)
    ) -> None:
        self._store = store
        self._now_factory = now_factory

    def destination_for(
        self, scope: TenantScope, route_purpose: RoutePurpose, expected_destination_ref: str | None = None
    ) -> RouteDestination | None:
        expected_type = {
            "support": "support_worker",
            "human_support": "human_support_route",
            "human_sales": "human_sales_route",
        }[route_purpose]
        matches = [
            record
            for record in self._store.list(scope, "routing", limit=100)
            if record.payload.get("record_type") == "front_desk_destination"
            and record.payload.get("route_purpose") == route_purpose
            and record.payload.get("destination_type") == expected_type
            and record.payload.get("lifecycle_state") == "active"
            and record.payload.get("channel_scope") == ["web_chat"]
            and self._healthy_and_fresh(record.payload)
            and (expected_destination_ref is None or record.record_ref == expected_destination_ref)
        ]
        if len(matches) != 1:
            return None
        return RouteDestination(matches[0].record_ref)

    def _healthy_and_fresh(self, payload: Mapping[str, object]) -> bool:
        expiry = payload.get("health_expires_at")
        if payload.get("health_state") != "healthy" or not isinstance(expiry, str):
            return False
        try:
            parsed_expiry = datetime.fromisoformat(expiry)
            return parsed_expiry.tzinfo is not None and parsed_expiry > self._now_factory()
        except ValueError:
            return False


class FrontDeskRoutingApi:
    """Record a bounded Front Desk routing outcome for an existing conversation."""

    path = "/v1/conversation-routing-requests"
    route_ref = "conversation.front-desk-routing-request.v1"
    required_permission = "agent.context.read"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: RoutingStore,
        registry: RouteDestinationRegistry,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._store = store
        self._registry = registry
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if environ.get("REQUEST_METHOD") != "POST" or environ.get("PATH_INFO") != self.path:
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            request = self._parse_request(environ)
            scope = TenantScope(membership.tenant_ref, identity.environment_ref, correlation_ref)
            conversation = self._store.get(scope, "conversation", request["conversation_ref"])
            if conversation is None or conversation.payload.get("active_turn_ref") is not None:
                raise AuthorizationError("conversation_not_routable")
            record_ref = f"front-desk:{request['event_ref']}"
            existing = self._store.get(scope, "routing", record_ref)
            if existing is not None:
                if (
                    existing.payload.get("conversation_ref") != request["conversation_ref"]
                    or existing.payload.get("route_purpose") != request["route_purpose"]
                    or existing.payload.get("route_action") != request["route_action"]
                    or existing.payload.get("offer_ref") != request.get("offer_ref")
                ):
                    return self._respond(
                        start_response,
                        "409 Conflict",
                        headers,
                        {"error": "state_conflict", "correlation_ref": correlation_ref},
                    )
                return self._respond(start_response, "200 OK", headers, self._public_body(existing.payload, correlation_ref))
            route_purpose = cast(RoutePurpose, request["route_purpose"])
            action = request["route_action"]
            expected_destination_ref = None
            if action == "request" and "offer_ref" in request:
                offer = self._store.get(scope, "routing", request["offer_ref"])
                if (
                    offer is None
                    or offer.payload.get("record_type") != "front_desk_routing_request"
                    or offer.payload.get("conversation_ref") != request["conversation_ref"]
                    or offer.payload.get("route_purpose") != route_purpose
                    or offer.payload.get("outcome")
                    not in {"route_offered", "handoff_offered"}
                    or not isinstance(offer.payload.get("destination_ref"), str)
                ):
                    raise AuthorizationError("invalid_route_offer")
                expected_destination_ref = cast(str, offer.payload["destination_ref"])
            destination = self._registry.destination_for(
                scope, route_purpose, expected_destination_ref
            )
            outcome, public_message = self._outcome(route_purpose, action, destination)
            payload: dict[str, object] = {
                "record_type": "front_desk_routing_request",
                "routing_request_ref": record_ref,
                "conversation_ref": request["conversation_ref"],
                "route_purpose": request["route_purpose"],
                "event_ref": request["event_ref"],
                "route_action": action,
                "outcome": outcome,
                "public_message": public_message,
                "review_state": "new",
            }
            if destination is not None:
                payload["destination_ref"] = destination.destination_ref
            if "offer_ref" in request:
                payload["offer_ref"] = request["offer_ref"]
            self._store.save(scope, "routing", VersionedRecord(record_ref, "v1", payload))
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})

        self._audit_sink.record(
            AuditEvent(
                "allowed",
                cast(str, payload["outcome"]),
                correlation_ref,
                self.route_ref,
                identity.principal_ref,
                membership.tenant_ref,
            )
        )
        return self._respond(start_response, "200 OK", headers, self._public_body(payload, correlation_ref))

    @staticmethod
    def _parse_request(environ: Mapping[str, object]) -> dict[str, str]:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = cast(object, environ.get("wsgi.input"))
        if not hasattr(raw, "read") or content_length < 2:
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("invalid_request")
        base = {"conversation_ref", "route_purpose", "event_ref"}
        keys = set(payload)
        if keys == base:
            payload["route_action"] = "request"
        elif keys == base | {"route_action"} and payload.get("route_action") == "offer":
            pass
        elif keys == base | {"route_action", "offer_ref"} and payload.get("route_action") == "request":
            pass
        else:
            raise ValueError("invalid_request")
        if not all(isinstance(payload[name], str) and payload[name] for name in payload):
            raise ValueError("invalid_request")
        if payload["route_purpose"] not in {"support", "human_support", "human_sales"}:
            raise ValueError("invalid_request")
        if any(len(cast(str, payload[name])) > 240 for name in payload):
            raise ValueError("invalid_request")
        return cast(dict[str, str], payload)

    @staticmethod
    def _outcome(
        route_purpose: RoutePurpose, action: str, destination: RouteDestination | None
    ) -> tuple[str, str]:
        if destination is None:
            unavailable = {
                "support": "Support is not available through this channel right now.",
                "human_support": "Human support is not available through this channel right now.",
                "human_sales": "Human Sales is not available through this channel right now.",
            }
            return "safe_unavailable", unavailable[route_purpose]
        if route_purpose == "support" and action == "offer":
            return "route_offered", "I can connect you with Support."
        if route_purpose == "human_support" and action == "offer":
            return "handoff_offered", "I can help you reach human support."
        if route_purpose == "human_sales" and action == "offer":
            return "handoff_offered", "I can help you request a route to human sales. This does not share contact details or confirm availability."
        if route_purpose == "support":
            return "route_requested", "Your request has been sent to Support."
        if route_purpose == "human_sales":
            return "handoff_requested", "Your request for human sales has been recorded. This does not confirm a salesperson or availability."
        return "handoff_requested", "Your request for human support has been sent."

    @staticmethod
    def _public_body(payload: Mapping[str, object], correlation_ref: str) -> dict[str, object]:
        return {
            "routing_request_ref": payload["routing_request_ref"],
            "outcome": payload["outcome"],
            "public_message": payload["public_message"],
            "correlation_ref": correlation_ref,
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


class FrontDeskHumanSalesRequestsApi:
    """List opaque, recorded Human Sales requests for a tenant administrator."""

    path = "/v1/front-desk/human-sales-requests"
    route_ref = "platform.front-desk-human-sales-request-list.v1"
    required_permission = "platform.front-desk.configure"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: RoutingStore,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._store = store
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        method = environ.get("REQUEST_METHOD")
        path = environ.get("PATH_INFO")
        if method != "GET" and not (method == "POST" and isinstance(path, str) and path.startswith(f"{self.path}/")):
            return FrontDeskRoutingApi._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            scope = TenantScope(membership.tenant_ref, identity.environment_ref, correlation_ref)
            if method == "GET":
                requests = [
                    self._public(record.payload)
                    for record in self._store.list(scope, "routing", limit=100)
                    if record.payload.get("record_type") == "front_desk_routing_request"
                    and record.payload.get("route_purpose") == "human_sales"
                    and record.payload.get("route_action") == "request"
                    and record.payload.get("outcome") == "handoff_requested"
                ]
            else:
                request_ref, separator, operation = cast(str, path).removeprefix(f"{self.path}/").rpartition("/")
                record = self._store.get(scope, "routing", request_ref)
                if (
                    not separator
                    or operation not in {"review", "close"}
                    or record is None
                    or record.payload.get("record_type") != "front_desk_routing_request"
                    or record.payload.get("route_purpose") != "human_sales"
                    or record.payload.get("route_action") != "request"
                    or record.payload.get("outcome") != "handoff_requested"
                ):
                    raise AuthorizationError("invalid_human_sales_request")
                payload = dict(record.payload)
                current_state = payload.get("review_state", "new")
                if current_state not in {"new", "reviewed", "closed"}:
                    raise AuthorizationError("invalid_review_state")
                if operation == "review" and current_state in {"new", "reviewed"}:
                    payload["review_state"] = "reviewed"
                elif operation == "close" and current_state in {"reviewed", "closed"}:
                    payload["review_state"] = "closed"
                else:
                    raise AuthorizationError("invalid_review_transition")
                self._store.save(scope, "routing", VersionedRecord(record.record_ref, record.contract_version, payload))
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return FrontDeskRoutingApi._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except AuthorizationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return FrontDeskRoutingApi._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        outcome = "human_sales_requests_listed" if method == "GET" else {
            "review": "human_sales_request_reviewed",
            "close": "human_sales_request_closed",
        }[operation]
        self._audit_sink.record(AuditEvent("allowed", outcome, correlation_ref, self.route_ref, identity.principal_ref, membership.tenant_ref))
        body: dict[str, object] = {"correlation_ref": correlation_ref}
        if method == "GET":
            body["requests"] = requests
        else:
            body["request"] = self._public(payload)
        return FrontDeskRoutingApi._respond(start_response, "200 OK", headers, body)

    @staticmethod
    def _public(payload: Mapping[str, object]) -> dict[str, str]:
        return {
            "routing_request_ref": cast(str, payload["routing_request_ref"]),
            "outcome": cast(str, payload["outcome"]),
            "public_message": cast(str, payload["public_message"]),
            "review_state": cast(str, payload.get("review_state", "new")),
        }

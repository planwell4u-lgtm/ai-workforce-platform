"""Protected, idempotent consent-gated HubSpot lead endpoint."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from typing import Protocol, cast

from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord
from ai_workforce_integration.hubspot_lead import HubSpotClient, HubSpotLeadRejected, HubSpotLeadRequest, HubSpotLeadUncertain

from .b1 import AuditEvent, AuditSink, AuthenticationError, AuthorizationError, IdentityVerifier, MembershipDirectory


class LeadStore(Protocol):
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: ...
    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None: ...


class SalesLeadApi:
    path = "/v1/sales-leads"
    route_ref = "integration.hubspot.lead.create.v1"
    required_permission = "integration.crm.lead.create"

    def __init__(self, verifier: IdentityVerifier, memberships: MembershipDirectory, audit_sink: AuditSink, store: LeadStore, client: HubSpotClient, environment_ref: str, correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4())) -> None:
        self._verifier, self._memberships, self._audit_sink = verifier, memberships, audit_sink
        self._store, self._client, self._environment_ref, self._correlation_factory = store, client, environment_ref, correlation_factory

    def __call__(self, environ: Mapping[str, object], start_response: Callable[..., object]) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        try:
            if environ.get("REQUEST_METHOD") != "POST" or environ.get("PATH_INFO") != self.path:
                return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if self.required_permission not in membership.permissions or self.required_permission not in identity.granted_permissions:
                raise AuthorizationError("insufficient_permission")
            request, idempotency_ref = self._parse_request(environ)
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        scope = TenantScope(membership.tenant_ref, self._environment_ref, correlation_ref)
        existing = self._store.get(scope, "action", idempotency_ref)
        if existing is not None:
            return self._respond(start_response, self._status(existing.payload, repeated=True), headers, existing.payload)
        try:
            contact_ref = self._client.create_lead(request)
            body: dict[str, object] = {"outcome": "succeeded", "idempotency_ref": idempotency_ref, "contact_ref": contact_ref, "correlation_ref": correlation_ref}
        except HubSpotLeadRejected as error:
            body = {"outcome": "failed", "idempotency_ref": idempotency_ref, "reason": str(error), "correlation_ref": correlation_ref}
        except HubSpotLeadUncertain as error:
            body = {"outcome": "uncertain", "idempotency_ref": idempotency_ref, "reason": str(error), "correlation_ref": correlation_ref}
        self._store.save(scope, "action", VersionedRecord(idempotency_ref, "v1", body))
        self._audit_sink.record(AuditEvent("allowed", str(body["outcome"]), correlation_ref, self.route_ref, identity.principal_ref, membership.tenant_ref))
        return self._respond(start_response, self._status(body), headers, body)

    @staticmethod
    def _parse_request(environ: Mapping[str, object]) -> tuple[HubSpotLeadRequest, str]:
        raw, length = cast(object, environ.get("wsgi.input")), int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        if not hasattr(raw, "read"):
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(length).decode("utf-8"))
        if not isinstance(payload, dict) or set(payload) != {"name", "email", "consent", "idempotency_ref"}:
            raise ValueError("invalid_request")
        name, email, consent, idempotency_ref = (payload.get(key) for key in ("name", "email", "consent", "idempotency_ref"))
        if not isinstance(name, str) or not name.strip() or len(name) > 200 or not isinstance(email, str) or "@" not in email or len(email) > 320 or consent is not True or not isinstance(idempotency_ref, str) or not idempotency_ref:
            raise ValueError("invalid_request")
        return HubSpotLeadRequest(name.strip(), email.strip(), consent), idempotency_ref

    @staticmethod
    def _status(body: Mapping[str, object], *, repeated: bool = False) -> str:
        if body.get("outcome") == "succeeded": return "200 OK" if repeated else "201 Created"
        if body.get("outcome") == "uncertain": return "202 Accepted"
        return "502 Bad Gateway"

    @staticmethod
    def _respond(start_response: Callable[..., object], status: str, headers: list[tuple[str, str]], body: object) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

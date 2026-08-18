"""B1 tenant-aware identity and protected API entry."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
import uuid
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Literal

PrincipalType = Literal["human", "workload"]


class AuthenticationError(Exception):
    """A bearer credential cannot establish an active identity."""


class AuthorizationError(Exception):
    """An identity has no current authority for this route."""


@dataclass(frozen=True)
class IdentityContext:
    principal_ref: str
    principal_type: PrincipalType
    issuer_ref: str
    environment_ref: str
    authenticated_at: int
    granted_permissions: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Membership:
    principal_ref: str
    tenant_ref: str
    status: Literal["active", "revoked"]
    permissions: frozenset[str]


@dataclass(frozen=True)
class AuditEvent:
    outcome: Literal["allowed", "denied"]
    reason: str
    correlation_ref: str
    route_ref: str
    principal_ref: str | None = None
    tenant_ref: str | None = None


class IdentityVerifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        raise NotImplementedError


class MembershipDirectory:
    def resolve(self, principal_ref: str) -> Membership:
        raise NotImplementedError


class AuditSink:
    def record(self, event: AuditEvent) -> None:
        raise NotImplementedError


class InMemoryMembershipDirectory(MembershipDirectory):
    def __init__(self, memberships: Iterable[Membership]) -> None:
        self._memberships = {item.principal_ref: item for item in memberships}

    def resolve(self, principal_ref: str) -> Membership:
        membership = self._memberships.get(principal_ref)
        if membership is None or membership.status != "active":
            raise AuthorizationError("membership_not_active")
        return membership


class InMemoryAuditSink(AuditSink):
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        self.events.append(event)


class SignedBearerTokenVerifier(IdentityVerifier):
    """Verify a short-lived HMAC-SHA256 token in a controlled B1 sandbox."""

    def __init__(self, signing_key: bytes, audience: str, environment_ref: str) -> None:
        if not signing_key:
            raise ValueError("signing_key must not be empty")
        self._signing_key = signing_key
        self._audience = audience
        self._environment_ref = environment_ref

    def verify(self, authorization: str | None) -> IdentityContext:
        if authorization is None or not authorization.startswith("Bearer "):
            raise AuthenticationError("missing_bearer_token")
        try:
            encoded_claims, encoded_signature = authorization.removeprefix("Bearer ").split(".", 1)
            expected = hmac.new(
                self._signing_key, encoded_claims.encode("ascii"), hashlib.sha256
            ).digest()
            if not hmac.compare_digest(expected, _decode(encoded_signature)):
                raise AuthenticationError("invalid_signature")
            claims = json.loads(_decode(encoded_claims))
            principal_type = claims["principal_type"]
            if principal_type not in {"human", "workload"}:
                raise AuthenticationError("invalid_principal_type")
            now = int(time.time())
            if claims["aud"] != self._audience or claims["env"] != self._environment_ref:
                raise AuthenticationError("invalid_audience_or_environment")
            if claims["exp"] <= now or claims["iat"] > now or not claims["sub"]:
                raise AuthenticationError("expired_or_invalid_token")
            return IdentityContext(
                claims["sub"], principal_type, claims["iss"], claims["env"], claims["iat"]
            )
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise AuthenticationError("invalid_token") from error


class ProtectedApi:
    route_ref = "platform.foundation.tenant-context.v1"
    required_permission = "platform.tenant-context.read"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, str], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if (
            environ.get("REQUEST_METHOD") != "GET"
            or environ.get("PATH_INFO") != "/v1/tenant-context"
        ):
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(environ.get("HTTP_AUTHORIZATION"))
            membership = self._memberships.resolve(identity.principal_ref)
            if self.required_permission not in membership.permissions:
                raise AuthorizationError("insufficient_permission")
        except AuthenticationError as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except AuthorizationError as error:
            self._audit_sink.record(
                AuditEvent("denied", str(error), correlation_ref, self.route_ref)
            )
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                "authorized",
                correlation_ref,
                self.route_ref,
                identity.principal_ref,
                membership.tenant_ref,
            )
        )
        return self._respond(
            start_response,
            "200 OK",
            headers,
            {
                "principal_ref": identity.principal_ref,
                "principal_type": identity.principal_type,
                "tenant_ref": membership.tenant_ref,
                "route_ref": self.route_ref,
                "correlation_ref": correlation_ref,
            },
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


def issue_sandbox_token(
    signing_key: bytes,
    *,
    subject: str,
    principal_type: PrincipalType,
    audience: str,
    environment_ref: str,
    expires_at: int | None = None,
) -> str:
    """Create a test-only token; issuance is deliberately not exposed by the API."""
    now = int(time.time())
    claims = {
        "sub": subject,
        "principal_type": principal_type,
        "aud": audience,
        "env": environment_ref,
        "iss": "b1-sandbox-issuer",
        "iat": now,
        "exp": expires_at if expires_at is not None else now + 300,
    }
    encoded_claims = _encode(json.dumps(claims, separators=(",", ":"), sort_keys=True).encode())
    signature = hmac.new(signing_key, encoded_claims.encode("ascii"), hashlib.sha256).digest()
    return f"{encoded_claims}.{_encode(signature)}"


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))

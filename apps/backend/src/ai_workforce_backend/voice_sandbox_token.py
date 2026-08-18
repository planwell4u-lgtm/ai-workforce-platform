"""Short-lived browser access for the local LiveKit evaluation sandbox."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from datetime import timedelta
from typing import cast

from livekit import api

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class VoiceSandboxTokenApi:
    """Issue a room-bound token without ever returning provider credentials."""

    route_ref = "voice.local-sandbox.token.v1"
    required_permission = "agent.context.read"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        *,
        url: str,
        api_key: str,
        api_secret: str,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        if not url.startswith(("ws://", "wss://")):
            raise ValueError("LIVEKIT_SANDBOX_URL must use ws:// or wss://")
        if not api_key or not api_secret:
            raise ValueError("LiveKit sandbox credentials are required")
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._url = url
        self._api_key = api_key
        self._api_secret = api_secret
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation_ref)]
        if environ.get("REQUEST_METHOD") != "POST" or environ.get("PATH_INFO") != "/v1/voice-sandbox-token":
            return self._respond(start_response, "404 Not Found", headers, {"error": "not_found"})
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if (
                self.required_permission not in membership.permissions
                or self.required_permission not in identity.granted_permissions
            ):
                raise AuthorizationError("insufficient_permission")
            room_ref = self._room_ref(environ, membership.tenant_ref)
            token = (
                api.AccessToken(self._api_key, self._api_secret)
                .with_ttl(timedelta(minutes=5))
                .with_identity(f"voice-{uuid.uuid4()}")
                .with_name("Planwell local voice test")
                .with_grants(api.VideoGrants(room_join=True, room=room_ref))
                .to_jwt()
            )
        except AuthenticationError as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except (AuthorizationError, TypeError, ValueError) as error:
            self._audit_sink.record(AuditEvent("denied", str(error), correlation_ref, self.route_ref))
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                "local_voice_token_issued",
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
            {"url": self._url, "token": token, "room_ref": room_ref, "correlation_ref": correlation_ref},
        )

    @staticmethod
    def _room_ref(environ: Mapping[str, object], tenant_ref: str) -> str:
        content_length = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        if content_length == 0:
            return f"local-voice-{tenant_ref}-{uuid.uuid4()}"
        raw = environ.get("wsgi.input")
        if not hasattr(raw, "read"):
            raise TypeError("invalid_request")
        payload = json.loads(raw.read(content_length).decode("utf-8"))
        room_ref = payload.get("room_ref") if isinstance(payload, dict) else None
        expected_prefix = f"local-voice-{tenant_ref}-"
        if not isinstance(room_ref, str) or not room_ref.startswith(expected_prefix):
            raise ValueError("invalid_room_ref")
        uuid.UUID(room_ref.removeprefix(expected_prefix))
        return room_ref

    @staticmethod
    def _respond(
        start_response: Callable[..., object], status: str, headers: list[tuple[str, str]], body: object
    ) -> list[bytes]:
        encoded = json.dumps(body, separators=(",", ":")).encode()
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

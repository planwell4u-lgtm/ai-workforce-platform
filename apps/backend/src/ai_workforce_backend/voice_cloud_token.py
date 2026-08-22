"""Short-lived browser access to one explicitly configured LiveKit Cloud agent."""

from __future__ import annotations

import json
import uuid
from collections.abc import Callable, Mapping
from datetime import timedelta
from typing import cast

from livekit import api
from ai_workforce_agent.context import LocalKnowledgeSource

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)


class VoiceCloudAgentTokenApi:
    """Issue a tenant-bound token that dispatches only the configured Cloud agent."""

    route_ref = "voice.cloud-agent.token.v1"
    required_permission = "agent.context.read"
    path = "/v1/livekit-cloud-agent-token"

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        *,
        url: str,
        api_key: str,
        api_secret: str,
        agent_name: str,
        knowledge: LocalKnowledgeSource,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        if not url.startswith("wss://"):
            raise ValueError("LIVEKIT_CLOUD_URL must use wss://")
        if not api_key or not api_secret or not agent_name:
            raise ValueError("LiveKit Cloud credentials and agent name are required")
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._url = url
        self._api_key = api_key
        self._api_secret = api_secret
        self._agent_name = agent_name
        self._knowledge = knowledge
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
            body_size = int(cast(str, environ.get("CONTENT_LENGTH") or "0"))
            if body_size < 1 or body_size > 512:
                raise AuthorizationError("invalid_context_request")
            request = json.loads(cast(object, environ.get("wsgi.input")).read(body_size))
            query = request.get("support_query") if isinstance(request, dict) else None
            if not isinstance(query, str) or not query.strip() or len(query) > 240:
                raise AuthorizationError("invalid_context_request")
            entry = self._knowledge.search(membership.tenant_ref, query)
            if entry is None:
                raise AuthorizationError("approved_context_unavailable")
            room_ref = f"cloud-agent-{membership.tenant_ref}-{uuid.uuid4()}"
            token = (
                api.AccessToken(self._api_key, self._api_secret)
                .with_ttl(timedelta(minutes=5))
                .with_identity(f"cloud-agent-user-{uuid.uuid4()}")
                .with_name("Planwell browser agent test")
                .with_grants(api.VideoGrants(room_join=True, room=room_ref))
                .with_room_config(
                    api.RoomConfiguration(
                        agents=[
                            api.RoomAgentDispatch(
                                agent_name=self._agent_name,
                                metadata=json.dumps(
                                    {"mode": "support-faq", "source_ref": entry.source_ref,
                                     "support_context": entry.excerpt}, separators=(",", ":")
                                ),
                            )
                        ]
                    )
                )
                .to_jwt()
            )
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
        self._audit_sink.record(
            AuditEvent(
                "allowed",
                "cloud_agent_token_issued",
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
                "url": self._url,
                "token": token,
                "room_ref": room_ref,
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
        encoded = json.dumps(body, separators=(",", ":")).encode()
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

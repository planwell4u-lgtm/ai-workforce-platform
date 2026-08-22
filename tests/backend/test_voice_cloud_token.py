"""Tests for the protected LiveKit Cloud browser-agent token endpoint."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path

from livekit import api

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from ai_workforce_backend.b1 import (
    IdentityContext,
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_backend.voice_cloud_token import VoiceCloudAgentTokenApi
from ai_workforce_agent.context import KnowledgeEntry, LocalKnowledgeSource


class Verifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        if authorization != "Bearer valid":
            from ai_workforce_backend.b1 import AuthenticationError

            raise AuthenticationError("missing_bearer_token")
        return IdentityContext(
            "auth0|member",
            "human",
            "https://issuer/",
            "local",
            1,
            frozenset({"agent.context.read"}),
        )


class VoiceCloudAgentTokenTests(unittest.TestCase):
    def test_issues_a_short_lived_token_with_only_explicit_agent_dispatch(self) -> None:
        token_api = VoiceCloudAgentTokenApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (
                    Membership(
                        "auth0|member", "tenant-a", "active", frozenset({"agent.context.read"})
                    ),
                )
            ),
            InMemoryAuditSink(),
            url="wss://project.livekit.cloud",
            api_key="cloud-key",
            api_secret="cloud-secret",
            agent_name="planwell-browser-proof",
            knowledge=LocalKnowledgeSource((KnowledgeEntry("faq:v1", "tenant-a", "internal", True, "Q: order tracking\nA: Your order is on its way."),)),
            correlation_factory=lambda: "correlation-a",
        )
        captured: dict[str, object] = {}
        body = b"".join(
            token_api(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": token_api.path,
                    "HTTP_AUTHORIZATION": "Bearer valid",
                    "CONTENT_LENGTH": "25",
                    "wsgi.input": BytesIO(b'{"support_query":"order"}'),
                },
                lambda status, headers: captured.update(status=status),
            )
        )
        response = json.loads(body)
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(response["url"], "wss://project.livekit.cloud")
        self.assertTrue(response["room_ref"].startswith("cloud-agent-tenant-a-"))
        self.assertNotIn("cloud-secret", response)
        claims = api.TokenVerifier("cloud-key", "cloud-secret").verify(response["token"])
        self.assertEqual(claims.video.room, response["room_ref"])
        self.assertEqual(claims.room_config.agents[0].agent_name, "planwell-browser-proof")
        metadata = json.loads(claims.room_config.agents[0].metadata)
        self.assertEqual(metadata["mode"], "support-faq")
        self.assertEqual(metadata["source_ref"], "faq:v1")

"""Tests for the local-only LiveKit browser token endpoint."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from livekit import api

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from ai_workforce_backend.b1 import IdentityContext, InMemoryAuditSink, InMemoryMembershipDirectory, Membership
from ai_workforce_backend.voice_sandbox_token import VoiceSandboxTokenApi


class Verifier:
    def __init__(self, permissions: frozenset[str]) -> None:
        self._permissions = permissions

    def verify(self, authorization: str | None) -> IdentityContext:
        if authorization != "Bearer valid":
            from ai_workforce_backend.b1 import AuthenticationError

            raise AuthenticationError("missing_bearer_token")
        return IdentityContext("auth0|member", "human", "https://issuer/", "local", 1, self._permissions)


class VoiceSandboxTokenTests(unittest.TestCase):
    def _api(self, permissions: frozenset[str] = frozenset({"agent.context.read"})) -> VoiceSandboxTokenApi:
        return VoiceSandboxTokenApi(
            Verifier(permissions),
            InMemoryMembershipDirectory((Membership("auth0|member", "tenant-a", "active", permissions),)),
            InMemoryAuditSink(),
            url="ws://localhost:7880",
            api_key="devkey",
            api_secret="secret",
            correlation_factory=lambda: "correlation-a",
        )

    def test_issues_short_lived_room_bound_token_without_provider_secret(self) -> None:
        captured: dict[str, object] = {}
        body = b"".join(
            self._api()(
                {"REQUEST_METHOD": "POST", "PATH_INFO": "/v1/voice-sandbox-token", "HTTP_AUTHORIZATION": "Bearer valid"},
                lambda status, headers: captured.update(status=status, headers=headers),
            )
        )
        response = json.loads(body)
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(response["url"], "ws://localhost:7880")
        self.assertTrue(response["room_ref"].startswith("local-voice-tenant-a-"))
        self.assertNotIn("secret", response)
        claims = api.TokenVerifier("devkey", "secret").verify(response["token"])
        self.assertEqual(claims.identity, "auth0|member")
        self.assertEqual(claims.video.room, response["room_ref"])
        self.assertTrue(claims.video.room_join)

    def test_requires_the_existing_support_permission(self) -> None:
        captured: dict[str, object] = {}
        body = b"".join(
            self._api(frozenset())(
                {"REQUEST_METHOD": "POST", "PATH_INFO": "/v1/voice-sandbox-token", "HTTP_AUTHORIZATION": "Bearer valid"},
                lambda status, headers: captured.update(status=status),
            )
        )
        self.assertEqual(captured["status"], "403 Forbidden")
        self.assertEqual(json.loads(body), {"error": "forbidden"})

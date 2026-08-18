"""Tests for the local-only LiveKit browser token endpoint."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
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
        self.assertTrue(claims.identity.startswith("voice-"))
        self.assertEqual(claims.video.room, response["room_ref"])
        self.assertTrue(claims.video.room_join)

    def test_allows_a_second_local_participant_to_join_the_same_tenant_room(self) -> None:
        first_body = b"".join(
            self._api()(
                {"REQUEST_METHOD": "POST", "PATH_INFO": "/v1/voice-sandbox-token", "HTTP_AUTHORIZATION": "Bearer valid"},
                lambda status, headers: None,
            )
        )
        first = json.loads(first_body)
        join_body = json.dumps({"room_ref": first["room_ref"]}).encode()
        second_body = b"".join(
            self._api()(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": "/v1/voice-sandbox-token",
                    "HTTP_AUTHORIZATION": "Bearer valid",
                    "CONTENT_LENGTH": str(len(join_body)),
                    "wsgi.input": BytesIO(join_body),
                },
                lambda status, headers: None,
            )
        )
        second = json.loads(second_body)
        first_claims = api.TokenVerifier("devkey", "secret").verify(first["token"])
        second_claims = api.TokenVerifier("devkey", "secret").verify(second["token"])
        self.assertEqual(second["room_ref"], first["room_ref"])
        self.assertNotEqual(second_claims.identity, first_claims.identity)

    def test_rejects_a_room_from_another_tenant(self) -> None:
        join_body = json.dumps({"room_ref": "local-voice-tenant-b-12345678-1234-1234-1234-123456789abc"}).encode()
        captured: dict[str, object] = {}
        body = b"".join(
            self._api()(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": "/v1/voice-sandbox-token",
                    "HTTP_AUTHORIZATION": "Bearer valid",
                    "CONTENT_LENGTH": str(len(join_body)),
                    "wsgi.input": BytesIO(join_body),
                },
                lambda status, headers: captured.update(status=status),
            )
        )
        self.assertEqual(captured["status"], "403 Forbidden")
        self.assertEqual(json.loads(body), {"error": "forbidden"})

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

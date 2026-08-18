"""B1 acceptance tests."""

from __future__ import annotations

import json
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from ai_workforce_backend.b1 import (
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
    ProtectedApi,
    SignedBearerTokenVerifier,
    issue_sandbox_token,
)

KEY = b"test-signing-key"
AUDIENCE = "ai-workforce-api"
ENVIRONMENT = "local"
PERMISSION = "platform.tenant-context.read"


class ProtectedApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditSink()
        memberships = (
            Membership("human-1", "tenant-a", "active", frozenset({PERMISSION})),
            Membership("workload-1", "tenant-a", "active", frozenset({PERMISSION})),
            Membership("revoked-1", "tenant-a", "revoked", frozenset({PERMISSION})),
            Membership("limited-1", "tenant-a", "active", frozenset()),
        )
        self.app = ProtectedApi(
            SignedBearerTokenVerifier(KEY, AUDIENCE, ENVIRONMENT),
            InMemoryMembershipDirectory(memberships),
            self.audit,
            correlation_factory=lambda: "correlation-1",
        )

    def request(self, token: str | None = None) -> tuple[str, dict[str, str], dict[str, object]]:
        captured: dict[str, object] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = status
            captured["headers"] = dict(headers)

        environ = {"REQUEST_METHOD": "GET", "PATH_INFO": "/v1/tenant-context"}
        if token is not None:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        body = b"".join(self.app(environ, start_response))
        return captured["status"], captured["headers"], json.loads(body)

    def token(self, subject: str, principal_type: str = "human", **kwargs: object) -> str:
        return issue_sandbox_token(
            KEY,
            subject=subject,
            principal_type=principal_type,
            audience=AUDIENCE,
            environment_ref=ENVIRONMENT,
            **kwargs,
        )

    def test_authorized_human_access_has_server_resolved_tenant_and_audit(self) -> None:
        status, headers, body = self.request(self.token("human-1"))
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["tenant_ref"], "tenant-a")
        self.assertEqual(body["correlation_ref"], "correlation-1")
        self.assertEqual(headers["X-Correlation-Id"], "correlation-1")
        self.assertEqual(self.audit.events[-1].outcome, "allowed")

    def test_authorized_workload_identity_succeeds(self) -> None:
        status, _, body = self.request(self.token("workload-1", "workload"))
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["principal_type"], "workload")

    def test_missing_or_expired_identity_is_rejected(self) -> None:
        status, _, body = self.request()
        self.assertEqual((status, body), ("401 Unauthorized", {"error": "unauthorized"}))
        status, _, body = self.request(self.token("human-1", expires_at=int(time.time()) - 1))
        self.assertEqual((status, body), ("401 Unauthorized", {"error": "unauthorized"}))

    def test_wrong_environment_is_rejected(self) -> None:
        token = issue_sandbox_token(
            KEY,
            subject="human-1",
            principal_type="human",
            audience=AUDIENCE,
            environment_ref="other",
        )
        status, _, body = self.request(token)
        self.assertEqual((status, body), ("401 Unauthorized", {"error": "unauthorized"}))

    def test_revoked_membership_and_insufficient_permission_are_rejected(self) -> None:
        status, _, body = self.request(self.token("revoked-1"))
        self.assertEqual((status, body), ("403 Forbidden", {"error": "forbidden"}))
        status, _, body = self.request(self.token("limited-1"))
        self.assertEqual((status, body), ("403 Forbidden", {"error": "forbidden"}))

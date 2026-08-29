"""Tests for durable ticket state in the authorized Admin history response."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_backend.admin_conversations import AdminConversationsApi
from ai_workforce_backend.b1 import (
    IdentityContext,
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord


class Verifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        return IdentityContext(
            "auth0|operator",
            "human",
            "https://issuer/",
            "staging",
            1,
            frozenset({"operator.status.read"}),
        )


class Store:
    def list(self, scope: TenantScope, kind: str) -> list[VersionedRecord]:
        if scope.tenant_ref != "tenant-a":
            return []
        if kind == "conversation":
            return [
                VersionedRecord(
                    "conversation-a",
                    "v1",
                    {
                        "transcript": [{"sender": "you", "text": "Need help"}],
                        "turn_outcomes": {"turn-1": "succeeded"},
                    },
                )
            ]
        if kind == "action":
            return [
                VersionedRecord(
                    "conversation-a", "v1", {"outcome": "succeeded", "ticket_ref": "CS-4"}
                )
            ]
        return []


class AdminConversationTests(unittest.TestCase):
    def test_history_includes_saved_ticket_reference(self) -> None:
        api = AdminConversationsApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (
                    Membership(
                        "auth0|operator", "tenant-a", "active", frozenset({"operator.status.read"})
                    ),
                )
            ),
            InMemoryAuditSink(),
            Store(),
            "staging",
        )
        captured: dict[str, object] = {}

        body = b"".join(
            api(
                {
                    "REQUEST_METHOD": "GET",
                    "PATH_INFO": "/v1/admin/conversations",
                    "HTTP_AUTHORIZATION": "Bearer valid",
                },
                lambda status, headers: captured.update(status=status),
            )
        )

        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(json.loads(body)["conversations"][0]["ticket_ref"], "CS-4")
        self.assertEqual(json.loads(body)["conversations"][0]["ticket_outcome"], "succeeded")

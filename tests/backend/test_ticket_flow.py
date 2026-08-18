"""End-to-end backend flow tests with controlled identity, store, and Jira doubles."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "integration" / "python" / "src"))

from ai_workforce_backend.b1 import (
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_backend.ticket_flow import SupportTicketApi
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord
from ai_workforce_integration.support_ticket import SupportTicketResult


class Verifier:
    def verify(self, authorization: str | None):
        from ai_workforce_backend.b1 import IdentityContext

        return IdentityContext(
            "auth0|user",
            "human",
            "https://issuer/",
            "staging",
            1,
            frozenset({"integration.support-ticket.create"}),
        )


class Store:
    def __init__(self) -> None:
        self.records: dict[tuple[str, str], VersionedRecord] = {}

    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None:
        return self.records.get((scope.tenant_ref, record_ref))

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None:
        self.records[(scope.tenant_ref, record.record_ref)] = record


class Action:
    def __init__(self) -> None:
        self.calls = 0

    def request(self, request, permissions):
        self.calls += 1
        return SupportTicketResult("succeeded", request.idempotency_ref, "CS-4")


class SupportTicketFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = Store()
        self.action = Action()
        self.api = SupportTicketApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (Membership("auth0|user", "tenant-a", "active", frozenset({"integration.support-ticket.create"})),)
            ),
            InMemoryAuditSink(),
            self.store,
            self.action,
            correlation_factory=lambda: "correlation-1",
        )

    def request(self, payload: dict[str, str]) -> tuple[str, dict[str, object]]:
        captured: dict[str, object] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = status

        raw = json.dumps(payload).encode()
        body = b"".join(
            self.api(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": "/v1/support-tickets",
                    "HTTP_AUTHORIZATION": "Bearer valid",
                    "CONTENT_LENGTH": str(len(raw)),
                    "wsgi.input": BytesIO(raw),
                },
                start_response,
            )
        )
        return str(captured["status"]), json.loads(body)

    def test_authenticated_request_persists_then_creates_one_jira_ticket(self) -> None:
        payload = {"conversation_ref": "conversation-a", "idempotency_ref": "request-1", "summary": "Need help"}
        status, body = self.request(payload)
        self.assertEqual(status, "201 Created")
        self.assertEqual(body["ticket_ref"], "CS-4")
        self.assertEqual(self.store.records[("tenant-a", "request-1")].payload["outcome"], "succeeded")
        repeat_status, repeat_body = self.request(payload)
        self.assertEqual((repeat_status, repeat_body), ("200 OK", body))
        self.assertEqual(self.action.calls, 1)

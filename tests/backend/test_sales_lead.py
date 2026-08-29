"""Tests for the consent-gated HubSpot lead boundary using a local fake."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "apps" / "backend" / "src"), str(ROOT / "packages" / "data" / "python" / "src"), str(ROOT / "packages" / "integration" / "python" / "src")]

from ai_workforce_backend.b1 import IdentityContext, InMemoryAuditSink, InMemoryMembershipDirectory, Membership
from ai_workforce_backend.sales_lead import SalesLeadApi
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord
from ai_workforce_integration.hubspot_lead import HubSpotLeadRejected


PERMISSION = "integration.crm.lead.create"


class Verifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        return IdentityContext("auth0|user", "human", "https://issuer/", "staging", 1, frozenset({PERMISSION}))


class Store:
    def __init__(self) -> None: self.records: dict[str, VersionedRecord] = {}
    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None: return self.records.get(record_ref)
    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None: self.records[record.record_ref] = record


class Client:
    def __init__(self) -> None: self.calls = 0
    def create_lead(self, request: object) -> str: self.calls += 1; return "contact-1"


class RejectedClient:
    def create_lead(self, request: object) -> str: raise HubSpotLeadRejected("hubspot_rejected_400")


class SalesLeadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store, self.client = Store(), Client()
        self.api = SalesLeadApi(Verifier(), InMemoryMembershipDirectory((Membership("auth0|user", "tenant-a", "active", frozenset({PERMISSION})),)), InMemoryAuditSink(), self.store, self.client, "staging", correlation_factory=lambda: "correlation-1")

    def request(self, payload: dict[str, object]) -> tuple[str, dict[str, object]]:
        captured: dict[str, object] = {}
        raw = json.dumps(payload).encode()
        body = b"".join(self.api({"REQUEST_METHOD": "POST", "PATH_INFO": "/v1/sales-leads", "HTTP_AUTHORIZATION": "Bearer valid", "CONTENT_LENGTH": str(len(raw)), "wsgi.input": BytesIO(raw)}, lambda status, headers: captured.update(status=status)))
        return str(captured["status"]), json.loads(body)

    def test_explicit_consent_creates_and_records_one_contact(self) -> None:
        payload = {"name": "Test Owner", "email": "owner@example.test", "consent": True, "idempotency_ref": "lead-1"}
        status, body = self.request(payload)
        self.assertEqual((status, body["contact_ref"]), ("201 Created", "contact-1"))
        repeated_status, repeated = self.request(payload)
        self.assertEqual((repeated_status, repeated), ("200 OK", body))
        self.assertEqual(self.client.calls, 1)

    def test_missing_consent_never_calls_hubspot(self) -> None:
        status, body = self.request({"name": "Test Owner", "email": "owner@example.test", "consent": False, "idempotency_ref": "lead-2"})
        self.assertEqual((status, body), ("403 Forbidden", {"error": "forbidden"}))
        self.assertEqual(self.client.calls, 0)

    def test_hubspot_rejection_is_not_reported_as_success(self) -> None:
        self.api._client = RejectedClient()
        status, body = self.request({"name": "Test Owner", "email": "owner@example.test", "consent": True, "idempotency_ref": "lead-3"})
        self.assertEqual((status, body["outcome"]), ("422 Unprocessable Content", "failed"))

"""Tests for tenant-admin Front Desk destination configuration."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_backend.b1 import IdentityContext, InMemoryAuditSink, InMemoryMembershipDirectory, Membership
from ai_workforce_backend.front_desk_destinations import FrontDeskDestinationsApi
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord


class Verifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        return IdentityContext(
            "auth0|admin", "human", "https://issuer/", "staging", 1, frozenset({"platform.front-desk.configure"})
        )


class Store:
    def __init__(self) -> None:
        self.records: dict[tuple[str, str, str], VersionedRecord] = {}
        self.active_claims: dict[tuple[str, str], str] = {}

    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None:
        return self.records.get((scope.tenant_ref, kind, record_ref))

    def list(self, scope: TenantScope, kind: str, limit: int = 25) -> list[VersionedRecord]:
        return [record for (tenant, stored_kind, _), record in self.records.items() if tenant == scope.tenant_ref and stored_kind == kind][:limit]

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None:
        self.records[(scope.tenant_ref, kind, record.record_ref)] = record

    def compare_and_swap_versioned(
        self, scope: TenantScope, kind: str, record: VersionedRecord, expected_version: int
    ) -> bool:
        current = self.get(scope, kind, record.record_ref)
        if current is None or current.payload.get("configuration_version") != expected_version:
            return False
        self.save(scope, kind, record)
        return True

    def activate_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        purpose = record.payload.get("route_purpose")
        if not isinstance(purpose, str) or (scope.tenant_ref, purpose) in self.active_claims:
            return False
        if not self.compare_and_swap_versioned(scope, "routing", record, expected_version):
            return False
        self.active_claims[(scope.tenant_ref, purpose)] = record.record_ref
        return True

    def suspend_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        purpose = record.payload.get("route_purpose")
        if not isinstance(purpose, str) or self.active_claims.get((scope.tenant_ref, purpose)) != record.record_ref:
            return False
        if not self.compare_and_swap_versioned(scope, "routing", record, expected_version):
            return False
        del self.active_claims[(scope.tenant_ref, purpose)]
        return True

    def withdraw_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        return self.suspend_front_desk_destination(scope, record, expected_version)


class DestinationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = Store()
        self.api = FrontDeskDestinationsApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (Membership("auth0|admin", "tenant-a", "active", frozenset({"platform.front-desk.configure"})),)
            ),
            InMemoryAuditSink(),
            self.store,
            correlation_factory=lambda: "correlation-1",
            destination_factory=lambda: "dst-1",
        )

    def call(self, method: str, path: str, payload: dict[str, object] | None = None) -> tuple[str, dict[str, object]]:
        captured: dict[str, object] = {}
        raw = json.dumps(payload).encode() if payload is not None else b""
        body = b"".join(
            self.api(
                {"REQUEST_METHOD": method, "PATH_INFO": path, "HTTP_AUTHORIZATION": "Bearer valid", "CONTENT_LENGTH": str(len(raw)), "wsgi.input": BytesIO(raw)},
                lambda status, headers: captured.update(status=status),
            )
        )
        return str(captured["status"]), json.loads(body)

    def test_draft_validate_activate_and_suspend(self) -> None:
        draft = {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"]}
        status, body = self.call("POST", "/v1/front-desk/destinations", draft)
        self.assertEqual((status, body["lifecycle_state"]), ("201 Created", "draft"))
        self.assertEqual(self.call("POST", "/v1/front-desk/destinations/dst-1/validate", {"expected_configuration_version": 1})[1]["lifecycle_state"], "validated")
        self.assertEqual(self.call("POST", "/v1/front-desk/destinations/dst-1/activate", {"expected_configuration_version": 2})[1]["lifecycle_state"], "active")
        self.assertEqual(self.call("POST", "/v1/front-desk/destinations/dst-1/suspend", {"expected_configuration_version": 3})[1]["lifecycle_state"], "suspended")

    def test_human_sales_destination_is_an_allowed_pair(self) -> None:
        draft = {"route_purpose": "human_sales", "destination_type": "human_sales_route", "channel_scope": ["web_chat"]}
        status, body = self.call("POST", "/v1/front-desk/destinations", draft)
        self.assertEqual((status, body["route_purpose"], body["lifecycle_state"]), ("201 Created", "human_sales", "draft"))

    def test_only_one_active_destination_per_purpose(self) -> None:
        draft = {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"]}
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-1/validate", {"expected_configuration_version": 1})
        self.call("POST", "/v1/front-desk/destinations/dst-1/activate", {"expected_configuration_version": 2})
        self.api._destination_factory = lambda: "dst-2"
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-2/validate", {"expected_configuration_version": 1})
        status, body = self.call("POST", "/v1/front-desk/destinations/dst-2/activate", {"expected_configuration_version": 2})
        self.assertEqual((status, body["error"]), ("409 Conflict", "state_conflict"))

    def test_unlisted_fields_are_rejected(self) -> None:
        status, body = self.call("POST", "/v1/front-desk/destinations", {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"], "target_ref": "not-allowed"})
        self.assertEqual((status, body), ("400 Bad Request", {"error": "invalid_request"}))

    def test_stale_version_cannot_overwrite_a_newer_change(self) -> None:
        draft = {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"]}
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-1/validate", {"expected_configuration_version": 1})
        status, body = self.call("POST", "/v1/front-desk/destinations/dst-1/activate", {"expected_configuration_version": 1})
        self.assertEqual((status, body["error"]), ("409 Conflict", "state_conflict"))

    def test_suspending_releases_the_purpose_for_a_new_destination(self) -> None:
        draft = {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"]}
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-1/validate", {"expected_configuration_version": 1})
        self.call("POST", "/v1/front-desk/destinations/dst-1/activate", {"expected_configuration_version": 2})
        self.call("POST", "/v1/front-desk/destinations/dst-1/suspend", {"expected_configuration_version": 3})
        self.api._destination_factory = lambda: "dst-2"
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-2/validate", {"expected_configuration_version": 1})
        status, body = self.call("POST", "/v1/front-desk/destinations/dst-2/activate", {"expected_configuration_version": 2})
        self.assertEqual((status, body["lifecycle_state"]), ("200 OK", "active"))

    def test_withdrawing_an_active_destination_releases_its_purpose(self) -> None:
        draft = {"route_purpose": "support", "destination_type": "support_worker", "channel_scope": ["web_chat"]}
        self.call("POST", "/v1/front-desk/destinations", draft)
        self.call("POST", "/v1/front-desk/destinations/dst-1/validate", {"expected_configuration_version": 1})
        self.call("POST", "/v1/front-desk/destinations/dst-1/activate", {"expected_configuration_version": 2})
        status, body = self.call("POST", "/v1/front-desk/destinations/dst-1/withdraw", {"expected_configuration_version": 3})
        self.assertEqual((status, body["lifecycle_state"]), ("200 OK", "withdrawn"))
        self.assertNotIn(("tenant-a", "support"), self.store.active_claims)

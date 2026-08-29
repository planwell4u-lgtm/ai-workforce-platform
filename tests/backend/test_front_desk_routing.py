"""Test-only Front Desk routing boundary tests."""

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
from ai_workforce_backend.front_desk_routing import ActiveDestinationRegistry, FrontDeskHumanSalesRequestsApi, FrontDeskRoutingApi
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord


class Verifier:
    def verify(self, authorization: str | None) -> IdentityContext:
        return IdentityContext(
            "auth0|user", "human", "https://issuer/", "staging", 1,
            frozenset({"agent.context.read", "platform.front-desk.configure"}),
        )


class Store:
    def __init__(self) -> None:
        self.records: dict[tuple[str, str, str], VersionedRecord] = {}

    def get(self, scope: TenantScope, kind: str, record_ref: str) -> VersionedRecord | None:
        return self.records.get((scope.tenant_ref, kind, record_ref))

    def list(self, scope: TenantScope, kind: str, limit: int = 25) -> list[VersionedRecord]:
        return [
            record
            for (tenant, stored_kind, _), record in self.records.items()
            if tenant == scope.tenant_ref and stored_kind == kind
        ][:limit]

    def save(self, scope: TenantScope, kind: str, record: VersionedRecord) -> None:
        self.records[(scope.tenant_ref, kind, record.record_ref)] = record


class FrontDeskRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = Store()
        scope = TenantScope("tenant-a", "staging", "setup")
        self.store.save(
            scope,
            "conversation",
            VersionedRecord("conversation-a", "v1", {"active_turn_ref": None}),
        )
        self.store.save(
            scope,
            "routing",
            VersionedRecord(
                "destination-a",
                "v1",
                {
                    "record_type": "front_desk_destination",
                    "route_purpose": "support",
                    "destination_type": "support_worker",
                    "channel_scope": ["web_chat"],
                    "lifecycle_state": "active",
                    "health_state": "healthy",
                    "health_expires_at": "2099-01-01T00:00:00+00:00",
                },
            ),
        )
        self.api = FrontDeskRoutingApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (Membership("auth0|user", "tenant-a", "active", frozenset({"agent.context.read"})),)
            ),
            InMemoryAuditSink(),
            self.store,
            ActiveDestinationRegistry(self.store),
            correlation_factory=lambda: "correlation-1",
        )
        self.admin_api = FrontDeskHumanSalesRequestsApi(
            Verifier(),
            InMemoryMembershipDirectory(
                (Membership("auth0|user", "tenant-a", "active", frozenset({"platform.front-desk.configure"})),)
            ),
            InMemoryAuditSink(),
            self.store,
            correlation_factory=lambda: "correlation-2",
        )

    def request(self, payload: dict[str, str]) -> tuple[str, dict[str, object]]:
        captured: dict[str, object] = {}
        raw = json.dumps(payload).encode()
        body = b"".join(
            self.api(
                {
                    "REQUEST_METHOD": "POST",
                    "PATH_INFO": "/v1/conversation-routing-requests",
                    "HTTP_AUTHORIZATION": "Bearer valid",
                    "CONTENT_LENGTH": str(len(raw)),
                    "wsgi.input": BytesIO(raw),
                },
                lambda status, headers: captured.update(status=status),
            )
        )
        return str(captured["status"]), json.loads(body)

    def test_support_request_is_recorded_and_idempotent(self) -> None:
        payload = {"conversation_ref": "conversation-a", "route_purpose": "support", "event_ref": "event-1"}
        status, body = self.request(payload)
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["outcome"], "route_requested")
        replay_status, replay_body = self.request(payload)
        self.assertEqual((replay_status, replay_body), ("200 OK", body))
        self.assertEqual(len(self.store.records), 3)

    def test_human_support_is_safely_unavailable(self) -> None:
        status, body = self.request(
            {"conversation_ref": "conversation-a", "route_purpose": "human_support", "event_ref": "event-2"}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["outcome"], "safe_unavailable")

    def test_human_sales_offer_and_request_are_recorded(self) -> None:
        scope = TenantScope("tenant-a", "staging", "setup")
        self.store.save(scope, "routing", VersionedRecord("sales-a", "v1", {
            "record_type": "front_desk_destination", "route_purpose": "human_sales",
            "destination_type": "human_sales_route", "channel_scope": ["web_chat"],
            "lifecycle_state": "active", "health_state": "healthy",
            "health_expires_at": "2099-01-01T00:00:00+00:00",
        }))
        offer_status, offer = self.request({"conversation_ref": "conversation-a", "route_purpose": "human_sales", "event_ref": "sales-offer", "route_action": "offer"})
        self.assertEqual((offer_status, offer["outcome"]), ("200 OK", "handoff_offered"))
        status, body = self.request({"conversation_ref": "conversation-a", "route_purpose": "human_sales", "event_ref": "sales-request", "route_action": "request", "offer_ref": offer["routing_request_ref"]})
        self.assertEqual((status, body["outcome"]), ("200 OK", "handoff_requested"))

    def test_administrator_can_list_only_recorded_human_sales_requests(self) -> None:
        scope = TenantScope("tenant-a", "staging", "setup")
        self.store.save(scope, "routing", VersionedRecord("sales-a", "v1", {
            "record_type": "front_desk_destination", "route_purpose": "human_sales",
            "destination_type": "human_sales_route", "channel_scope": ["web_chat"],
            "lifecycle_state": "active", "health_state": "healthy",
            "health_expires_at": "2099-01-01T00:00:00+00:00",
        }))
        offer_status, offer = self.request({"conversation_ref": "conversation-a", "route_purpose": "human_sales", "event_ref": "sales-list-offer", "route_action": "offer"})
        self.assertEqual((offer_status, offer["outcome"]), ("200 OK", "handoff_offered"))
        self.request({"conversation_ref": "conversation-a", "route_purpose": "human_sales", "event_ref": "sales-list-request", "route_action": "request", "offer_ref": offer["routing_request_ref"]})
        captured: dict[str, object] = {}
        body = b"".join(self.admin_api(
            {"REQUEST_METHOD": "GET", "PATH_INFO": "/v1/front-desk/human-sales-requests", "HTTP_AUTHORIZATION": "Bearer valid"},
            lambda status, headers: captured.update(status=status),
        ))
        result = json.loads(body)
        self.assertEqual(captured["status"], "200 OK")
        self.assertEqual(result["requests"], [{
            "routing_request_ref": "front-desk:sales-list-request",
            "outcome": "handoff_requested",
            "public_message": "Your request for human sales has been recorded. This does not confirm a salesperson or availability.",
            "review_state": "new",
        }])
        reviewed: dict[str, object] = {}
        review_body = b"".join(self.admin_api(
            {"REQUEST_METHOD": "POST", "PATH_INFO": "/v1/front-desk/human-sales-requests/front-desk:sales-list-request/review", "HTTP_AUTHORIZATION": "Bearer valid"},
            lambda status, headers: reviewed.update(status=status),
        ))
        self.assertEqual(reviewed["status"], "200 OK")
        self.assertEqual(json.loads(review_body)["request"]["review_state"], "reviewed")

    def test_suspended_destination_is_safely_unavailable(self) -> None:
        destination = self.store.records[("tenant-a", "routing", "destination-a")]
        self.store.records[("tenant-a", "routing", "destination-a")] = VersionedRecord(
            destination.record_ref, "v1", {**destination.payload, "lifecycle_state": "suspended"}
        )
        status, body = self.request(
            {"conversation_ref": "conversation-a", "route_purpose": "support", "event_ref": "event-suspended"}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["outcome"], "safe_unavailable")

    def test_expired_destination_is_safely_unavailable(self) -> None:
        destination = self.store.records[("tenant-a", "routing", "destination-a")]
        self.store.records[("tenant-a", "routing", "destination-a")] = VersionedRecord(
            destination.record_ref,
            "v1",
            {**destination.payload, "health_expires_at": "2020-01-01T00:00:00+00:00"},
        )
        status, body = self.request(
            {"conversation_ref": "conversation-a", "route_purpose": "support", "event_ref": "event-expired"}
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["outcome"], "safe_unavailable")

    def test_offer_is_revalidated_before_the_request(self) -> None:
        offer_status, offer = self.request(
            {"conversation_ref": "conversation-a", "route_purpose": "support", "event_ref": "event-offer", "route_action": "offer"}
        )
        self.assertEqual((offer_status, offer["outcome"]), ("200 OK", "route_offered"))
        destination = self.store.records[("tenant-a", "routing", "destination-a")]
        self.store.records[("tenant-a", "routing", "destination-a")] = VersionedRecord(
            destination.record_ref, "v1", {**destination.payload, "lifecycle_state": "withdrawn"}
        )
        status, body = self.request(
            {
                "conversation_ref": "conversation-a",
                "route_purpose": "support",
                "event_ref": "event-request",
                "route_action": "request",
                "offer_ref": offer["routing_request_ref"],
            }
        )
        self.assertEqual(status, "200 OK")
        self.assertEqual(body["outcome"], "safe_unavailable")

    def test_unknown_conversation_cannot_be_routed(self) -> None:
        status, body = self.request(
            {"conversation_ref": "other-tenant-conversation", "route_purpose": "support", "event_ref": "event-3"}
        )
        self.assertEqual((status, body), ("403 Forbidden", {"error": "forbidden"}))

    def test_reusing_an_event_for_a_changed_request_is_a_conflict(self) -> None:
        self.request({"conversation_ref": "conversation-a", "route_purpose": "support", "event_ref": "event-4"})
        status, body = self.request(
            {"conversation_ref": "conversation-a", "route_purpose": "human_support", "event_ref": "event-4"}
        )
        self.assertEqual(status, "409 Conflict")
        self.assertEqual(body["error"], "state_conflict")

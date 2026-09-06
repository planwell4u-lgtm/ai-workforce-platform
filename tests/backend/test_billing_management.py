"""Unit tests for Self-contained Mock SaaS Billing & Usage Metering API."""

from __future__ import annotations

import json
import unittest
from unittest.mock import MagicMock

from ai_workforce_backend.b1 import (
    AuthenticationError,
    AuthorizationError,
    IdentityContext,
    IdentityVerifier,
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_backend.billing_management import BillingManagementApi, PLANS
from ai_workforce_data.postgres_store import (
    TenantInvoiceRecord,
    TenantSubscriptionRecord,
)


class TestBillingManagementApi(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.audit_sink = MagicMock()
        self.store = MagicMock()

        self.api = BillingManagementApi(
            verifier=self.verifier,
            memberships=self.memberships,
            audit_sink=self.audit_sink,
            store=self.store,
            correlation_factory=lambda: "corr-123",
        )

        self.owner_identity = IdentityContext(
            principal_ref="usr-owner-1",
            principal_type="user",
            issuer_ref="auth0",
            environment_ref="staging",
            authenticated_at=1700000000,
            granted_permissions=frozenset({"platform.owner"}),
        )
        self.owner_membership = Membership(
            principal_ref="usr-owner-1",
            tenant_ref="tenant-abc",
            status="active",
            permissions=frozenset({"platform.owner"}),
        )

    def test_get_billing_status_default_free(self) -> None:
        self.verifier.verify.return_value = self.owner_identity
        self.memberships.resolve.return_value = self.owner_membership
        self.store.get_tenant_subscription.return_value = None
        self.store.upsert_tenant_subscription.return_value = TenantSubscriptionRecord(
            subscription_ref="sub-1",
            tenant_ref="tenant-abc",
            tier="free",
            status="active",
            billing_cycle="monthly",
            payment_method_summary="Free Tier",
            current_period_start="2026-09-01T00:00:00Z",
            current_period_end="2026-10-01T00:00:00Z",
            cancel_at_period_end=False,
            updated_at="2026-09-01T00:00:00Z",
        )
        self.store.list_tenant_invoices.return_value = []
        self.store.get_tenant_usage_counts.return_value = {
            "knowledge_articles": 2,
            "conversations": 5,
            "actions_executed": 1,
            "voice_agent_minutes": 15,
        }

        start_response = MagicMock()
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/v1/owner/billing",
            "HTTP_AUTHORIZATION": "Bearer valid-token",
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "200 OK")

        body = json.loads(response[0].decode("utf-8"))
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["subscription"]["tier"], "free")
        self.assertEqual(body["usage"]["metrics"]["knowledge_articles"], 2)
        self.assertEqual(body["usage"]["limits"]["knowledge_articles"], 10)

    def test_post_checkout_success(self) -> None:
        self.verifier.verify.return_value = self.owner_identity
        self.memberships.resolve.return_value = self.owner_membership
        self.store.record_tenant_invoice.return_value = TenantInvoiceRecord(
            invoice_ref="inv-123",
            tenant_ref="tenant-abc",
            amount_cents=4900,
            currency="usd",
            status="paid",
            tier="starter",
            description="Planwell Starter Plan (Monthly)",
            pdf_receipt_ref="rec_inv-123",
            created_at="2026-09-05T12:00:00Z",
        )
        self.store.upsert_tenant_subscription.return_value = TenantSubscriptionRecord(
            subscription_ref="sub-starter-1",
            tenant_ref="tenant-abc",
            tier="starter",
            status="active",
            billing_cycle="monthly",
            payment_method_summary="Visa ending in 4242",
            current_period_start="2026-09-05T12:00:00Z",
            current_period_end="2026-10-05T12:00:00Z",
            cancel_at_period_end=False,
            updated_at="2026-09-05T12:00:00Z",
        )

        start_response = MagicMock()
        payload = json.dumps({
            "action": "checkout",
            "tier": "starter",
            "billing_cycle": "monthly",
            "card_number": "4242 4242 4242 4242",
            "card_brand": "Visa",
        }).encode("utf-8")

        import io
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/v1/owner/billing",
            "HTTP_AUTHORIZATION": "Bearer valid-token",
            "CONTENT_LENGTH": str(len(payload)),
            "wsgi.input": io.BytesIO(payload),
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "200 OK")

        body = json.loads(response[0].decode("utf-8"))
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["subscription"]["tier"], "starter")
        self.audit_sink.record.assert_called_once()

    def test_post_checkout_declined_card(self) -> None:
        self.verifier.verify.return_value = self.owner_identity
        self.memberships.resolve.return_value = self.owner_membership

        start_response = MagicMock()
        payload = json.dumps({
            "action": "checkout",
            "tier": "pro",
            "card_number": "4000 0000 0000 0002",
        }).encode("utf-8")

        import io
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/v1/owner/billing",
            "HTTP_AUTHORIZATION": "Bearer valid-token",
            "CONTENT_LENGTH": str(len(payload)),
            "wsgi.input": io.BytesIO(payload),
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "400 Bad Request")

        body = json.loads(response[0].decode("utf-8"))
        self.assertEqual(body["error"], "card_declined")

    def test_post_cancel_and_resume(self) -> None:
        self.verifier.verify.return_value = self.owner_identity
        self.memberships.resolve.return_value = self.owner_membership
        self.store.get_tenant_subscription.return_value = TenantSubscriptionRecord(
            subscription_ref="sub-1",
            tenant_ref="tenant-abc",
            tier="starter",
            status="active",
            billing_cycle="monthly",
            payment_method_summary="Visa ending in 4242",
            current_period_start="2026-09-01T00:00:00Z",
            current_period_end="2026-10-01T00:00:00Z",
            cancel_at_period_end=False,
            updated_at="2026-09-01T00:00:00Z",
        )
        self.store.upsert_tenant_subscription.return_value = TenantSubscriptionRecord(
            subscription_ref="sub-1",
            tenant_ref="tenant-abc",
            tier="starter",
            status="active",
            billing_cycle="monthly",
            payment_method_summary="Visa ending in 4242",
            current_period_start="2026-09-01T00:00:00Z",
            current_period_end="2026-10-01T00:00:00Z",
            cancel_at_period_end=True,
            updated_at="2026-09-05T12:00:00Z",
        )

        start_response = MagicMock()
        payload = json.dumps({"action": "cancel"}).encode("utf-8")

        import io
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/v1/owner/billing",
            "HTTP_AUTHORIZATION": "Bearer valid-token",
            "CONTENT_LENGTH": str(len(payload)),
            "wsgi.input": io.BytesIO(payload),
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "200 OK")
        body = json.loads(response[0].decode("utf-8"))
        self.assertEqual(body["action"], "canceled")

    def test_unauthorized_user_denied(self) -> None:
        self.verifier.verify.return_value = IdentityContext(
            principal_ref="usr-reader",
            principal_type="user",
            issuer_ref="auth0",
            environment_ref="staging",
            authenticated_at=1700000000,
            granted_permissions=frozenset({"agent.context.read"}),
        )
        self.memberships.resolve.return_value = Membership(
            principal_ref="usr-reader",
            tenant_ref="tenant-abc",
            status="active",
            permissions=frozenset({"agent.context.read"}),
        )

        start_response = MagicMock()
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/v1/owner/billing",
            "HTTP_AUTHORIZATION": "Bearer valid-token",
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "403 Forbidden")


if __name__ == "__main__":
    unittest.main()

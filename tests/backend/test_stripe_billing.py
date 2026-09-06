"""Unit tests for Stripe Billing Service and Feature-Gated API Integration."""

from __future__ import annotations

import io
import json
import unittest
from unittest.mock import MagicMock, patch

from ai_workforce_backend.b1 import (
    IdentityContext,
    Membership,
)
from ai_workforce_backend.billing_management import BillingManagementApi
from ai_workforce_backend.stripe_billing import StripeBillingService
from ai_workforce_data.postgres_store import (
    TenantInvoiceRecord,
    TenantSubscriptionRecord,
)


class TestStripeBillingService(unittest.TestCase):
    def setUp(self) -> None:
        self.store = MagicMock()

    def test_disabled_by_default(self) -> None:
        service = StripeBillingService(store=self.store, enabled=False)
        self.assertFalse(service.is_enabled)
        with self.assertRaises(RuntimeError) as ctx:
            service.create_checkout_session(
                tenant_ref="tenant-123",
                tier="pro",
                success_url="https://example.com/success",
                cancel_url="https://example.com/cancel",
            )
        self.assertIn("stripe_disabled", str(ctx.exception))

    def test_disabled_portal_session(self) -> None:
        service = StripeBillingService(store=self.store, enabled=False)
        self.assertFalse(service.is_enabled)
        with self.assertRaises(RuntimeError) as ctx:
            service.create_portal_session(
                stripe_customer_id="cus_123",
                return_url="https://example.com",
            )
        self.assertIn("stripe_disabled", str(ctx.exception))

    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session_when_enabled(self, mock_session_create: MagicMock) -> None:
        mock_session_create.return_value = MagicMock(id="cs_test_123", url="https://checkout.stripe.com/c/pay/cs_test_123")
        self.store.get_tenant_subscription.return_value = None

        service = StripeBillingService(
            store=self.store,
            secret_key="sk_test_12345",
            webhook_secret="whsec_12345",
            enabled=True,
        )
        self.assertTrue(service.is_enabled)

        res = service.create_checkout_session(
            tenant_ref="tenant-xyz",
            tier="pro",
            billing_cycle="monthly",
            success_url="https://planwell.online/success",
            cancel_url="https://planwell.online/cancel",
            customer_email="owner@test.com",
        )

        self.assertEqual(res["session_id"], "cs_test_123")
        self.assertEqual(res["checkout_url"], "https://checkout.stripe.com/c/pay/cs_test_123")
        mock_session_create.assert_called_once()

    @patch("stripe.Webhook.construct_event")
    def test_handle_webhook_checkout_completed(self, mock_construct: MagicMock) -> None:
        mock_construct.return_value = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "client_reference_id": "tenant-abc",
                    "customer": "cus_999",
                    "subscription": "sub_stripe_111",
                    "metadata": {"tier": "pro", "billing_cycle": "monthly"},
                }
            },
        }

        service = StripeBillingService(
            store=self.store,
            secret_key="sk_test_12345",
            webhook_secret="whsec_12345",
            enabled=True,
        )

        res = service.handle_webhook(payload=b'{"test": 1}', signature_header="t=123,v1=abc")
        self.assertTrue(res["received"])
        self.assertEqual(res["event_type"], "checkout.session.completed")
        self.store.upsert_tenant_subscription.assert_called_once()


class TestBillingManagementApiStripeIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.audit_sink = MagicMock()
        self.store = MagicMock()
        self.stripe_service = MagicMock()

        self.api = BillingManagementApi(
            verifier=self.verifier,
            memberships=self.memberships,
            audit_sink=self.audit_sink,
            store=self.store,
            stripe_service=self.stripe_service,
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

    def test_stripe_checkout_blocked_when_disabled(self) -> None:
        self.verifier.verify.return_value = self.owner_identity
        self.memberships.resolve.return_value = self.owner_membership
        self.stripe_service.is_enabled = False

        start_response = MagicMock()
        payload = json.dumps({"action": "stripe_checkout", "tier": "pro"}).encode("utf-8")
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
        self.assertEqual(body["error"], "stripe_disabled")

    def test_stripe_webhook_direct_dispatch(self) -> None:
        self.stripe_service.handle_webhook.return_value = {"received": True, "event_type": "invoice.payment_succeeded"}

        start_response = MagicMock()
        raw_body = b'{"id": "evt_test"}'
        environ = {
            "REQUEST_METHOD": "POST",
            "PATH_INFO": "/v1/owner/billing/stripe/webhook",
            "HTTP_STRIPE_SIGNATURE": "t=1,v1=sig",
            "CONTENT_LENGTH": str(len(raw_body)),
            "wsgi.input": io.BytesIO(raw_body),
        }

        response = self.api(environ, start_response)
        start_response.assert_called_once()
        status = start_response.call_args[0][0]
        self.assertEqual(status, "200 OK")

        body = json.loads(response[0].decode("utf-8"))
        self.assertTrue(body["received"])
        self.stripe_service.handle_webhook.assert_called_once_with(payload=raw_body, signature_header="t=1,v1=sig")

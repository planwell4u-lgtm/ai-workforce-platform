"""Production-ready Stripe Billing Service with dormant feature-flag toggle."""

from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from ai_workforce_data.postgres_store import PostgresTenantStore

logger = logging.getLogger(__name__)

try:
    import stripe
except ImportError:
    stripe = None  # type: ignore[assignment]


class StripeBillingService:
    """Production-ready Stripe Billing integration.
    
    Can be dynamically toggled via STRIPE_ENABLED env var (default: False).
    When disabled, safely rejects checkout/portal calls without crashing.
    """

    def __init__(
        self,
        store: PostgresTenantStore,
        secret_key: str | None = None,
        webhook_secret: str | None = None,
        enabled: bool | None = None,
    ) -> None:
        self._store = store
        self._secret_key = secret_key or os.environ.get("STRIPE_SECRET_KEY", "").strip()
        self._webhook_secret = webhook_secret or os.environ.get("STRIPE_WEBHOOK_SECRET", "").strip()
        
        if enabled is not None:
            self._enabled = enabled
        else:
            self._enabled = os.environ.get("STRIPE_ENABLED", "false").lower() in ("true", "1", "yes")

        if stripe and self._secret_key:
            stripe.api_key = self._secret_key

    @property
    def is_enabled(self) -> bool:
        """Returns True if Stripe is explicitly enabled and API key is present."""
        return self._enabled and bool(self._secret_key) and (stripe is not None)

    def create_checkout_session(
        self,
        *,
        tenant_ref: str,
        tier: str,
        billing_cycle: str = "monthly",
        success_url: str,
        cancel_url: str,
        customer_email: str | None = None,
    ) -> dict[str, str]:
        """Creates a Stripe Checkout Session for subscription checkout."""
        if not self.is_enabled:
            raise RuntimeError("stripe_disabled: Stripe billing is currently dormant or unconfigured.")

        if not stripe:
            raise RuntimeError("stripe_missing: Stripe Python package is not installed.")

        # Price catalog mapping in cents
        price_cents = {
            "starter": 4900,
            "pro": 19900,
            "enterprise": 49900,
        }.get(tier.lower(), 4900)

        interval = "year" if billing_cycle.lower() == "annual" else "month"
        if interval == "year":
            price_cents = int(price_cents * 10)  # 2 months free discount

        session_params: dict[str, Any] = {
            "payment_method_types": ["card"],
            "mode": "subscription",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "client_reference_id": tenant_ref,
            "metadata": {
                "tenant_ref": tenant_ref,
                "tier": tier,
                "billing_cycle": billing_cycle,
            },
            "line_items": [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Planwell {tier.capitalize()} Plan",
                            "description": f"Planwell AI Workforce {tier.capitalize()} Subscription ({billing_cycle.capitalize()})",
                        },
                        "unit_amount": price_cents,
                        "recurring": {
                            "interval": interval,
                        },
                    },
                    "quantity": 1,
                }
            ],
        }

        if customer_email:
            session_params["customer_email"] = customer_email

        # Check if customer already has a Stripe customer ID
        existing_sub = self._store.get_tenant_subscription(tenant_ref)
        if existing_sub and existing_sub.stripe_customer_id:
            session_params["customer"] = existing_sub.stripe_customer_id
            session_params.pop("customer_email", None)

        session = stripe.checkout.Session.create(**session_params)
        return {
            "session_id": session.id,
            "checkout_url": session.url,
        }

    def create_portal_session(
        self,
        *,
        stripe_customer_id: str,
        return_url: str,
    ) -> dict[str, str]:
        """Creates a Stripe Customer Portal session for managing payment methods & billing details."""
        if not self.is_enabled:
            raise RuntimeError("stripe_disabled: Stripe billing is currently dormant or unconfigured.")

        if not stripe:
            raise RuntimeError("stripe_missing: Stripe Python package is not installed.")

        portal = stripe.billing_portal.Session.create(
            customer=stripe_customer_id,
            return_url=return_url,
        )
        return {
            "portal_url": portal.url,
        }

    def handle_webhook(
        self,
        *,
        payload: bytes,
        signature_header: str,
    ) -> dict[str, object]:
        """Verifies Stripe webhook signature and synchronizes PostgreSQL state."""
        if not stripe:
            raise RuntimeError("stripe_missing: Stripe Python package is not installed.")

        if not self._webhook_secret:
            raise RuntimeError("webhook_secret_missing: STRIPE_WEBHOOK_SECRET is not configured.")

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=signature_header,
                secret=self._webhook_secret,
            )
        except Exception as err:
            logger.warning("Stripe webhook signature verification failed: %s", err)
            raise ValueError(f"invalid_webhook_signature: {err}") from err

        event_type = event.get("type", "")
        data_object = event.get("data", {}).get("object", {})

        logger.info("Processing Stripe webhook event: %s", event_type)

        if event_type == "checkout.session.completed":
            self._on_checkout_completed(data_object)
        elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
            self._on_subscription_updated(data_object)
        elif event_type == "customer.subscription.deleted":
            self._on_subscription_deleted(data_object)
        elif event_type == "invoice.payment_succeeded":
            self._on_invoice_payment_succeeded(data_object)

        return {"received": True, "event_type": event_type}

    def _on_checkout_completed(self, session: dict[str, Any]) -> None:
        tenant_ref = session.get("client_reference_id") or session.get("metadata", {}).get("tenant_ref")
        tier = session.get("metadata", {}).get("tier", "starter")
        billing_cycle = session.get("metadata", {}).get("billing_cycle", "monthly")
        stripe_customer_id = session.get("customer")
        stripe_subscription_id = session.get("subscription")

        if not tenant_ref:
            logger.warning("Stripe checkout completed without tenant_ref metadata.")
            return

        self._store.upsert_tenant_subscription(
            subscription_ref=str(uuid.uuid4()),
            tenant_ref=tenant_ref,
            tier=tier,
            status="active",
            billing_cycle=billing_cycle,
            payment_method_summary="Stripe Card Payment",
            provider="stripe",
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
            cancel_at_period_end=False,
        )

    def _on_subscription_updated(self, sub: dict[str, Any]) -> None:
        stripe_sub_id = sub.get("id")
        stripe_customer_id = sub.get("customer")
        status = sub.get("status", "active")
        cancel_at_period_end = bool(sub.get("cancel_at_period_end", False))

        existing = self._store.get_tenant_subscription_by_stripe_customer(stripe_customer_id)
        if not existing:
            logger.warning("No tenant subscription matching Stripe customer: %s", stripe_customer_id)
            return

        self._store.upsert_tenant_subscription(
            subscription_ref=existing.subscription_ref,
            tenant_ref=existing.tenant_ref,
            tier=existing.tier,
            status="active" if status in ("active", "trialing") else status,
            billing_cycle=existing.billing_cycle,
            payment_method_summary=existing.payment_method_summary or "Stripe Subscription",
            provider="stripe",
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_sub_id,
            cancel_at_period_end=cancel_at_period_end,
        )

    def _on_subscription_deleted(self, sub: dict[str, Any]) -> None:
        stripe_customer_id = sub.get("customer")
        existing = self._store.get_tenant_subscription_by_stripe_customer(stripe_customer_id)
        if not existing:
            return

        self._store.upsert_tenant_subscription(
            subscription_ref=existing.subscription_ref,
            tenant_ref=existing.tenant_ref,
            tier="free",
            status="canceled",
            billing_cycle=existing.billing_cycle,
            payment_method_summary="Free Tier",
            provider="stripe",
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=None,
            cancel_at_period_end=False,
        )

    def _on_invoice_payment_succeeded(self, invoice: dict[str, Any]) -> None:
        stripe_customer_id = invoice.get("customer")
        stripe_inv_id = invoice.get("id")
        amount_paid = invoice.get("amount_paid", 0)
        currency = invoice.get("currency", "usd")
        hosted_url = invoice.get("hosted_invoice_url")

        existing = self._store.get_tenant_subscription_by_stripe_customer(stripe_customer_id)
        if not existing:
            return

        self._store.record_tenant_invoice(
            invoice_ref=str(uuid.uuid4()),
            tenant_ref=existing.tenant_ref,
            amount_cents=amount_paid,
            currency=currency,
            status="paid",
            tier=existing.tier,
            description=f"Stripe Recurring Payment - {existing.tier.capitalize()} Plan",
            pdf_receipt_ref=invoice.get("invoice_pdf"),
            provider="stripe",
            stripe_invoice_id=stripe_inv_id,
            stripe_hosted_invoice_url=hosted_url,
        )

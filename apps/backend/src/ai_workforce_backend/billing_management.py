"""Self-contained Mock SaaS Billing & Usage Metering API."""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Mapping
from typing import Callable, cast

from ai_workforce_backend.b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)
from ai_workforce_backend.stripe_billing import StripeBillingService
from ai_workforce_data.postgres_store import PostgresTenantStore

PLANS = {
    "free": {
        "id": "free",
        "name": "Free Tier",
        "price_cents": 0,
        "price_monthly": 0,
        "limits": {
            "voice_agent_minutes": 60,
            "knowledge_articles": 10,
            "actions_executed": 5,
        },
        "features": [
            "60 Agent Minutes / month",
            "Up to 10 Knowledge Articles",
            "5 Jira Escalations",
            "Single Workspace Owner",
            "Standard Community Support",
        ],
    },
    "starter": {
        "id": "starter",
        "name": "Starter",
        "price_cents": 4900,
        "price_monthly": 49,
        "limits": {
            "voice_agent_minutes": 500,
            "knowledge_articles": 50,
            "actions_executed": 50,
        },
        "features": [
            "500 Agent Minutes / month",
            "Up to 50 Knowledge Articles",
            "50 Jira Escalations",
            "Multiple Workspace Owners",
            "Live Voice & Web-Chat AI",
            "Standard Email Support",
        ],
    },
    "pro": {
        "id": "pro",
        "name": "Pro",
        "price_cents": 19900,
        "price_monthly": 199,
        "limits": {
            "voice_agent_minutes": 2500,
            "knowledge_articles": 250,
            "actions_executed": 250,
        },
        "features": [
            "2,500 Agent Minutes / month",
            "Up to 250 Knowledge Articles",
            "250 Jira Escalations",
            "Dedicated Support Routing",
            "Priority Audit Log Retention",
            "24/7 Priority Support",
        ],
    },
    "enterprise": {
        "id": "enterprise",
        "name": "Enterprise",
        "price_cents": 49900,
        "price_monthly": 499,
        "limits": {
            "voice_agent_minutes": 10000,
            "knowledge_articles": 1000,
            "actions_executed": 1000,
        },
        "features": [
            "10,000 Agent Minutes / month",
            "Up to 1,000 Knowledge Articles",
            "1,000 Jira Escalations",
            "Custom SLA & Guaranteed Uptime",
            "Dedicated Account Manager",
            "Custom LiveKit & Voice Workpools",
        ],
    },
}


class BillingManagementApi:
    """Mock SaaS Billing & Usage Metering API."""

    path = "/v1/owner/billing"
    route_ref = "platform.billing.v1"
    required_permissions = frozenset({"platform.owner", "platform.front-desk.configure"})

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        audit_sink: AuditSink,
        store: PostgresTenantStore,
        stripe_service: StripeBillingService | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._audit_sink = audit_sink
        self._store = store
        self._stripe_service = stripe_service
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        headers = [
            ("Content-Type", "application/json"),
            ("X-Correlation-Id", correlation_ref),
        ]

        method = environ.get("REQUEST_METHOD")
        path_info = str(environ.get("PATH_INFO", "")).rstrip("/")

        # Direct Stripe Webhook handling (Signature-based auth instead of Bearer token)
        if path_info.endswith("/stripe/webhook") or environ.get("HTTP_STRIPE_SIGNATURE"):
            if not self._stripe_service:
                return self._respond(
                    start_response, "503 Service Unavailable", headers, {"error": "stripe_service_unconfigured"}
                )
            sig_header = str(environ.get("HTTP_STRIPE_SIGNATURE", ""))
            try:
                raw_body = self._read_raw(environ)
                res = self._stripe_service.handle_webhook(payload=raw_body, signature_header=sig_header)
                return self._respond(start_response, "200 OK", headers, res)
            except ValueError as val_err:
                return self._respond(
                    start_response, "400 Bad Request", headers, {"error": "invalid_signature", "message": str(val_err)}
                )
            except Exception as err:
                return self._respond(
                    start_response, "500 Internal Server Error", headers, {"error": "webhook_error", "message": str(err)}
                )

        identity = None
        membership = None

        try:
            identity = self._verifier.verify(
                cast(str | None, environ.get("HTTP_AUTHORIZATION"))
            )
            membership = self._memberships.resolve(identity.principal_ref)

            permissions = identity.granted_permissions | membership.permissions
            if not (self.required_permissions & permissions):
                raise AuthorizationError("insufficient_permission")

            tenant_ref = membership.tenant_ref

            if method == "GET":
                sub = self._store.get_tenant_subscription(tenant_ref)
                if not sub:
                    sub = self._store.upsert_tenant_subscription(
                        subscription_ref=str(uuid.uuid4()),
                        tenant_ref=tenant_ref,
                        tier="free",
                        status="active",
                        billing_cycle="monthly",
                        payment_method_summary="Free Tier",
                    )

                invoices = self._store.list_tenant_invoices(tenant_ref)
                usage = self._store.get_tenant_usage_counts(tenant_ref)
                plan_limits = PLANS.get(sub.tier, PLANS["free"])["limits"]
                stripe_active = bool(self._stripe_service and self._stripe_service.is_enabled)

                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {
                        "status": "ok",
                        "tenant_ref": tenant_ref,
                        "billing_mode": "stripe" if stripe_active else "mock",
                        "stripe_enabled": stripe_active,
                        "subscription": {
                            "subscription_ref": sub.subscription_ref,
                            "tier": sub.tier,
                            "status": sub.status,
                            "billing_cycle": sub.billing_cycle,
                            "payment_method_summary": sub.payment_method_summary,
                            "provider": sub.provider,
                            "stripe_customer_id": sub.stripe_customer_id,
                            "stripe_subscription_id": sub.stripe_subscription_id,
                            "current_period_start": sub.current_period_start,
                            "current_period_end": sub.current_period_end,
                            "cancel_at_period_end": sub.cancel_at_period_end,
                            "updated_at": sub.updated_at,
                        },
                        "plans": PLANS,
                        "usage": {
                            "metrics": usage,
                            "limits": plan_limits,
                        },
                        "invoices": [
                            {
                                "invoice_ref": inv.invoice_ref,
                                "amount_cents": inv.amount_cents,
                                "currency": inv.currency,
                                "status": inv.status,
                                "tier": inv.tier,
                                "description": inv.description,
                                "pdf_receipt_ref": inv.pdf_receipt_ref,
                                "provider": inv.provider,
                                "stripe_invoice_id": inv.stripe_invoice_id,
                                "stripe_hosted_invoice_url": inv.stripe_hosted_invoice_url,
                                "created_at": inv.created_at,
                            }
                            for inv in invoices
                        ],
                    },
                )

            if method == "POST":
                body = self._read_json(environ)
                action = body.get("action", "checkout")

                if action == "stripe_checkout":
                    if not self._stripe_service or not self._stripe_service.is_enabled:
                        return self._respond(
                            start_response,
                            "400 Bad Request",
                            headers,
                            {
                                "error": "stripe_disabled",
                                "message": "Stripe billing is currently dormant. Toggle STRIPE_ENABLED=true in environment to activate.",
                            },
                        )
                    target_tier = str(body.get("tier", "starter")).lower().strip()
                    billing_cycle = str(body.get("billing_cycle", "monthly")).lower().strip()
                    success_url = str(body.get("success_url", "https://planwell.online/local-management?billing=success"))
                    cancel_url = str(body.get("cancel_url", "https://planwell.online/local-management?billing=cancel"))
                    customer_email = str(body.get("customer_email", "")) if body.get("customer_email") else None

                    checkout_res = self._stripe_service.create_checkout_session(
                        tenant_ref=tenant_ref,
                        tier=target_tier,
                        billing_cycle=billing_cycle,
                        success_url=success_url,
                        cancel_url=cancel_url,
                        customer_email=customer_email,
                    )
                    return self._respond(start_response, "200 OK", headers, {"status": "ok", **checkout_res})

                if action == "stripe_portal":
                    if not self._stripe_service or not self._stripe_service.is_enabled:
                        return self._respond(
                            start_response,
                            "400 Bad Request",
                            headers,
                            {
                                "error": "stripe_disabled",
                                "message": "Stripe customer portal is currently dormant.",
                            },
                        )
                    sub = self._store.get_tenant_subscription(tenant_ref)
                    if not sub or not sub.stripe_customer_id:
                        return self._respond(
                            start_response,
                            "400 Bad Request",
                            headers,
                            {"error": "no_stripe_customer", "message": "No active Stripe customer found for this tenant."},
                        )
                    return_url = str(body.get("return_url", "https://planwell.online/local-management"))
                    portal_res = self._stripe_service.create_portal_session(
                        stripe_customer_id=sub.stripe_customer_id,
                        return_url=return_url,
                    )
                    return self._respond(start_response, "200 OK", headers, {"status": "ok", **portal_res})

                if action == "cancel":
                    sub = self._store.upsert_tenant_subscription(
                        subscription_ref=str(uuid.uuid4()),
                        tenant_ref=tenant_ref,
                        tier=(self._store.get_tenant_subscription(tenant_ref).tier if self._store.get_tenant_subscription(tenant_ref) else "starter"),
                        status="active",
                        cancel_at_period_end=True,
                    )
                    self._record_audit(
                        correlation_ref,
                        "allowed",
                        "subscription_canceled_at_period_end",
                        identity.principal_ref,
                        tenant_ref,
                    )
                    return self._respond(
                        start_response,
                        "200 OK",
                        headers,
                        {
                            "status": "ok",
                            "action": "canceled",
                            "subscription": {
                                "subscription_ref": sub.subscription_ref,
                                "tier": sub.tier,
                                "status": sub.status,
                                "billing_cycle": sub.billing_cycle,
                                "payment_method_summary": sub.payment_method_summary,
                                "current_period_start": sub.current_period_start,
                                "current_period_end": sub.current_period_end,
                                "cancel_at_period_end": sub.cancel_at_period_end,
                                "updated_at": sub.updated_at,
                            },
                        },
                    )

                if action == "resume":
                    current_sub = self._store.get_tenant_subscription(tenant_ref)
                    tier = current_sub.tier if current_sub else "starter"
                    sub = self._store.upsert_tenant_subscription(
                        subscription_ref=str(uuid.uuid4()),
                        tenant_ref=tenant_ref,
                        tier=tier,
                        status="active",
                        cancel_at_period_end=False,
                    )
                    self._record_audit(
                        correlation_ref,
                        "allowed",
                        "subscription_resumed",
                        identity.principal_ref,
                        tenant_ref,
                    )
                    return self._respond(
                        start_response,
                        "200 OK",
                        headers,
                        {
                            "status": "ok",
                            "action": "resumed",
                            "subscription": {
                                "subscription_ref": sub.subscription_ref,
                                "tier": sub.tier,
                                "status": sub.status,
                                "billing_cycle": sub.billing_cycle,
                                "payment_method_summary": sub.payment_method_summary,
                                "current_period_start": sub.current_period_start,
                                "current_period_end": sub.current_period_end,
                                "cancel_at_period_end": sub.cancel_at_period_end,
                                "updated_at": sub.updated_at,
                            },
                        },
                    )

                # Default: checkout / subscribe / change tier
                target_tier = str(body.get("tier", "starter")).lower().strip()
                if target_tier not in PLANS:
                    return self._respond(
                        start_response,
                        "400 Bad Request",
                        headers,
                        {"error": "invalid_plan_tier", "message": f"Plan '{target_tier}' does not exist."},
                    )

                billing_cycle = str(body.get("billing_cycle", "monthly")).lower().strip()
                card_number = str(body.get("card_number", "4242424242424242")).replace(" ", "").replace("-", "")

                # Simulated test card error validation
                if card_number.endswith("0002"):
                    return self._respond(
                        start_response,
                        "400 Bad Request",
                        headers,
                        {"error": "card_declined", "message": "The simulated card was declined."},
                    )
                if card_number.endswith("9995"):
                    return self._respond(
                        start_response,
                        "400 Bad Request",
                        headers,
                        {"error": "insufficient_funds", "message": "The simulated card has insufficient funds."},
                    )
                if card_number.endswith("0069"):
                    return self._respond(
                        start_response,
                        "400 Bad Request",
                        headers,
                        {"error": "expired_card", "message": "The simulated card has expired."},
                    )

                last4 = card_number[-4:] if len(card_number) >= 4 else "4242"
                card_brand = str(body.get("card_brand", "Visa")).capitalize()
                pm_summary = f"{card_brand} ending in {last4}"

                plan_info = PLANS[target_tier]
                amount_cents = plan_info["price_cents"]
                if billing_cycle == "annual":
                    amount_cents = int(amount_cents * 10)  # 2 months free

                invoice_ref = str(uuid.uuid4())
                description = f"Planwell {plan_info['name']} Plan ({billing_cycle.capitalize()})"
                receipt_ref = f"rec_{invoice_ref[:8]}"

                # Record Invoice
                invoice = self._store.record_tenant_invoice(
                    invoice_ref=invoice_ref,
                    tenant_ref=tenant_ref,
                    amount_cents=amount_cents,
                    currency="usd",
                    status="paid",
                    tier=target_tier,
                    description=description,
                    pdf_receipt_ref=receipt_ref,
                )

                # Upsert Subscription
                sub = self._store.upsert_tenant_subscription(
                    subscription_ref=str(uuid.uuid4()),
                    tenant_ref=tenant_ref,
                    tier=target_tier,
                    status="active",
                    billing_cycle=billing_cycle,
                    payment_method_summary=pm_summary,
                    cancel_at_period_end=False,
                )

                self._record_audit(
                    correlation_ref,
                    "allowed",
                    f"subscription_updated:{target_tier}:{amount_cents}",
                    identity.principal_ref,
                    tenant_ref,
                )

                return self._respond(
                    start_response,
                    "200 OK",
                    headers,
                    {
                        "status": "ok",
                        "message": f"Successfully subscribed to {plan_info['name']}.",
                        "subscription": {
                            "subscription_ref": sub.subscription_ref,
                            "tier": sub.tier,
                            "status": sub.status,
                            "billing_cycle": sub.billing_cycle,
                            "payment_method_summary": sub.payment_method_summary,
                            "current_period_start": sub.current_period_start,
                            "current_period_end": sub.current_period_end,
                            "cancel_at_period_end": sub.cancel_at_period_end,
                            "updated_at": sub.updated_at,
                        },
                        "invoice": {
                            "invoice_ref": invoice.invoice_ref,
                            "amount_cents": invoice.amount_cents,
                            "currency": invoice.currency,
                            "status": invoice.status,
                            "tier": invoice.tier,
                            "description": invoice.description,
                            "pdf_receipt_ref": invoice.pdf_receipt_ref,
                            "created_at": invoice.created_at,
                        },
                    },
                )

            return self._respond(
                start_response, "405 Method Not Allowed", headers, {"error": "method_not_allowed"}
            )

        except AuthenticationError:
            return self._respond(
                start_response, "401 Unauthorized", headers, {"error": "unauthorized"}
            )
        except AuthorizationError:
            try:
                self._record_audit(
                    correlation_ref,
                    "denied",
                    "forbidden",
                    identity.principal_ref if identity else None,
                    membership.tenant_ref if membership else None,
                )
            except Exception:
                pass
            return self._respond(
                start_response, "403 Forbidden", headers, {"error": "forbidden"}
            )
        except Exception as error:
            try:
                self._record_audit(
                    correlation_ref,
                    "denied",
                    f"internal_error:{error}",
                    identity.principal_ref if identity else None,
                    membership.tenant_ref if membership else None,
                )
            except Exception:
                pass
            return self._respond(
                start_response,
                "500 Internal Server Error",
                headers,
                {"error": "internal_error", "message": str(error)},
            )

    def _record_audit(
        self,
        correlation_ref: str,
        decision: str,
        reason: str,
        principal_ref: str | None,
        tenant_ref: str | None,
    ) -> None:
        self._audit_sink.record(
            AuditEvent(
                outcome="allowed" if decision == "allowed" else "denied",
                reason=reason,
                correlation_ref=correlation_ref,
                route_ref=self.route_ref,
                principal_ref=principal_ref,
                tenant_ref=tenant_ref,
            )
        )

    @staticmethod
    def _read_raw(environ: Mapping[str, object]) -> bytes:
        try:
            length = int(str(environ.get("CONTENT_LENGTH") or 0))
        except (ValueError, TypeError):
            length = 0
        stream = environ.get("wsgi.input")
        if not stream or length <= 0:
            return b""
        try:
            return stream.read(length) or b""  # type: ignore[union-attr]
        except Exception:
            return b""

    @staticmethod
    def _read_json(environ: Mapping[str, object]) -> dict[str, object]:
        try:
            length = int(str(environ.get("CONTENT_LENGTH") or 0))
        except (ValueError, TypeError):
            length = 0
        stream = environ.get("wsgi.input")
        if not stream or length <= 0:
            return {}
        try:
            data = stream.read(length)  # type: ignore[union-attr]
            return json.loads(data.decode("utf-8")) if data else {}
        except Exception:
            return {}

    @staticmethod
    def _respond(
        start_response: Callable[..., object],
        status: str,
        headers: list[tuple[str, str]],
        body: dict[str, object],
    ) -> list[bytes]:
        payload = json.dumps(body).encode("utf-8")
        headers.append(("Content-Length", str(len(payload))))
        start_response(status, headers)
        return [payload]

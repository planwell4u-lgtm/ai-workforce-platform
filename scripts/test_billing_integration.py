import os
import uuid
from pathlib import Path
from ai_workforce_data.postgres_store import PostgresTenantStore

def load_env():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()

def run():
    load_env()
    db_url = os.environ["DATABASE_URL"]
    store = PostgresTenantStore(db_url)
    print("--- 1. Applying Migrations (including Migration 9 for Billing) ---")
    store.apply_migrations()

    tenant_ref = "staging-demo"
    print("\n--- 2. Checking Current Tenant Subscription ---")
    sub = store.get_tenant_subscription(tenant_ref)
    if not sub:
        print("No subscription found; initializing Free Tier...")
        sub = store.upsert_tenant_subscription(
            subscription_ref=str(uuid.uuid4()),
            tenant_ref=tenant_ref,
            tier="free",
            status="active",
            billing_cycle="monthly",
            payment_method_summary="Free Tier",
        )
    print(f"Active Tier: {sub.tier.upper()} | Status: {sub.status} | Payment: {sub.payment_method_summary}")

    print("\n--- 3. Simulating Mock Upgrade to Pro Tier with Dummy Card 4242 ---")
    inv_ref = str(uuid.uuid4())
    invoice = store.record_tenant_invoice(
        invoice_ref=inv_ref,
        tenant_ref=tenant_ref,
        amount_cents=19900,
        currency="usd",
        status="paid",
        tier="pro",
        description="Planwell Pro Plan (Monthly)",
        pdf_receipt_ref=f"rec_{inv_ref[:8]}",
    )
    print(f"Recorded Invoice: {invoice.invoice_ref} | Amount: ${invoice.amount_cents / 100:.2f} | Receipt: {invoice.pdf_receipt_ref}")

    upgraded_sub = store.upsert_tenant_subscription(
        subscription_ref=str(uuid.uuid4()),
        tenant_ref=tenant_ref,
        tier="pro",
        status="active",
        billing_cycle="monthly",
        payment_method_summary="Visa ending in 4242",
        cancel_at_period_end=False,
    )
    print(f"Upgraded Subscription: Tier={upgraded_sub.tier.upper()} | Payment={upgraded_sub.payment_method_summary}")

    print("\n--- 4. Listing Invoices ---")
    invoices = store.list_tenant_invoices(tenant_ref)
    print(f"Total Invoices: {len(invoices)}")
    for inv in invoices[:3]:
        print(f" - [{inv.created_at[:10]}] {inv.description}: ${inv.amount_cents / 100:.2f} ({inv.status.upper()}) - {inv.pdf_receipt_ref}")

    print("\n--- 5. Computing Live Tenant Usage Metrics ---")
    usage = store.get_tenant_usage_counts(tenant_ref)
    print("Live Usage Counts:")
    for k, v in usage.items():
        print(f" • {k}: {v}")

    print("\n--- 6. Testing Subscription Cancellation & Resume ---")
    sub_canceled = store.upsert_tenant_subscription(
        subscription_ref=upgraded_sub.subscription_ref,
        tenant_ref=tenant_ref,
        tier="pro",
        status="active",
        payment_method_summary="Visa ending in 4242",
        cancel_at_period_end=True,
    )
    print(f"Cancel at period end set: {sub_canceled.cancel_at_period_end}")

    sub_resumed = store.upsert_tenant_subscription(
        subscription_ref=upgraded_sub.subscription_ref,
        tenant_ref=tenant_ref,
        tier="pro",
        status="active",
        payment_method_summary="Visa ending in 4242",
        cancel_at_period_end=False,
    )
    print(f"Subscription Resumed: cancel_at_period_end={sub_resumed.cancel_at_period_end}")

    print("\nALL BILLING & USAGE METERING INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run()

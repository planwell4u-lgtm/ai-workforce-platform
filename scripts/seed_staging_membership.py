"""Seed one explicitly approved staging principal membership."""

from __future__ import annotations

import argparse
import os

from ai_workforce_data.postgres_store import PostgresTenantStore


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--principal-ref", required=True)
    parser.add_argument("--tenant-ref", required=True)
    arguments = parser.parse_args()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is required")
    store = PostgresTenantStore(database_url)
    try:
        store.apply_migrations()
        store.verify_schema()
        store.upsert_principal_membership(
            arguments.principal_ref,
            arguments.tenant_ref,
            frozenset(
                {
                    "platform.tenant-context.read",
                    "agent.context.read",
                    "integration.support-ticket.create",
                    "operator.status.read",
                }
            ),
        )
        print(f"seeded active membership for {arguments.principal_ref} in {arguments.tenant_ref}")
    except Exception:
        store._connection.rollback()
        raise
    finally:
        store.close()


if __name__ == "__main__":
    main()

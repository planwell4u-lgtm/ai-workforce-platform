"""Integration checks for the Supabase PostgreSQL tenant-record adapter."""

from __future__ import annotations

import os
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_data.postgres_store import PostgresTenantStore
from ai_workforce_data.sqlite_store import TenantScope, VersionedRecord


@unittest.skipUnless(os.getenv("DATABASE_URL"), "DATABASE_URL is not configured")
class PostgresTenantStoreIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = PostgresTenantStore(os.environ["DATABASE_URL"])
        self.store.apply_migrations()
        self.scope = TenantScope("verification-tenant", "staging", "verification-correlation")

    def tearDown(self) -> None:
        self.store.close()

    def test_save_and_get_preserves_tenant_scope(self) -> None:
        record = VersionedRecord("postgres-verification", "v1", {"status": "ready"})
        self.store.save(self.scope, "action", record)
        self.assertEqual(self.store.get(self.scope, "action", record.record_ref), record)
        other_tenant = TenantScope("other-tenant", "staging", "other-correlation")
        self.assertIsNone(self.store.get(other_tenant, "action", record.record_ref))

    def test_conversation_compare_and_swap_rejects_stale_writes(self) -> None:
        record_ref = f"postgres-conversation-{uuid.uuid4()}"
        first = VersionedRecord(record_ref, "v1", {"state_version": 1})
        self.assertTrue(self.store.compare_and_swap(self.scope, "conversation", first, 0))
        stale = VersionedRecord(record_ref, "v1", {"state_version": 1})
        self.assertFalse(self.store.compare_and_swap(self.scope, "conversation", stale, 0))
        second = VersionedRecord(record_ref, "v1", {"state_version": 2})
        self.assertTrue(self.store.compare_and_swap(self.scope, "conversation", second, 1))

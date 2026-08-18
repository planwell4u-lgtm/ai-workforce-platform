"""B2 contract, migration, and tenant-isolation tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_data.sqlite_store import (
    ContractError,
    SqliteTenantStore,
    TenantScope,
    VersionedRecord,
)


class SqliteTenantStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temporary_directory.name) / "b2.sqlite3"
        self.store = SqliteTenantStore(self.database_path)
        self.store.apply_migrations()
        self.tenant_a = TenantScope("tenant-a", "local", "correlation-a")
        self.tenant_b = TenantScope("tenant-b", "local", "correlation-b")

    def tearDown(self) -> None:
        self.store.close()
        self.temporary_directory.cleanup()

    def test_tenant_scope_is_mandatory_for_write_and_read(self) -> None:
        record = VersionedRecord("agent-1", "v1", {"display_name": "Support"})
        self.store.save(self.tenant_a, "agent", record)
        self.assertEqual(self.store.get(self.tenant_a, "agent", "agent-1"), record)
        self.assertIsNone(self.store.get(self.tenant_b, "agent", "agent-1"))

    def test_environment_scope_cannot_read_another_environment(self) -> None:
        self.store.save(self.tenant_a, "conversation", VersionedRecord("conversation-1", "v1", {}))
        other_environment = TenantScope("tenant-a", "staging", "correlation-staging")
        self.assertIsNone(self.store.get(other_environment, "conversation", "conversation-1"))

    def test_conversation_compare_and_swap_rejects_stale_writes(self) -> None:
        first = VersionedRecord("conversation-a", "v1", {"state_version": 1})
        self.assertTrue(self.store.compare_and_swap(self.tenant_a, "conversation", first, 0))
        stale = VersionedRecord("conversation-a", "v1", {"state_version": 1})
        self.assertFalse(self.store.compare_and_swap(self.tenant_a, "conversation", stale, 0))
        second = VersionedRecord("conversation-a", "v1", {"state_version": 2})
        self.assertTrue(self.store.compare_and_swap(self.tenant_a, "conversation", second, 1))

    def test_contract_and_record_kind_are_versioned_and_bounded(self) -> None:
        with self.assertRaises(ContractError):
            VersionedRecord("agent-1", "v2", {})
        with self.assertRaises(ContractError):
            self.store.save(self.tenant_a, "unknown", VersionedRecord("record-1", "v1", {}))

    def test_migrations_are_idempotent_and_persist_after_reopen(self) -> None:
        record = VersionedRecord("action-1", "v1", {"status": "pending"})
        self.store.save(self.tenant_a, "action", record)
        self.store.apply_migrations()
        self.store.verify_schema()
        self.store.close()
        self.store = SqliteTenantStore(self.database_path)
        self.store.apply_migrations()
        self.store.verify_schema()
        self.assertEqual(self.store.get(self.tenant_a, "action", "action-1"), record)

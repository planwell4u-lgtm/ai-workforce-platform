"""Staging PostgreSQL runtime-selection tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_backend.b1 import AuditEvent
from ai_workforce_backend.runtime import (
    PostgresAuditSink,
    RuntimeConfigurationError,
    create_tenant_store,
)

DATABASE_URL = "postgresql://postgres.project:password@aws-0.pooler.supabase.com:5432/postgres"


class RuntimeConfigurationTests(unittest.TestCase):
    def test_postgres_audit_sink_persists_bounded_event_fields(self) -> None:
        store = Mock()
        PostgresAuditSink(store).record(
            AuditEvent(
                "allowed", "authorized", "correlation-1", "route-1", "principal-1", "tenant-a"
            )
        )
        arguments = store.record_audit_event.call_args.kwargs
        self.assertEqual(arguments["outcome"], "allowed")
        self.assertEqual(arguments["tenant_ref"], "tenant-a")
        self.assertTrue(arguments["event_ref"])

    @patch("ai_workforce_backend.runtime.PostgresTenantStore")
    def test_staging_selects_and_verifies_the_supabase_store(self, store_type: Mock) -> None:
        store = store_type.return_value
        self.assertIs(create_tenant_store("staging", {"DATABASE_URL": DATABASE_URL}), store)
        store_type.assert_called_once_with(DATABASE_URL)
        store.apply_migrations.assert_called_once_with()
        store.verify_schema.assert_called_once_with()

    def test_staging_requires_a_complete_supabase_postgres_url(self) -> None:
        invalid_configurations = (
            {},
            {"DATABASE_URL": "postgresql://user:password@localhost:5432/postgres"},
            {"DATABASE_URL": "https://example.supabase.co"},
        )
        for configuration in invalid_configurations:
            with (
                self.subTest(configuration=configuration),
                self.assertRaises(RuntimeConfigurationError),
            ):
                create_tenant_store("staging", configuration)

    def test_non_staging_runtime_is_not_silently_redirected_to_sqlite(self) -> None:
        with self.assertRaises(RuntimeConfigurationError):
            create_tenant_store("local", {"DATABASE_URL": DATABASE_URL})

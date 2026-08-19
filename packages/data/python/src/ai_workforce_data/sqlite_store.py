"""Local B2 SQLite adapter with mandatory tenant/environment scope."""

from __future__ import annotations

import json
import sqlite3
import time
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

RecordKind = Literal["agent", "conversation", "action"]
SUPPORTED_CONTRACT_VERSION = "v1"


class ScopeError(ValueError):
    """A required trusted scope is missing or invalid."""


class ContractError(ValueError):
    """A record does not meet the currently supported contract."""


class MigrationError(RuntimeError):
    """The local schema cannot be safely migrated or verified."""


@dataclass(frozen=True)
class TenantScope:
    """Server-resolved context; clients must not construct authority from input."""

    tenant_ref: str
    environment_ref: str
    correlation_ref: str

    def __post_init__(self) -> None:
        if not all((self.tenant_ref, self.environment_ref, self.correlation_ref)):
            raise ScopeError("trusted tenant, environment, and correlation are required")


@dataclass(frozen=True)
class VersionedRecord:
    record_ref: str
    contract_version: str
    payload: Mapping[str, object]

    def __post_init__(self) -> None:
        if not self.record_ref:
            raise ContractError("record_ref is required")
        if self.contract_version != SUPPORTED_CONTRACT_VERSION:
            raise ContractError("unsupported contract version")


MIGRATIONS: tuple[tuple[int, str], ...] = (
    (
        1,
        """
        CREATE TABLE IF NOT EXISTS tenant_records (
            record_kind TEXT NOT NULL,
            record_ref TEXT NOT NULL,
            tenant_ref TEXT NOT NULL,
            environment_ref TEXT NOT NULL,
            contract_version TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            correlation_ref TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            PRIMARY KEY (record_kind, record_ref, tenant_ref, environment_ref)
        );
        CREATE INDEX IF NOT EXISTS tenant_records_scope_idx
            ON tenant_records (tenant_ref, environment_ref, record_kind, record_ref);
        """,
    ),
)


class SqliteTenantStore:
    """Data-owned local storage that always predicates operations by trusted scope."""

    def __init__(self, database_path: Path) -> None:
        self._connection = sqlite3.connect(database_path)
        self._connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self._connection.close()

    def apply_migrations(self) -> None:
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at INTEGER NOT NULL)"
        )
        applied = {
            row["version"]
            for row in self._connection.execute("SELECT version FROM schema_migrations")
        }
        known = {version for version, _ in MIGRATIONS}
        if not applied.issubset(known):
            raise MigrationError("database contains an unknown migration")
        for version, script in MIGRATIONS:
            if version not in applied:
                self._connection.executescript(script)
                self._connection.execute(
                    "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (version, int(time.time())),
                )
        self._connection.commit()

    def verify_schema(self) -> None:
        expected = {version for version, _ in MIGRATIONS}
        rows = self._connection.execute("SELECT version FROM schema_migrations").fetchall()
        if {row["version"] for row in rows} != expected:
            raise MigrationError("schema migration ledger does not match the approved local plan")

    def save(self, scope: TenantScope, kind: RecordKind, record: VersionedRecord) -> None:
        self._validate_kind(kind)
        payload_json = json.dumps(record.payload, separators=(",", ":"), sort_keys=True)
        self._connection.execute(
            """
            INSERT INTO tenant_records (
                record_kind, record_ref, tenant_ref, environment_ref, contract_version,
                payload_json, correlation_ref, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(record_kind, record_ref, tenant_ref, environment_ref) DO UPDATE SET
                contract_version = excluded.contract_version,
                payload_json = excluded.payload_json,
                correlation_ref = excluded.correlation_ref,
                created_at = excluded.created_at
            """,
            (
                kind,
                record.record_ref,
                scope.tenant_ref,
                scope.environment_ref,
                record.contract_version,
                payload_json,
                scope.correlation_ref,
                int(time.time()),
            ),
        )
        self._connection.commit()

    def get(self, scope: TenantScope, kind: RecordKind, record_ref: str) -> VersionedRecord | None:
        self._validate_kind(kind)
        if not record_ref:
            raise ContractError("record_ref is required")
        row = self._connection.execute(
            """
            SELECT record_ref, contract_version, payload_json
            FROM tenant_records
            WHERE record_kind = ? AND record_ref = ? AND tenant_ref = ? AND environment_ref = ?
            """,
            (kind, record_ref, scope.tenant_ref, scope.environment_ref),
        ).fetchone()
        if row is None:
            return None
        return VersionedRecord(
            row["record_ref"], row["contract_version"], json.loads(row["payload_json"])
        )

    def compare_and_swap(
        self,
        scope: TenantScope,
        kind: RecordKind,
        record: VersionedRecord,
        expected_state_version: int,
    ) -> bool:
        """Persist one versioned conversation transition without last-write-wins behavior."""
        self._validate_kind(kind)
        if kind != "conversation" or expected_state_version < 0:
            raise ContractError("conversation state version is required")
        state_version = record.payload.get("state_version")
        if not isinstance(state_version, int) or state_version != expected_state_version + 1:
            raise ContractError("state_version must increment exactly once")
        payload_json = json.dumps(record.payload, separators=(",", ":"), sort_keys=True)
        try:
            self._connection.execute("BEGIN IMMEDIATE")
            cursor = self._connection.execute(
                """
                UPDATE tenant_records
                SET contract_version = ?, payload_json = ?, correlation_ref = ?, created_at = ?
                WHERE record_kind = ? AND record_ref = ? AND tenant_ref = ? AND environment_ref = ?
                  AND json_extract(payload_json, '$.state_version') = ?
                """,
                (
                    record.contract_version,
                    payload_json,
                    scope.correlation_ref,
                    int(time.time()),
                    kind,
                    record.record_ref,
                    scope.tenant_ref,
                    scope.environment_ref,
                    expected_state_version,
                ),
            )
            if cursor.rowcount == 1:
                self._connection.commit()
                return True
            if expected_state_version != 0:
                self._connection.rollback()
                return False
            cursor = self._connection.execute(
                """
                INSERT INTO tenant_records (
                    record_kind, record_ref, tenant_ref, environment_ref, contract_version,
                    payload_json, correlation_ref, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(record_kind, record_ref, tenant_ref, environment_ref) DO NOTHING
                """,
                (
                    kind,
                    record.record_ref,
                    scope.tenant_ref,
                    scope.environment_ref,
                    record.contract_version,
                    payload_json,
                    scope.correlation_ref,
                    int(time.time()),
                ),
            )
            self._connection.commit()
            return cursor.rowcount == 1
        except Exception:
            self._connection.rollback()
            raise

    @staticmethod
    def _validate_kind(kind: str) -> None:
        if kind not in {"agent", "conversation", "action"}:
            raise ContractError("unsupported record kind")

"""PostgreSQL storage adapter for scoped, versioned tenant records."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Json

from ai_workforce_data.sqlite_store import (
    ContractError,
    MigrationError,
    RecordKind,
    TenantScope,
    VersionedRecord,
)

POSTGRES_MIGRATIONS: tuple[tuple[int, str], ...] = (
    (
        1,
        """
        CREATE TABLE IF NOT EXISTS tenant_records (
            record_kind TEXT NOT NULL,
            record_ref TEXT NOT NULL,
            tenant_ref TEXT NOT NULL,
            environment_ref TEXT NOT NULL,
            contract_version TEXT NOT NULL,
            payload_json JSONB NOT NULL,
            correlation_ref TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (record_kind, record_ref, tenant_ref, environment_ref)
        );
        CREATE INDEX IF NOT EXISTS tenant_records_scope_idx
            ON tenant_records (tenant_ref, environment_ref, record_kind, record_ref);
        """,
    ),
    (
        2,
        """
        CREATE TABLE IF NOT EXISTS principal_memberships (
            principal_ref TEXT PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('active', 'revoked')),
            permissions JSONB NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    (
        3,
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            event_ref UUID PRIMARY KEY,
            occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            outcome TEXT NOT NULL CHECK (outcome IN ('allowed', 'denied')),
            reason TEXT NOT NULL,
            correlation_ref TEXT NOT NULL,
            route_ref TEXT NOT NULL,
            principal_ref TEXT,
            tenant_ref TEXT
        );
        CREATE INDEX IF NOT EXISTS audit_events_correlation_idx
            ON audit_events (correlation_ref, occurred_at);
        """,
    ),
    (
        4,
        """
        CREATE TABLE IF NOT EXISTS front_desk_active_destinations (
            tenant_ref TEXT NOT NULL,
            environment_ref TEXT NOT NULL,
            route_purpose TEXT NOT NULL,
            destination_ref TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tenant_ref, environment_ref, route_purpose)
        );
        """,
    ),
)


@dataclass(frozen=True)
class PrincipalMembershipRecord:
    principal_ref: str
    tenant_ref: str
    status: str
    permissions: frozenset[str]


class PostgresTenantStore:
    """PostgreSQL storage where every operation requires trusted tenant scope."""

    def __init__(self, database_url: str) -> None:
        if not database_url:
            raise MigrationError("DATABASE_URL is required for PostgreSQL storage")
        self._database_url = database_url
        self._connection = self._connect()

    def close(self) -> None:
        self._connection.close()

    def apply_migrations(self) -> None:
        self._ensure_connection()
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version INTEGER PRIMARY KEY,
                        applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                cursor.execute("SELECT version FROM schema_migrations")
                applied = {cast(int, row["version"]) for row in cursor.fetchall()}
                known = {version for version, _ in POSTGRES_MIGRATIONS}
                if not applied.issubset(known):
                    raise MigrationError("database contains an unknown migration")
                for version, statement in POSTGRES_MIGRATIONS:
                    if version not in applied:
                        cursor.execute(statement)
                        cursor.execute(
                            "INSERT INTO schema_migrations (version) VALUES (%s)", (version,)
                        )
            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

    def verify_schema(self) -> None:
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT version FROM schema_migrations")
            applied = {cast(int, row["version"]) for row in cursor.fetchall()}
        expected = {version for version, _ in POSTGRES_MIGRATIONS}
        if applied != expected:
            raise MigrationError("schema migration ledger does not match the approved plan")

    def save(self, scope: TenantScope, kind: RecordKind, record: VersionedRecord) -> None:
        self._ensure_connection()
        self._validate_kind(kind)
        payload = json.loads(json.dumps(record.payload))
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_records (
                    record_kind, record_ref, tenant_ref, environment_ref, contract_version,
                    payload_json, correlation_ref
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT(record_kind, record_ref, tenant_ref, environment_ref) DO UPDATE SET
                    contract_version = EXCLUDED.contract_version,
                    payload_json = EXCLUDED.payload_json,
                    correlation_ref = EXCLUDED.correlation_ref,
                    created_at = CURRENT_TIMESTAMP
                """,
                (
                    kind,
                    record.record_ref,
                    scope.tenant_ref,
                    scope.environment_ref,
                    record.contract_version,
                    Json(payload),
                    scope.correlation_ref,
                ),
            )
        self._connection.commit()

    def get(self, scope: TenantScope, kind: RecordKind, record_ref: str) -> VersionedRecord | None:
        self._ensure_connection()
        self._validate_kind(kind)
        if not record_ref:
            raise ContractError("record_ref is required")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT record_ref, contract_version, payload_json
                FROM tenant_records
                WHERE record_kind = %s AND record_ref = %s AND tenant_ref = %s
                  AND environment_ref = %s
                """,
                (kind, record_ref, scope.tenant_ref, scope.environment_ref),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        payload = row["payload_json"]
        if not isinstance(payload, Mapping):
            raise ContractError("stored payload is not an object")
        return VersionedRecord(
            cast(str, row["record_ref"]),
            cast(str, row["contract_version"]),
            cast(Mapping[str, object], payload),
        )

    def list(self, scope: TenantScope, kind: RecordKind, limit: int = 25) -> list[VersionedRecord]:
        """Return recent records only from the trusted tenant and environment scope."""
        self._ensure_connection()
        self._validate_kind(kind)
        if not 1 <= limit <= 100:
            raise ContractError("limit must be between 1 and 100")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT record_ref, contract_version, payload_json
                FROM tenant_records
                WHERE record_kind = %s AND tenant_ref = %s AND environment_ref = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (kind, scope.tenant_ref, scope.environment_ref, limit),
            )
            rows = cursor.fetchall()
        return [
            VersionedRecord(
                cast(str, row["record_ref"]),
                cast(str, row["contract_version"]),
                cast(Mapping[str, object], row["payload_json"]),
            )
            for row in rows
            if isinstance(row["payload_json"], Mapping)
        ]

    def compare_and_swap(
        self,
        scope: TenantScope,
        kind: RecordKind,
        record: VersionedRecord,
        expected_state_version: int,
    ) -> bool:
        """Persist one versioned conversation transition without last-write-wins behavior."""
        self._ensure_connection()
        self._validate_kind(kind)
        if kind != "conversation" or expected_state_version < 0:
            raise ContractError("conversation state version is required")
        state_version = record.payload.get("state_version")
        if not isinstance(state_version, int) or state_version != expected_state_version + 1:
            raise ContractError("state_version must increment exactly once")
        payload = json.loads(json.dumps(record.payload))
        with self._connection.cursor() as cursor:
            if expected_state_version == 0:
                cursor.execute(
                    """
                    INSERT INTO tenant_records (
                        record_kind, record_ref, tenant_ref, environment_ref, contract_version,
                        payload_json, correlation_ref
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT(record_kind, record_ref, tenant_ref, environment_ref) DO NOTHING
                    """,
                    (
                        kind,
                        record.record_ref,
                        scope.tenant_ref,
                        scope.environment_ref,
                        record.contract_version,
                        Json(payload),
                        scope.correlation_ref,
                    ),
                )
            else:
                cursor.execute(
                    """
                    UPDATE tenant_records
                    SET contract_version = %s, payload_json = %s, correlation_ref = %s,
                        created_at = CURRENT_TIMESTAMP
                    WHERE record_kind = %s AND record_ref = %s AND tenant_ref = %s
                      AND environment_ref = %s
                      AND (payload_json ->> 'state_version')::integer = %s
                    """,
                    (
                        record.contract_version,
                        Json(payload),
                        scope.correlation_ref,
                        kind,
                        record.record_ref,
                        scope.tenant_ref,
                        scope.environment_ref,
                        expected_state_version,
                    ),
                )
            changed = cursor.rowcount == 1
        self._connection.commit()
        return changed

    def compare_and_swap_versioned(
        self, scope: TenantScope, kind: RecordKind, record: VersionedRecord, expected_version: int
    ) -> bool:
        """Update one configuration record only when its version still matches."""
        self._ensure_connection()
        self._validate_kind(kind)
        if expected_version < 1:
            raise ContractError("expected version must be positive")
        next_version = record.payload.get("configuration_version")
        if not isinstance(next_version, int) or next_version != expected_version + 1:
            raise ContractError("configuration_version must increment exactly once")
        payload = json.loads(json.dumps(record.payload))
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tenant_records
                    SET contract_version = %s, payload_json = %s, correlation_ref = %s,
                        created_at = CURRENT_TIMESTAMP
                    WHERE record_kind = %s AND record_ref = %s AND tenant_ref = %s
                      AND environment_ref = %s
                      AND (payload_json ->> 'configuration_version')::integer = %s
                    """,
                    (
                        record.contract_version, Json(payload), scope.correlation_ref, kind,
                        record.record_ref, scope.tenant_ref, scope.environment_ref, expected_version,
                    ),
                )
            self._connection.commit()
            return cursor.rowcount == 1
        except Exception:
            self._connection.rollback()
            raise

    def activate_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        """Atomically activate a destination and claim its tenant/purpose slot."""
        purpose = self._destination_transition_inputs(record, expected_version, "active")
        payload = json.loads(json.dumps(record.payload))
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tenant_records SET contract_version = %s, payload_json = %s,
                        correlation_ref = %s, created_at = CURRENT_TIMESTAMP
                    WHERE record_kind = 'routing' AND record_ref = %s AND tenant_ref = %s
                      AND environment_ref = %s
                      AND (payload_json ->> 'configuration_version')::integer = %s
                    """,
                    (record.contract_version, Json(payload), scope.correlation_ref, record.record_ref,
                     scope.tenant_ref, scope.environment_ref, expected_version),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
                cursor.execute(
                    """
                    INSERT INTO front_desk_active_destinations (
                        tenant_ref, environment_ref, route_purpose, destination_ref
                    ) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
                    """,
                    (scope.tenant_ref, scope.environment_ref, purpose, record.record_ref),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
            self._connection.commit()
            return True
        except Exception:
            self._connection.rollback()
            raise

    def suspend_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        """Atomically suspend a destination and release only its own active claim."""
        purpose = self._destination_transition_inputs(record, expected_version, "suspended")
        payload = json.loads(json.dumps(record.payload))
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tenant_records SET contract_version = %s, payload_json = %s,
                        correlation_ref = %s, created_at = CURRENT_TIMESTAMP
                    WHERE record_kind = 'routing' AND record_ref = %s AND tenant_ref = %s
                      AND environment_ref = %s
                      AND (payload_json ->> 'configuration_version')::integer = %s
                    """,
                    (record.contract_version, Json(payload), scope.correlation_ref, record.record_ref,
                     scope.tenant_ref, scope.environment_ref, expected_version),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
                cursor.execute(
                    """
                    DELETE FROM front_desk_active_destinations
                    WHERE tenant_ref = %s AND environment_ref = %s AND route_purpose = %s
                      AND destination_ref = %s
                    """,
                    (scope.tenant_ref, scope.environment_ref, purpose, record.record_ref),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
            self._connection.commit()
            return True
        except Exception:
            self._connection.rollback()
            raise

    def withdraw_front_desk_destination(
        self, scope: TenantScope, record: VersionedRecord, expected_version: int
    ) -> bool:
        """Atomically withdraw an active destination and release its claim."""
        purpose = self._destination_transition_inputs(record, expected_version, "withdrawn")
        payload = json.loads(json.dumps(record.payload))
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tenant_records SET contract_version = %s, payload_json = %s,
                        correlation_ref = %s, created_at = CURRENT_TIMESTAMP
                    WHERE record_kind = 'routing' AND record_ref = %s AND tenant_ref = %s
                      AND environment_ref = %s
                      AND (payload_json ->> 'configuration_version')::integer = %s
                    """,
                    (record.contract_version, Json(payload), scope.correlation_ref, record.record_ref,
                     scope.tenant_ref, scope.environment_ref, expected_version),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
                cursor.execute(
                    """
                    DELETE FROM front_desk_active_destinations
                    WHERE tenant_ref = %s AND environment_ref = %s AND route_purpose = %s
                      AND destination_ref = %s
                    """,
                    (scope.tenant_ref, scope.environment_ref, purpose, record.record_ref),
                )
                if cursor.rowcount != 1:
                    self._connection.rollback()
                    return False
            self._connection.commit()
            return True
        except Exception:
            self._connection.rollback()
            raise

    @staticmethod
    def _destination_transition_inputs(
        record: VersionedRecord, expected_version: int, expected_state: str
    ) -> str:
        payload = record.payload
        purpose = payload.get("route_purpose")
        if (
            not isinstance(purpose, str)
            or payload.get("lifecycle_state") != expected_state
            or payload.get("configuration_version") != expected_version + 1
        ):
            raise ContractError("invalid destination transition")
        return purpose

    def resolve_principal_membership(self, principal_ref: str) -> PrincipalMembershipRecord | None:
        self._ensure_connection()
        if not principal_ref:
            raise ContractError("principal_ref is required")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT principal_ref, tenant_ref, status, permissions
                FROM principal_memberships
                WHERE principal_ref = %s
                """,
                (principal_ref,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        permissions = row["permissions"]
        if not isinstance(permissions, list) or not all(
            isinstance(value, str) for value in permissions
        ):
            raise ContractError("stored membership permissions are invalid")
        return PrincipalMembershipRecord(
            cast(str, row["principal_ref"]),
            cast(str, row["tenant_ref"]),
            cast(str, row["status"]),
            frozenset(permissions),
        )

    def upsert_principal_membership(
        self, principal_ref: str, tenant_ref: str, permissions: frozenset[str]
    ) -> None:
        self._ensure_connection()
        if not principal_ref or not tenant_ref or not permissions:
            raise ContractError("principal_ref, tenant_ref, and permissions are required")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO principal_memberships (principal_ref, tenant_ref, status, permissions)
                VALUES (%s, %s, 'active', %s)
                ON CONFLICT (principal_ref) DO UPDATE SET
                    tenant_ref = EXCLUDED.tenant_ref,
                    status = EXCLUDED.status,
                    permissions = EXCLUDED.permissions,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (principal_ref, tenant_ref, Json(sorted(permissions))),
            )
        self._connection.commit()

    def revoke_principal_membership(self, principal_ref: str, tenant_ref: str) -> None:
        """Revoke one active principal membership without deleting its history."""
        self._ensure_connection()
        if not principal_ref or not tenant_ref:
            raise ContractError("principal_ref and tenant_ref are required")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE principal_memberships
                SET status = 'revoked', updated_at = CURRENT_TIMESTAMP
                WHERE principal_ref = %s AND tenant_ref = %s AND status = 'active'
                """,
                (principal_ref, tenant_ref),
            )
            if cursor.rowcount != 1:
                raise ContractError("active principal membership was not found")
        self._connection.commit()

    def record_audit_event(
        self,
        *,
        event_ref: str,
        outcome: str,
        reason: str,
        correlation_ref: str,
        route_ref: str,
        principal_ref: str | None,
        tenant_ref: str | None,
    ) -> None:
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO audit_events (
                    event_ref, outcome, reason, correlation_ref, route_ref, principal_ref, tenant_ref
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (event_ref, outcome, reason, correlation_ref, route_ref, principal_ref, tenant_ref),
            )
        self._connection.commit()

    def _connect(self) -> psycopg.Connection[dict[str, object]]:
        return psycopg.connect(self._database_url, row_factory=dict_row)

    def _ensure_connection(self) -> None:
        if self._connection.closed:
            self._connection = self._connect()

    @staticmethod
    def _validate_kind(kind: str) -> None:
        if kind not in {"agent", "conversation", "action", "routing"}:
            raise ContractError("unsupported record kind")

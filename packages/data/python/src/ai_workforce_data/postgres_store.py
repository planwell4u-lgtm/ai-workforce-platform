"""PostgreSQL storage adapter for scoped, versioned tenant records."""

from __future__ import annotations

import json
import time
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
    (
        5,
        """
        CREATE TABLE IF NOT EXISTS access_change_events (
            event_ref UUID PRIMARY KEY,
            occurred_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            tenant_ref TEXT NOT NULL,
            actor_ref TEXT NOT NULL,
            target_ref TEXT NOT NULL,
            target_email TEXT,
            permissions JSONB NOT NULL
        );
        """,
    ),
    (
        6,
        """
        ALTER TABLE access_change_events
            ADD COLUMN IF NOT EXISTS actor_email TEXT;
        """,
    ),
    (
        7,
        """
        CREATE INDEX IF NOT EXISTS access_change_events_tenant_idx
            ON access_change_events (tenant_ref, occurred_at DESC);
        """,
    ),
    (
        8,
        """
        CREATE TABLE IF NOT EXISTS tenant_knowledge_articles (
            article_ref UUID PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            topic TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'faq',
            published BOOLEAN NOT NULL DEFAULT TRUE,
            created_by TEXT NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS tenant_knowledge_tenant_idx
            ON tenant_knowledge_articles (tenant_ref, updated_at DESC);
        """,
    ),
    (
        9,
        """
        CREATE TABLE IF NOT EXISTS tenant_subscriptions (
            subscription_ref UUID PRIMARY KEY,
            tenant_ref TEXT NOT NULL UNIQUE,
            tier TEXT NOT NULL DEFAULT 'free',
            status TEXT NOT NULL DEFAULT 'active',
            billing_cycle TEXT NOT NULL DEFAULT 'monthly',
            payment_method_summary TEXT,
            current_period_start TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            current_period_end TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP + INTERVAL '30 days',
            cancel_at_period_end BOOLEAN NOT NULL DEFAULT FALSE,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS tenant_subscriptions_tenant_idx
            ON tenant_subscriptions (tenant_ref);

        CREATE TABLE IF NOT EXISTS tenant_invoices (
            invoice_ref UUID PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            currency TEXT NOT NULL DEFAULT 'usd',
            status TEXT NOT NULL DEFAULT 'paid',
            tier TEXT NOT NULL,
            description TEXT NOT NULL,
            pdf_receipt_ref TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS tenant_invoices_tenant_idx
            ON tenant_invoices (tenant_ref, created_at DESC);
        """,
    ),
    (
        10,
        """
        ALTER TABLE tenant_subscriptions
            ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'mock',
            ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT,
            ADD COLUMN IF NOT EXISTS stripe_subscription_id TEXT;

        CREATE INDEX IF NOT EXISTS tenant_subscriptions_stripe_cust_idx
            ON tenant_subscriptions (stripe_customer_id) WHERE stripe_customer_id IS NOT NULL;

        CREATE INDEX IF NOT EXISTS tenant_subscriptions_stripe_sub_idx
            ON tenant_subscriptions (stripe_subscription_id) WHERE stripe_subscription_id IS NOT NULL;

        ALTER TABLE tenant_invoices
            ADD COLUMN IF NOT EXISTS provider TEXT NOT NULL DEFAULT 'mock',
            ADD COLUMN IF NOT EXISTS stripe_invoice_id TEXT,
            ADD COLUMN IF NOT EXISTS stripe_hosted_invoice_url TEXT;

        CREATE INDEX IF NOT EXISTS tenant_invoices_stripe_inv_idx
            ON tenant_invoices (stripe_invoice_id) WHERE stripe_invoice_id IS NOT NULL;
        """,
    ),
    (
        11,
        """
        CREATE TABLE IF NOT EXISTS tenant_conversation_insights (
            insight_ref TEXT PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            conversation_ref TEXT NOT NULL,
            intent TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            sentiment_score DOUBLE PRECISION NOT NULL,
            summary TEXT NOT NULL,
            action_items JSONB NOT NULL DEFAULT '[]',
            resolution_status TEXT NOT NULL DEFAULT 'resolved',
            channel TEXT NOT NULL DEFAULT 'web',
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS conversation_insights_tenant_idx
            ON tenant_conversation_insights (tenant_ref, created_at DESC);
        CREATE INDEX IF NOT EXISTS conversation_insights_conv_idx
            ON tenant_conversation_insights (conversation_ref);
        """,
    ),
    (
        12,
        """
        CREATE TABLE IF NOT EXISTS tenant_phone_numbers (
            phone_ref TEXT PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            friendly_name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            twiml_url TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS tenant_phone_numbers_tenant_idx
            ON tenant_phone_numbers (tenant_ref, status);

        CREATE TABLE IF NOT EXISTS tenant_voice_call_logs (
            call_ref TEXT PRIMARY KEY,
            tenant_ref TEXT NOT NULL,
            caller_number TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'completed',
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS tenant_voice_call_logs_tenant_idx
            ON tenant_voice_call_logs (tenant_ref, created_at DESC);
        """,
    ),
)


@dataclass(frozen=True)
class TenantPhoneNumberRecord:
    phone_ref: str
    tenant_ref: str
    phone_number: str
    friendly_name: str
    status: str
    twiml_url: str
    created_at: str


@dataclass(frozen=True)
class TenantVoiceCallLogRecord:
    call_ref: str
    tenant_ref: str
    caller_number: str
    phone_number: str
    duration_seconds: int
    status: str
    created_at: str



@dataclass(frozen=True)
class KnowledgeArticleRecord:
    article_ref: str
    tenant_ref: str
    topic: str
    question: str
    answer: str
    category: str
    published: bool
    created_by: str
    updated_at: str


@dataclass(frozen=True)
class TenantSubscriptionRecord:
    subscription_ref: str
    tenant_ref: str
    tier: str
    status: str
    billing_cycle: str
    payment_method_summary: str | None
    current_period_start: str
    current_period_end: str
    cancel_at_period_end: bool
    updated_at: str
    provider: str = "mock"
    stripe_customer_id: str | None = None
    stripe_subscription_id: str | None = None


@dataclass(frozen=True)
class TenantInvoiceRecord:
    invoice_ref: str
    tenant_ref: str
    amount_cents: int
    currency: str
    status: str
    tier: str
    description: str
    pdf_receipt_ref: str | None
    created_at: str
    provider: str = "mock"
    stripe_invoice_id: str | None = None
    stripe_hosted_invoice_url: str | None = None


@dataclass(frozen=True)
class PrincipalMembershipRecord:
    principal_ref: str
    tenant_ref: str
    status: str
    permissions: frozenset[str]


@dataclass(frozen=True)
class ConversationInsightRecord:
    insight_ref: str
    tenant_ref: str
    conversation_ref: str
    intent: str
    sentiment: str
    sentiment_score: float
    summary: str
    action_items: list[str]
    resolution_status: str
    channel: str
    created_at: str


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

    def count_active_principals_with_permission(
        self, tenant_ref: str, permission: str
    ) -> int:
        """Count how many active principals have a specific permission in a tenant."""
        self._ensure_connection()
        if not tenant_ref or not permission:
            raise ContractError("tenant_ref and permission are required")
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT count(*) as total
                FROM principal_memberships
                WHERE tenant_ref = %s AND status = 'active'
                  AND permissions @> %s::jsonb
                """,
                (tenant_ref, json.dumps([permission])),
            )
            row = cursor.fetchone()
            return int(row["total"]) if row and "total" in row else 0

    def record_access_change(
        self, *, event_ref: str, tenant_ref: str, actor_ref: str, target_ref: str,
        target_email: str | None, actor_email: str | None, permissions: frozenset[str]
    ) -> None:
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO access_change_events (
                    event_ref, tenant_ref, actor_ref, target_ref, target_email, actor_email, permissions
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (event_ref, tenant_ref, actor_ref, target_ref, target_email, actor_email, Json(sorted(permissions))),
            )
        self._connection.commit()

    def list_access_changes(self, tenant_ref: str, limit: int = 20) -> list[dict[str, object]]:
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT occurred_at, actor_ref, actor_email, target_email, permissions
                FROM access_change_events
                WHERE tenant_ref = %s
                ORDER BY occurred_at DESC
                LIMIT %s
                """,
                (tenant_ref, limit),
            )
            return [dict(row) for row in cursor.fetchall()]

    def list_knowledge_articles(self, tenant_ref: str, published_only: bool = False) -> list[KnowledgeArticleRecord]:
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            if published_only:
                cursor.execute(
                    """
                    SELECT article_ref, tenant_ref, topic, question, answer, category, published, created_by, updated_at
                    FROM tenant_knowledge_articles
                    WHERE tenant_ref = %s AND published = TRUE
                    ORDER BY updated_at DESC
                    """,
                    (tenant_ref,),
                )
            else:
                cursor.execute(
                    """
                    SELECT article_ref, tenant_ref, topic, question, answer, category, published, created_by, updated_at
                    FROM tenant_knowledge_articles
                    WHERE tenant_ref = %s
                    ORDER BY updated_at DESC
                    """,
                    (tenant_ref,),
                )
            rows = cursor.fetchall()
            return [
                KnowledgeArticleRecord(
                    article_ref=str(row["article_ref"]),
                    tenant_ref=str(row["tenant_ref"]),
                    topic=str(row["topic"]),
                    question=str(row["question"]),
                    answer=str(row["answer"]),
                    category=str(row["category"]),
                    published=bool(row["published"]),
                    created_by=str(row["created_by"]),
                    updated_at=row["updated_at"].isoformat() if hasattr(row["updated_at"], "isoformat") else str(row["updated_at"]),
                )
                for row in rows
            ]

    def upsert_knowledge_article(
        self,
        *,
        article_ref: str,
        tenant_ref: str,
        topic: str,
        question: str,
        answer: str,
        category: str = "faq",
        published: bool = True,
        created_by: str,
    ) -> None:
        if not article_ref or not tenant_ref or not question or not answer:
            raise ContractError("article_ref, tenant_ref, question, and answer are required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_knowledge_articles (
                    article_ref, tenant_ref, topic, question, answer, category, published, created_by, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (article_ref) DO UPDATE SET
                    topic = EXCLUDED.topic,
                    question = EXCLUDED.question,
                    answer = EXCLUDED.answer,
                    category = EXCLUDED.category,
                    published = EXCLUDED.published,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (article_ref, tenant_ref, topic, question, answer, category, published, created_by),
            )
        self._connection.commit()

    def delete_knowledge_article(self, tenant_ref: str, article_ref: str) -> bool:
        if not tenant_ref or not article_ref:
            raise ContractError("tenant_ref and article_ref are required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tenant_knowledge_articles
                WHERE tenant_ref = %s AND article_ref = %s
                """,
                (tenant_ref, article_ref),
            )
            deleted = cursor.rowcount == 1
        self._connection.commit()
        return deleted

    def get_tenant_subscription(self, tenant_ref: str) -> TenantSubscriptionRecord | None:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT subscription_ref, tenant_ref, tier, status, billing_cycle,
                       payment_method_summary, current_period_start, current_period_end,
                       cancel_at_period_end, updated_at, provider, stripe_customer_id, stripe_subscription_id
                FROM tenant_subscriptions
                WHERE tenant_ref = %s
                """,
                (tenant_ref,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return TenantSubscriptionRecord(
                subscription_ref=str(row["subscription_ref"]),
                tenant_ref=str(row["tenant_ref"]),
                tier=str(row["tier"]),
                status=str(row["status"]),
                billing_cycle=str(row["billing_cycle"]),
                payment_method_summary=str(row["payment_method_summary"]) if row.get("payment_method_summary") else None,
                current_period_start=row["current_period_start"].isoformat() if hasattr(row["current_period_start"], "isoformat") else str(row["current_period_start"]),
                current_period_end=row["current_period_end"].isoformat() if hasattr(row["current_period_end"], "isoformat") else str(row["current_period_end"]),
                cancel_at_period_end=bool(row["cancel_at_period_end"]),
                updated_at=row["updated_at"].isoformat() if hasattr(row["updated_at"], "isoformat") else str(row["updated_at"]),
                provider=str(row.get("provider") or "mock"),
                stripe_customer_id=str(row.get("stripe_customer_id")) if row.get("stripe_customer_id") else None,
                stripe_subscription_id=str(row.get("stripe_subscription_id")) if row.get("stripe_subscription_id") else None,
            )

    def get_tenant_subscription_by_stripe_customer(self, stripe_customer_id: str) -> TenantSubscriptionRecord | None:
        if not stripe_customer_id:
            return None
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT subscription_ref, tenant_ref, tier, status, billing_cycle,
                       payment_method_summary, current_period_start, current_period_end,
                       cancel_at_period_end, updated_at, provider, stripe_customer_id, stripe_subscription_id
                FROM tenant_subscriptions
                WHERE stripe_customer_id = %s
                """,
                (stripe_customer_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return TenantSubscriptionRecord(
                subscription_ref=str(row["subscription_ref"]),
                tenant_ref=str(row["tenant_ref"]),
                tier=str(row["tier"]),
                status=str(row["status"]),
                billing_cycle=str(row["billing_cycle"]),
                payment_method_summary=str(row["payment_method_summary"]) if row.get("payment_method_summary") else None,
                current_period_start=row["current_period_start"].isoformat() if hasattr(row["current_period_start"], "isoformat") else str(row["current_period_start"]),
                current_period_end=row["current_period_end"].isoformat() if hasattr(row["current_period_end"], "isoformat") else str(row["current_period_end"]),
                cancel_at_period_end=bool(row["cancel_at_period_end"]),
                updated_at=row["updated_at"].isoformat() if hasattr(row["updated_at"], "isoformat") else str(row["updated_at"]),
                provider=str(row.get("provider") or "mock"),
                stripe_customer_id=str(row.get("stripe_customer_id")) if row.get("stripe_customer_id") else None,
                stripe_subscription_id=str(row.get("stripe_subscription_id")) if row.get("stripe_subscription_id") else None,
            )

    def upsert_tenant_subscription(
        self,
        *,
        subscription_ref: str,
        tenant_ref: str,
        tier: str,
        status: str = "active",
        billing_cycle: str = "monthly",
        payment_method_summary: str | None = None,
        cancel_at_period_end: bool = False,
        provider: str = "mock",
        stripe_customer_id: str | None = None,
        stripe_subscription_id: str | None = None,
    ) -> TenantSubscriptionRecord:
        if not subscription_ref or not tenant_ref or not tier:
            raise ContractError("subscription_ref, tenant_ref, and tier are required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_subscriptions (
                    subscription_ref, tenant_ref, tier, status, billing_cycle,
                    payment_method_summary, cancel_at_period_end, provider,
                    stripe_customer_id, stripe_subscription_id, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (tenant_ref) DO UPDATE SET
                    tier = EXCLUDED.tier,
                    status = EXCLUDED.status,
                    billing_cycle = EXCLUDED.billing_cycle,
                    payment_method_summary = COALESCE(EXCLUDED.payment_method_summary, tenant_subscriptions.payment_method_summary),
                    cancel_at_period_end = EXCLUDED.cancel_at_period_end,
                    provider = EXCLUDED.provider,
                    stripe_customer_id = COALESCE(EXCLUDED.stripe_customer_id, tenant_subscriptions.stripe_customer_id),
                    stripe_subscription_id = COALESCE(EXCLUDED.stripe_subscription_id, tenant_subscriptions.stripe_subscription_id),
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    subscription_ref,
                    tenant_ref,
                    tier,
                    status,
                    billing_cycle,
                    payment_method_summary,
                    cancel_at_period_end,
                    provider,
                    stripe_customer_id,
                    stripe_subscription_id,
                ),
            )
        self._connection.commit()
        record = self.get_tenant_subscription(tenant_ref)
        if not record:
            raise MigrationError("failed_to_retrieve_upserted_subscription")
        return record

    def list_tenant_invoices(self, tenant_ref: str) -> list[TenantInvoiceRecord]:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT invoice_ref, tenant_ref, amount_cents, currency, status,
                       tier, description, pdf_receipt_ref, created_at,
                       provider, stripe_invoice_id, stripe_hosted_invoice_url
                FROM tenant_invoices
                WHERE tenant_ref = %s
                ORDER BY created_at DESC
                """,
                (tenant_ref,),
            )
            rows = cursor.fetchall()
            return [
                TenantInvoiceRecord(
                    invoice_ref=str(row["invoice_ref"]),
                    tenant_ref=str(row["tenant_ref"]),
                    amount_cents=int(row["amount_cents"]),
                    currency=str(row["currency"]),
                    status=str(row["status"]),
                    tier=str(row["tier"]),
                    description=str(row["description"]),
                    pdf_receipt_ref=str(row["pdf_receipt_ref"]) if row.get("pdf_receipt_ref") else None,
                    created_at=row["created_at"].isoformat() if hasattr(row["created_at"], "isoformat") else str(row["created_at"]),
                    provider=str(row.get("provider") or "mock"),
                    stripe_invoice_id=str(row.get("stripe_invoice_id")) if row.get("stripe_invoice_id") else None,
                    stripe_hosted_invoice_url=str(row.get("stripe_hosted_invoice_url")) if row.get("stripe_hosted_invoice_url") else None,
                )
                for row in rows
            ]

    def record_tenant_invoice(
        self,
        *,
        invoice_ref: str,
        tenant_ref: str,
        amount_cents: int,
        currency: str = "usd",
        status: str = "paid",
        tier: str,
        description: str,
        pdf_receipt_ref: str | None = None,
        provider: str = "mock",
        stripe_invoice_id: str | None = None,
        stripe_hosted_invoice_url: str | None = None,
    ) -> TenantInvoiceRecord:
        if not invoice_ref or not tenant_ref or not tier or not description:
            raise ContractError("invoice_ref, tenant_ref, tier, and description are required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_invoices (
                    invoice_ref, tenant_ref, amount_cents, currency, status,
                    tier, description, pdf_receipt_ref, provider,
                    stripe_invoice_id, stripe_hosted_invoice_url, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """,
                (
                    invoice_ref,
                    tenant_ref,
                    amount_cents,
                    currency,
                    status,
                    tier,
                    description,
                    pdf_receipt_ref,
                    provider,
                    stripe_invoice_id,
                    stripe_hosted_invoice_url,
                ),
            )
        self._connection.commit()
        return TenantInvoiceRecord(
            invoice_ref=invoice_ref,
            tenant_ref=tenant_ref,
            amount_cents=amount_cents,
            currency=currency,
            status=status,
            tier=tier,
            description=description,
            pdf_receipt_ref=pdf_receipt_ref,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            provider=provider,
            stripe_invoice_id=stripe_invoice_id,
            stripe_hosted_invoice_url=stripe_hosted_invoice_url,
        )

    def get_tenant_usage_counts(self, tenant_ref: str) -> dict[str, int]:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) AS count FROM tenant_knowledge_articles WHERE tenant_ref = %s",
                (tenant_ref,),
            )
            kb_row = cursor.fetchone()
            kb_count = int(kb_row["count"]) if kb_row else 0

            cursor.execute(
                "SELECT COUNT(*) AS count FROM tenant_records WHERE tenant_ref = %s AND record_kind = 'conversation'",
                (tenant_ref,),
            )
            conv_row = cursor.fetchone()
            conv_count = int(conv_row["count"]) if conv_row else 0

            cursor.execute(
                "SELECT COUNT(*) AS count FROM tenant_records WHERE tenant_ref = %s AND record_kind = 'action'",
                (tenant_ref,),
            )
            action_row = cursor.fetchone()
            action_count = int(action_row["count"]) if action_row else 0

        return {
            "knowledge_articles": kb_count,
            "conversations": conv_count,
            "actions_executed": action_count,
            "voice_agent_minutes": conv_count * 3,  # estimated simulated active runtime
        }

    def upsert_conversation_insight(
        self, insight: ConversationInsightRecord
    ) -> ConversationInsightRecord:
        if not insight.tenant_ref or not insight.insight_ref:
            raise ContractError("tenant_ref and insight_ref are required")
        self._ensure_connection()
        action_items_json = Json(insight.action_items)
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_conversation_insights (
                    insight_ref, tenant_ref, conversation_ref, intent, sentiment,
                    sentiment_score, summary, action_items, resolution_status, channel
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT(insight_ref) DO UPDATE SET
                    intent = EXCLUDED.intent,
                    sentiment = EXCLUDED.sentiment,
                    sentiment_score = EXCLUDED.sentiment_score,
                    summary = EXCLUDED.summary,
                    action_items = EXCLUDED.action_items,
                    resolution_status = EXCLUDED.resolution_status,
                    channel = EXCLUDED.channel
                """,
                (
                    insight.insight_ref,
                    insight.tenant_ref,
                    insight.conversation_ref,
                    insight.intent,
                    insight.sentiment,
                    insight.sentiment_score,
                    insight.summary,
                    action_items_json,
                    insight.resolution_status,
                    insight.channel,
                ),
            )
        self._connection.commit()
        return insight

    def list_conversation_insights(
        self, tenant_ref: str, limit: int = 50
    ) -> list[ConversationInsightRecord]:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT insight_ref, tenant_ref, conversation_ref, intent, sentiment,
                       sentiment_score, summary, action_items, resolution_status, channel,
                       created_at
                FROM tenant_conversation_insights
                WHERE tenant_ref = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (tenant_ref, limit),
            )
            rows = cursor.fetchall()

        results: list[ConversationInsightRecord] = []
        for row in rows:
            items = row["action_items"]
            if isinstance(items, str):
                try:
                    items = json.loads(items)
                except Exception:
                    items = []
            elif not isinstance(items, list):
                items = []

            results.append(
                ConversationInsightRecord(
                    insight_ref=cast(str, row["insight_ref"]),
                    tenant_ref=cast(str, row["tenant_ref"]),
                    conversation_ref=cast(str, row["conversation_ref"]),
                    intent=cast(str, row["intent"]),
                    sentiment=cast(str, row["sentiment"]),
                    sentiment_score=float(row["sentiment_score"]),
                    summary=cast(str, row["summary"]),
                    action_items=[str(x) for x in items],
                    resolution_status=cast(str, row["resolution_status"]),
                    channel=cast(str, row["channel"]),
                    created_at=str(row["created_at"]),
                )
            )
        return results

    def assign_tenant_phone_number(
        self,
        *,
        tenant_ref: str,
        phone_number: str,
        friendly_name: str = "Voice Support Line",
        twiml_url: str = "https://handler.twilio.com/twiml/EH2b541a7f69ad0c39f340b2f36c4f3c67",
    ) -> TenantPhoneNumberRecord:
        if not tenant_ref or not phone_number:
            raise ContractError("tenant_ref and phone_number are required")
        self._ensure_connection()
        phone_ref = f"phone_{uuid.uuid4().hex[:12]}"
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_phone_numbers (
                    phone_ref, tenant_ref, phone_number, friendly_name, status, twiml_url
                ) VALUES (%s, %s, %s, %s, 'active', %s)
                RETURNING phone_ref, tenant_ref, phone_number, friendly_name, status, twiml_url, created_at
                """,
                (phone_ref, tenant_ref, phone_number, friendly_name, twiml_url),
            )
            row = cursor.fetchone()
        self._connection.commit()
        assert row is not None
        return TenantPhoneNumberRecord(
            phone_ref=cast(str, row["phone_ref"]),
            tenant_ref=cast(str, row["tenant_ref"]),
            phone_number=cast(str, row["phone_number"]),
            friendly_name=cast(str, row["friendly_name"]),
            status=cast(str, row["status"]),
            twiml_url=cast(str, row["twiml_url"]),
            created_at=str(row["created_at"]),
        )

    def list_tenant_phone_numbers(self, tenant_ref: str) -> list[TenantPhoneNumberRecord]:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT phone_ref, tenant_ref, phone_number, friendly_name, status, twiml_url, created_at
                FROM tenant_phone_numbers
                WHERE tenant_ref = %s
                ORDER BY created_at DESC
                """,
                (tenant_ref,),
            )
            rows = cursor.fetchall()
        return [
            TenantPhoneNumberRecord(
                phone_ref=cast(str, row["phone_ref"]),
                tenant_ref=cast(str, row["tenant_ref"]),
                phone_number=cast(str, row["phone_number"]),
                friendly_name=cast(str, row["friendly_name"]),
                status=cast(str, row["status"]),
                twiml_url=cast(str, row["twiml_url"]),
                created_at=str(row["created_at"]),
            )
            for row in rows
        ]

    def log_tenant_voice_call(
        self,
        *,
        tenant_ref: str,
        caller_number: str,
        phone_number: str,
        duration_seconds: int = 0,
        status: str = "completed",
    ) -> TenantVoiceCallLogRecord:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        call_ref = f"call_{uuid.uuid4().hex[:12]}"
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tenant_voice_call_logs (
                    call_ref, tenant_ref, caller_number, phone_number, duration_seconds, status
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING call_ref, tenant_ref, caller_number, phone_number, duration_seconds, status, created_at
                """,
                (call_ref, tenant_ref, caller_number, phone_number, duration_seconds, status),
            )
            row = cursor.fetchone()
        self._connection.commit()
        assert row is not None
        return TenantVoiceCallLogRecord(
            call_ref=cast(str, row["call_ref"]),
            tenant_ref=cast(str, row["tenant_ref"]),
            caller_number=cast(str, row["caller_number"]),
            phone_number=cast(str, row["phone_number"]),
            duration_seconds=int(row["duration_seconds"]),
            status=cast(str, row["status"]),
            created_at=str(row["created_at"]),
        )

    def list_tenant_voice_call_logs(self, tenant_ref: str, limit: int = 50) -> list[TenantVoiceCallLogRecord]:
        if not tenant_ref:
            raise ContractError("tenant_ref is required")
        self._ensure_connection()
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT call_ref, tenant_ref, caller_number, phone_number, duration_seconds, status, created_at
                FROM tenant_voice_call_logs
                WHERE tenant_ref = %s
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (tenant_ref, limit),
            )
            rows = cursor.fetchall()
        return [
            TenantVoiceCallLogRecord(
                call_ref=cast(str, row["call_ref"]),
                tenant_ref=cast(str, row["tenant_ref"]),
                caller_number=cast(str, row["caller_number"]),
                phone_number=cast(str, row["phone_number"]),
                duration_seconds=int(row["duration_seconds"]),
                status=cast(str, row["status"]),
                created_at=str(row["created_at"]),
            )
            for row in rows
        ]

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
        else:
            try:
                self._connection.execute("SELECT 1")
            except Exception:
                try:
                    self._connection.close()
                except Exception:
                    pass
                self._connection = self._connect()

    @staticmethod
    def _validate_kind(kind: str) -> None:
        if kind not in {"agent", "conversation", "action", "routing"}:
            raise ContractError("unsupported record kind")

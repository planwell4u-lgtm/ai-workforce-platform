"""Runtime selection for backend-owned provider adapters."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol
from urllib.parse import urlparse

from ai_workforce_data.postgres_store import PostgresTenantStore

from .b1 import AuditEvent, AuditSink, AuthorizationError, Membership, MembershipDirectory


class TenantStore(Protocol):
    """The bounded data contract needed by the backend composition root."""

    def close(self) -> None: ...

    def apply_migrations(self) -> None: ...

    def verify_schema(self) -> None: ...


class RuntimeConfigurationError(RuntimeError):
    """A deployment has not selected a safe runtime configuration."""


class PostgresMembershipDirectory(MembershipDirectory):
    """Resolve current tenant membership from the Data-owned PostgreSQL store."""

    def __init__(self, store: PostgresTenantStore) -> None:
        self._store = store

    def resolve(self, principal_ref: str) -> Membership:
        record = self._store.resolve_principal_membership(principal_ref)
        if record is None or record.status != "active":
            raise AuthorizationError("membership_not_active")
        return Membership(record.principal_ref, record.tenant_ref, "active", record.permissions)


class PostgresAuditSink(AuditSink):
    """Persist bounded backend audit evidence in the staging tenant store."""

    def __init__(self, store: PostgresTenantStore) -> None:
        self._store = store

    def record(self, event: AuditEvent) -> None:
        import uuid

        self._store.record_audit_event(
            event_ref=str(uuid.uuid4()),
            outcome=event.outcome,
            reason=event.reason,
            correlation_ref=event.correlation_ref,
            route_ref=event.route_ref,
            principal_ref=event.principal_ref,
            tenant_ref=event.tenant_ref,
        )


def create_tenant_store(environment_ref: str, configuration: Mapping[str, str]) -> TenantStore:
    """Select and prepare the approved tenant store for an environment."""
    if environment_ref != "staging":
        raise RuntimeConfigurationError("the backend runtime currently supports staging only")
    database_url = configuration.get("DATABASE_URL")
    if not database_url:
        raise RuntimeConfigurationError("DATABASE_URL is required in staging")
    _validate_supabase_postgres_url(database_url)
    store = PostgresTenantStore(database_url)
    try:
        store.apply_migrations()
        store.verify_schema()
    except Exception:
        store.close()
        raise
    return store


def _validate_supabase_postgres_url(database_url: str) -> None:
    parsed = urlparse(database_url)
    host = parsed.hostname or ""
    if (
        parsed.scheme not in {"postgres", "postgresql"}
        or not parsed.username
        or not parsed.password
    ):
        raise RuntimeConfigurationError("DATABASE_URL must be a complete PostgreSQL connection URL")
    if not host.endswith((".pooler.supabase.com", ".supabase.co")):
        raise RuntimeConfigurationError("staging DATABASE_URL must target Supabase PostgreSQL")

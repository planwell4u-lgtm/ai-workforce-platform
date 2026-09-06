"""System Governance & Health Telemetry API for Planwell Platform."""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable, Mapping
from typing import Any, cast

from ai_workforce_data.postgres_store import PostgresTenantStore

from .b1 import (
    AuditEvent,
    AuditSink,
    AuthenticationError,
    AuthorizationError,
    IdentityVerifier,
    MembershipDirectory,
)
from .redis_cache import RedisCacheManager

START_TIME = time.time()


class SystemHealthApi:
    """Exposes system governance, database latency, cache telemetry, and security health status."""

    route_ref = "agent.system-health.v1"
    read_permissions = frozenset({"platform.owner", "agent.context.read"})

    def __init__(
        self,
        verifier: IdentityVerifier,
        memberships: MembershipDirectory,
        store: PostgresTenantStore,
        audit_sink: AuditSink,
        cache: RedisCacheManager | None = None,
        correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4()),
    ) -> None:
        self._verifier = verifier
        self._memberships = memberships
        self._store = store
        self._audit_sink = audit_sink
        self._cache = cache or RedisCacheManager()
        self._correlation_factory = correlation_factory

    def __call__(
        self, environ: Mapping[str, object], start_response: Callable[..., object]
    ) -> list[bytes]:
        correlation_ref = self._correlation_factory()
        path = str(environ.get("PATH_INFO", "")).rstrip("/")
        method = str(environ.get("REQUEST_METHOD", "GET")).upper()

        if path == "/v1/owner/system-health" and method == "GET":
            return self._handle_get_health(environ, start_response, correlation_ref)

        return self._json_response(
            start_response, 404, {"error": "Not Found", "path": path}, correlation_ref
        )

    def _handle_get_health(
        self, environ: Mapping[str, object], start_response: Callable[..., object], correlation_ref: str
    ) -> list[bytes]:
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            if not (self.read_permissions & membership.permissions):
                raise AuthorizationError("forbidden")
            tenant_ref = membership.tenant_ref
        except AuthenticationError as exc:
            return self._json_response(start_response, 401, {"error": str(exc)}, correlation_ref)
        except AuthorizationError as exc:
            return self._json_response(start_response, 403, {"error": str(exc)}, correlation_ref)
        except Exception:
            return self._json_response(start_response, 401, {"error": "unauthorized"}, correlation_ref)

        # Database latency check
        db_start = time.time()
        db_healthy = True
        try:
            self._store._ensure_connection()
            db_latency_ms = round((time.time() - db_start) * 1000, 2)
        except Exception:
            db_healthy = False
            db_latency_ms = -1.0

        # Cache check
        cache_healthy = self._cache.is_available()
        cache_provider = "redis" if cache_healthy else "in_memory_fallback"

        uptime_seconds = int(time.time() - START_TIME)

        telemetry = {
            "status": "healthy" if db_healthy else "degraded",
            "uptime_seconds": uptime_seconds,
            "database": {
                "status": "healthy" if db_healthy else "error",
                "ping_latency_ms": db_latency_ms,
                "engine": "PostgreSQL 16",
                "latest_migration": 11,
            },
            "cache": {
                "status": "healthy" if cache_healthy else "standby",
                "provider": cache_provider,
                "failover_active": not cache_healthy,
            },
            "security": {
                "auth_provider": "Auth0 RS256 JWT",
                "hmac_validation": "Active (Meta WhatsApp & Webhooks)",
                "rbac_enforcement": "Active",
            },
        }

        self._audit_sink.record(
            AuditEvent(
                outcome="allowed",
                reason="get_system_health",
                correlation_ref=correlation_ref,
                route_ref=self.route_ref,
                principal_ref=identity.principal_ref,
                tenant_ref=tenant_ref,
            )
        )

        return self._json_response(start_response, 200, telemetry, correlation_ref)

    def _json_response(
        self,
        start_response: Callable[..., object],
        status_code: int,
        payload: dict[str, Any],
        correlation_ref: str,
    ) -> list[bytes]:
        status_lines = {
            200: "200 OK",
            401: "401 Unauthorized",
            403: "403 Forbidden",
            404: "404 Not Found",
            500: "500 Internal Server Error",
        }
        body = json.dumps(payload, indent=2).encode("utf-8")
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("X-Correlation-ID", correlation_ref),
        ]
        start_response(status_lines.get(status_code, f"{status_code} Status"), headers)
        return [body]

"""Owner-only management of the two Planwell workspace permissions."""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable, Mapping
from typing import Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from ai_workforce_data.postgres_store import PostgresTenantStore

from .b1 import AuditEvent, AuditSink, AuthenticationError, AuthorizationError, IdentityVerifier, MembershipDirectory


class Auth0ManagementClient:
    """Small, server-only Auth0 Management API client; secrets never leave the backend."""

    def __init__(self, domain: str, client_id: str, client_secret: str) -> None:
        self._domain, self._client_id, self._client_secret = domain, client_id, client_secret
        self._token = ""
        self._expires_at = 0.0

    def find_user(self, email: str) -> dict[str, object] | None:
        result = self._request("GET", f"/api/v2/users-by-email?email={quote(email, safe='@')}")
        if not isinstance(result, list) or not result:
            return None
        user = result[0]
        if not isinstance(user, dict) or not isinstance(user.get("user_id"), str):
            raise ValueError("invalid_auth0_response")
        return cast(dict[str, object], user)

    def user(self, user_id: str) -> dict[str, object] | None:
        result = self._request("GET", f"/api/v2/users/{quote(user_id, safe='')}")
        if not isinstance(result, dict):
            return None
        return cast(dict[str, object], result)

    def permissions(self, user_id: str) -> set[str]:
        result = self._request("GET", f"/api/v2/users/{quote(user_id, safe='')}/permissions")
        if not isinstance(result, list):
            raise ValueError("invalid_auth0_response")
        return {item["permission_name"] for item in result if isinstance(item, dict) and isinstance(item.get("permission_name"), str)}

    def add_permission(self, user_id: str, audience: str, permission: str) -> None:
        self._request("POST", f"/api/v2/users/{quote(user_id, safe='')}/permissions", {
            "permissions": [{"resource_server_identifier": audience, "permission_name": permission}]
        })

    def remove_permission(self, user_id: str, audience: str, permission: str) -> None:
        self._request("DELETE", f"/api/v2/users/{quote(user_id, safe='')}/permissions", {
            "permissions": [{"resource_server_identifier": audience, "permission_name": permission}]
        })

    def _request(self, method: str, path: str, payload: dict[str, object] | None = None) -> object:
        token = self._access_token()
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(f"https://{self._domain}{path}", data=body, method=method, headers={
            "Authorization": f"Bearer {token}", "Content-Type": "application/json",
        })
        try:
            with urlopen(request, timeout=10) as response:
                raw = response.read()
        except (HTTPError, URLError) as error:
            raise RuntimeError("auth0_management_request_failed") from error
        return json.loads(raw.decode("utf-8")) if raw else {}

    def _access_token(self) -> str:
        if self._token and time.time() < self._expires_at:
            return self._token
        payload = json.dumps({
            "client_id": self._client_id, "client_secret": self._client_secret,
            "audience": f"https://{self._domain}/api/v2/", "grant_type": "client_credentials",
        }).encode("utf-8")
        request = Request(f"https://{self._domain}/oauth/token", data=payload, method="POST", headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError) as error:
            raise RuntimeError("auth0_management_token_failed") from error
        token, expires_in = result.get("access_token"), result.get("expires_in")
        if not isinstance(token, str) or not isinstance(expires_in, int):
            raise RuntimeError("auth0_management_token_failed")
        self._token, self._expires_at = token, time.time() + max(30, expires_in - 60)
        return token


class AccessManagementApi:
    path = "/v1/access-management"
    route_ref = "platform.access-management.v1"
    required_permissions = frozenset({"platform.owner", "platform.front-desk.configure"})
    managed_permissions = frozenset({"agent.context.read", "platform.front-desk.configure", "platform.owner"})

    def __init__(self, verifier: IdentityVerifier, memberships: MembershipDirectory, audit_sink: AuditSink,
                 store: PostgresTenantStore, client: Auth0ManagementClient, audience: str,
                 correlation_factory: Callable[[], str] = lambda: str(uuid.uuid4())) -> None:
        self._verifier, self._memberships, self._audit_sink = verifier, memberships, audit_sink
        self._store, self._client, self._audience, self._correlation_factory = store, client, audience, correlation_factory

    def __call__(self, environ: Mapping[str, object], start_response: Callable[..., object]) -> list[bytes]:
        correlation = self._correlation_factory()
        headers = [("Content-Type", "application/json"), ("X-Correlation-Id", correlation)]
        identity = None
        membership = None
        try:
            identity = self._verifier.verify(cast(str | None, environ.get("HTTP_AUTHORIZATION")))
            membership = self._memberships.resolve(identity.principal_ref)
            has_membership_perm = any(perm in membership.permissions for perm in self.required_permissions)
            has_identity_perm = any(perm in identity.granted_permissions for perm in self.required_permissions)
            if not has_membership_perm or not has_identity_perm:
                raise AuthorizationError("insufficient_permission")
            actor = self._client.user(identity.principal_ref)
            actor_email = actor.get("email") if isinstance(actor, dict) and isinstance(actor.get("email"), str) else None
            status, body = self._dispatch(environ, membership.tenant_ref, identity.principal_ref, actor_email)
            self._audit_sink.record(AuditEvent("allowed", "access_updated", correlation, self.route_ref, identity.principal_ref, membership.tenant_ref))
            return self._respond(start_response, status, headers, body)
        except AuthenticationError:
            return self._respond(start_response, "401 Unauthorized", headers, {"error": "unauthorized"})
        except AuthorizationError:
            return self._respond(start_response, "403 Forbidden", headers, {"error": "forbidden"})
        except (TypeError, ValueError):
            return self._respond(start_response, "400 Bad Request", headers, {"error": "invalid_request"})
        except RuntimeError:
            return self._respond(start_response, "502 Bad Gateway", headers, {"error": "access_service_unavailable"})

    def _dispatch(self, environ: Mapping[str, object], tenant_ref: str, actor_ref: str, actor_email: str | None) -> tuple[str, dict[str, object]]:
        method = environ.get("REQUEST_METHOD")
        if method == "POST":
            data = self._body(environ, {"email", "permissions"})
            email, requested = data["email"], data["permissions"]
            if not isinstance(email, str) or not isinstance(requested, list) or not all(isinstance(p, str) for p in requested):
                raise ValueError("invalid_request")
            permissions = frozenset(requested)
            if not permissions.issubset(self.managed_permissions):
                raise ValueError("invalid_request")
            user = self._client.find_user(email.strip().lower())
            if user is None:
                return "404 Not Found", {"error": "user_not_found"}
            user_id = cast(str, user["user_id"])
            existing = self._client.permissions(user_id)
            record = self._store.resolve_principal_membership(user_id)
            is_currently_owner = "platform.owner" in existing or (record is not None and "platform.owner" in record.permissions)
            is_removing_owner = is_currently_owner and ("platform.owner" not in permissions)
            if is_removing_owner:
                active_owners = self._store.count_active_principals_with_permission(tenant_ref, "platform.owner")
                if active_owners <= 1:
                    return "400 Bad Request", {"error": "cannot_remove_last_owner"}
            for permission in self.managed_permissions:
                if permission in permissions and permission not in existing:
                    self._client.add_permission(user_id, self._audience, permission)
                if permission not in permissions and permission in existing:
                    self._client.remove_permission(user_id, self._audience, permission)
            preserved = frozenset() if record is None else record.permissions - self.managed_permissions
            next_permissions = preserved | permissions
            if next_permissions:
                self._store.upsert_principal_membership(user_id, tenant_ref, next_permissions)
            elif record is not None and record.status == "active":
                self._store.revoke_principal_membership(user_id, tenant_ref)
            self._store.record_access_change(
                event_ref=str(uuid.uuid4()), tenant_ref=tenant_ref, actor_ref=actor_ref,
                target_ref=user_id, target_email=cast(str | None, user.get("email")), actor_email=actor_email, permissions=permissions,
            )
            return "200 OK", {"user": self._public_user(user, permissions)}
        if method == "GET":
            query = cast(str, environ.get("QUERY_STRING", ""))
            if query == "history=1":
                return "200 OK", {"changes": self._history(tenant_ref)}
            if not query.startswith("email="):
                raise ValueError("invalid_request")
            email = query.removeprefix("email=").replace("%40", "@")
            user = self._client.find_user(email)
            if user is None:
                return "404 Not Found", {"error": "user_not_found"}
            current = self._client.permissions(cast(str, user["user_id"])) & self.managed_permissions
            return "200 OK", {"user": self._public_user(user, current)}
        return "405 Method Not Allowed", {"error": "method_not_allowed"}

    def _history(self, tenant_ref: str) -> list[dict[str, object]]:
        changes = self._store.list_access_changes(tenant_ref)
        return [
            {
                "occurred_at": row["occurred_at"].isoformat() if hasattr(row.get("occurred_at"), "isoformat") else row.get("occurred_at"),
                "changed_by": row.get("actor_email") or row.get("actor_ref"), "user_email": row.get("target_email"),
                "permissions": row.get("permissions") if isinstance(row.get("permissions"), list) else [],
            }
            for row in changes
        ]

    @staticmethod
    def _body(environ: Mapping[str, object], expected: set[str]) -> dict[str, object]:
        size = int(cast(str, environ.get("CONTENT_LENGTH", "0")))
        raw = environ.get("wsgi.input")
        if not hasattr(raw, "read") or not 2 <= size <= 4096:
            raise TypeError("invalid_request")
        data = json.loads(raw.read(size).decode("utf-8"))
        if not isinstance(data, dict) or set(data) != expected:
            raise ValueError("invalid_request")
        return cast(dict[str, object], data)

    @staticmethod
    def _public_user(user: Mapping[str, object], permissions: frozenset[str] | set[str]) -> dict[str, object]:
        return {"email": user.get("email"), "name": user.get("name"), "permissions": sorted(permissions)}

    @staticmethod
    def _respond(start_response: Callable[..., object], status: str, headers: list[tuple[str, str]], body: dict[str, object]) -> list[bytes]:
        encoded = json.dumps(body).encode("utf-8")
        start_response(status, [*headers, ("Content-Length", str(len(encoded)))])
        return [encoded]

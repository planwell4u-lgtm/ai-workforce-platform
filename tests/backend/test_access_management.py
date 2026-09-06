"""Access Management and Multiple Dedicated Owners unit tests."""

from __future__ import annotations

import io
import json
import sys
import time
import unittest
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "data" / "python" / "src"))

from ai_workforce_backend.access_management import AccessManagementApi, Auth0ManagementClient
from ai_workforce_backend.b1 import (
    AuthenticationError,
    IdentityContext,
    IdentityVerifier,
    InMemoryAuditSink,
    InMemoryMembershipDirectory,
    Membership,
)
from ai_workforce_data.postgres_store import PrincipalMembershipRecord

AUDIENCE = "https://api.planwell.online"
ENVIRONMENT = "local"


class FakeVerifier(IdentityVerifier):
    def __init__(self, permissions_map: dict[str, frozenset[str]]) -> None:
        self.permissions_map = permissions_map

    def verify(self, authorization: str | None) -> IdentityContext:
        if not authorization or not authorization.startswith("Bearer "):
            raise AuthenticationError("missing_bearer_token")
        principal = authorization.removeprefix("Bearer ")
        return IdentityContext(
            principal_ref=principal,
            principal_type="human",
            issuer_ref="test",
            environment_ref=ENVIRONMENT,
            authenticated_at=int(time.time()),
            granted_permissions=self.permissions_map.get(principal, frozenset()),
        )


class FakeAuth0Client(Auth0ManagementClient):
    def __init__(self) -> None:
        self.users = {
            "owner1@planwell.online": {"user_id": "auth0|owner1", "email": "owner1@planwell.online", "name": "Owner One"},
            "owner2@planwell.online": {"user_id": "auth0|owner2", "email": "owner2@planwell.online", "name": "Owner Two"},
            "employee@planwell.online": {"user_id": "auth0|emp1", "email": "employee@planwell.online", "name": "Employee One"},
        }
        self.user_perms: dict[str, set[str]] = {
            "auth0|owner1": {"platform.owner"},
            "auth0|owner2": {"platform.owner"},
            "auth0|emp1": {"agent.context.read"},
        }

    def find_user(self, email: str) -> dict[str, object] | None:
        return self.users.get(email)

    def user(self, user_id: str) -> dict[str, object] | None:
        for u in self.users.values():
            if u["user_id"] == user_id:
                return u
        return None

    def permissions(self, user_id: str) -> set[str]:
        return self.user_perms.get(user_id, set())

    def add_permission(self, user_id: str, audience: str, permission: str) -> None:
        self.user_perms.setdefault(user_id, set()).add(permission)

    def remove_permission(self, user_id: str, audience: str, permission: str) -> None:
        if user_id in self.user_perms:
            self.user_perms[user_id].discard(permission)


class FakePostgresTenantStore:
    def __init__(self) -> None:
        self.memberships: dict[str, PrincipalMembershipRecord] = {
            "auth0|owner1": PrincipalMembershipRecord("auth0|owner1", "tenant-planwell", "active", frozenset({"platform.owner"})),
            "auth0|owner2": PrincipalMembershipRecord("auth0|owner2", "tenant-planwell", "active", frozenset({"platform.owner"})),
            "auth0|emp1": PrincipalMembershipRecord("auth0|emp1", "tenant-planwell", "active", frozenset({"agent.context.read"})),
        }
        self.history: list[dict[str, object]] = []

    def resolve_principal_membership(self, principal_ref: str) -> PrincipalMembershipRecord | None:
        return self.memberships.get(principal_ref)

    def count_active_principals_with_permission(self, tenant_ref: str, permission: str) -> int:
        return sum(
            1 for m in self.memberships.values()
            if m.tenant_ref == tenant_ref and m.status == "active" and permission in m.permissions
        )

    def upsert_principal_membership(self, principal_ref: str, tenant_ref: str, permissions: frozenset[str]) -> None:
        self.memberships[principal_ref] = PrincipalMembershipRecord(principal_ref, tenant_ref, "active", permissions)

    def revoke_principal_membership(self, principal_ref: str, tenant_ref: str) -> None:
        if principal_ref in self.memberships:
            self.memberships[principal_ref] = PrincipalMembershipRecord(
                principal_ref, tenant_ref, "revoked", self.memberships[principal_ref].permissions
            )

    def record_access_change(self, **kwargs: object) -> None:
        self.history.append(kwargs)

    def list_access_changes(self, tenant_ref: str, limit: int = 20) -> list[dict[str, object]]:
        return self.history[:limit]


class AccessManagementApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = InMemoryAuditSink()
        self.store = FakePostgresTenantStore()
        self.client = FakeAuth0Client()
        memberships = (
            Membership("auth0|owner1", "tenant-planwell", "active", frozenset({"platform.owner"})),
            Membership("auth0|owner2", "tenant-planwell", "active", frozenset({"platform.owner"})),
            Membership("auth0|legacy-admin", "tenant-planwell", "active", frozenset({"platform.front-desk.configure"})),
            Membership("auth0|emp1", "tenant-planwell", "active", frozenset({"agent.context.read"})),
        )
        granted_permissions_map = {
            "auth0|owner1": frozenset({"platform.owner"}),
            "auth0|owner2": frozenset({"platform.owner"}),
            "auth0|legacy-admin": frozenset({"platform.front-desk.configure"}),
            "auth0|emp1": frozenset({"agent.context.read"}),
        }
        self.app = AccessManagementApi(
            FakeVerifier(granted_permissions_map),
            InMemoryMembershipDirectory(memberships),
            self.audit,
            cast(Any, self.store),
            self.client,
            AUDIENCE,
            correlation_factory=lambda: "corr-123",
        )

    def _request(self, method: str, query: str = "", body: dict[str, object] | None = None, token_principal: str | None = None) -> tuple[str, dict[str, object]]:
        captured: dict[str, object] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = status
            captured["headers"] = dict(headers)

        environ: dict[str, object] = {
            "REQUEST_METHOD": method,
            "PATH_INFO": "/v1/access-management",
            "QUERY_STRING": query,
        }
        if token_principal is not None:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {token_principal}"
        if body is not None:
            raw = json.dumps(body).encode("utf-8")
            environ["CONTENT_LENGTH"] = str(len(raw))
            environ["wsgi.input"] = io.BytesIO(raw)

        raw_resp = b"".join(self.app(environ, start_response))
        return cast(str, captured["status"]), json.loads(raw_resp) if raw_resp else {}

    def test_owner_can_query_user(self) -> None:
        status, data = self._request("GET", query="email=employee%40planwell.online", token_principal="auth0|owner1")
        self.assertEqual(status, "200 OK")
        self.assertEqual(data["user"]["email"], "employee@planwell.online")
        self.assertEqual(data["user"]["permissions"], ["agent.context.read"])

    def test_legacy_front_desk_admin_can_access(self) -> None:
        status, data = self._request("GET", query="email=employee%40planwell.online", token_principal="auth0|legacy-admin")
        self.assertEqual(status, "200 OK")

    def test_unauthorized_user_forbidden(self) -> None:
        status, data = self._request("GET", query="email=employee%40planwell.online", token_principal="auth0|emp1")
        self.assertEqual(status, "403 Forbidden")

    def test_owner_can_grant_second_owner(self) -> None:
        status, data = self._request(
            "POST",
            body={"email": "employee@planwell.online", "permissions": ["platform.owner", "agent.context.read"]},
            token_principal="auth0|owner1",
        )
        self.assertEqual(status, "200 OK")
        self.assertIn("platform.owner", data["user"]["permissions"])
        self.assertEqual(self.store.count_active_principals_with_permission("tenant-planwell", "platform.owner"), 3)

    def test_last_owner_protection_prevents_removing_sole_owner(self) -> None:
        # First demote owner2 so only owner1 remains
        self._request(
            "POST",
            body={"email": "owner2@planwell.online", "permissions": ["agent.context.read"]},
            token_principal="auth0|owner1",
        )
        self.assertEqual(self.store.count_active_principals_with_permission("tenant-planwell", "platform.owner"), 1)

        # Now attempt to remove platform.owner from owner1 (the last owner)
        status, data = self._request(
            "POST",
            body={"email": "owner1@planwell.online", "permissions": ["agent.context.read"]},
            token_principal="auth0|owner1",
        )
        self.assertEqual(status, "400 Bad Request")
        self.assertEqual(data["error"], "cannot_remove_last_owner")
        # Ensure owner1 is still owner
        self.assertEqual(self.store.count_active_principals_with_permission("tenant-planwell", "platform.owner"), 1)


if __name__ == "__main__":
    unittest.main()

"""Auth0 access-token validation for protected backend routes."""

from __future__ import annotations

from typing import Any

import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError, PyJWKClientError, PyJWTError

from .b1 import AuthenticationError, IdentityContext, IdentityVerifier


class Auth0JwtVerifier(IdentityVerifier):
    """Verify Auth0 RS256 access tokens against the tenant JWKS endpoint.

    The Auth0 ``sub`` claim is an external identity reference.  Tenant and
    permission decisions intentionally remain outside this verifier.
    """

    def __init__(
        self,
        domain: str,
        audience: str,
        environment_ref: str,
        *,
        jwks_client: PyJWKClient | None = None,
        leeway_seconds: int = 60,
    ) -> None:
        normalized_domain = domain.removeprefix("https://").rstrip("/")
        if not normalized_domain or "/" in normalized_domain:
            raise ValueError("AUTH0_DOMAIN must be an Auth0 hostname")
        if not audience:
            raise ValueError("AUTH0_AUDIENCE must not be empty")
        if not environment_ref:
            raise ValueError("APP_ENV must not be empty")

        self._issuer = f"https://{normalized_domain}/"
        self._audience = audience
        self._environment_ref = environment_ref
        self._jwks_client = jwks_client or PyJWKClient(f"{self._issuer}.well-known/jwks.json")
        self._leeway_seconds = leeway_seconds

    def verify(self, authorization: str | None) -> IdentityContext:
        token = _bearer_token(authorization)
        try:
            header = jwt.get_unverified_header(token)
            if header.get("alg") != "RS256" or not header.get("kid"):
                raise AuthenticationError("unsupported_token_header")
            signing_key = self._jwks_client.get_signing_key_from_jwt(token).key
            claims: dict[str, Any] = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=self._audience,
                issuer=self._issuer,
                leeway=self._leeway_seconds,
                options={"require": ["exp", "iat", "sub"]},
            )
            subject = claims["sub"]
            issued_at = claims["iat"]
            if not isinstance(subject, str) or not subject or isinstance(issued_at, bool):
                raise AuthenticationError("invalid_identity_claims")
            if not isinstance(issued_at, int):
                raise AuthenticationError("invalid_identity_claims")
            scope = claims.get("scope", "")
            permissions = claims.get("permissions", [])
            if not isinstance(scope, str) or not isinstance(permissions, list) or not all(
                isinstance(permission, str) for permission in permissions
            ):
                raise AuthenticationError("invalid_permission_claims")
            return IdentityContext(
                principal_ref=subject,
                principal_type="human",
                issuer_ref=self._issuer,
                environment_ref=self._environment_ref,
                authenticated_at=issued_at,
                granted_permissions=frozenset(scope.split()).union(permissions),
            )
        except AuthenticationError:
            raise
        except (
            InvalidTokenError,
            PyJWKClientError,
            PyJWTError,
            KeyError,
            TypeError,
            ValueError,
            OSError,
            RuntimeError,
        ) as error:
            raise AuthenticationError("invalid_auth0_token") from error


def _bearer_token(authorization: str | None) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise AuthenticationError("missing_bearer_token")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise AuthenticationError("missing_bearer_token")
    return token

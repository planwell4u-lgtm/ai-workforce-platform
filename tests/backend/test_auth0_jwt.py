"""Auth0 JWT validation tests using locally generated RS256 signing keys."""

from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path
from unittest.mock import Mock

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from ai_workforce_backend.auth0 import Auth0JwtVerifier
from ai_workforce_backend.b1 import AuthenticationError

DOMAIN = "example-staging.us.auth0.com"
ISSUER = f"https://{DOMAIN}/"
AUDIENCE = "https://my-saas-app/"


class Auth0JwtVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.jwks_client = Mock()
        self.jwks_client.get_signing_key_from_jwt.return_value = Mock(key=self.private_key.public_key())
        self.verifier = Auth0JwtVerifier(
            DOMAIN, AUDIENCE, "staging", jwks_client=self.jwks_client
        )

    def token(self, **changes: object) -> str:
        now = int(time.time())
        claims: dict[str, object] = {
            "iss": ISSUER,
            "sub": "auth0|user-123",
            "aud": AUDIENCE,
            "iat": now,
            "exp": now + 300,
        }
        claims.update(changes)
        return jwt.encode(claims, self.private_key, algorithm="RS256", headers={"kid": "test-key"})

    def test_valid_token_establishes_issuer_bound_human_identity(self) -> None:
        identity = self.verifier.verify(f"Bearer {self.token()}")
        self.assertEqual(identity.principal_ref, "auth0|user-123")
        self.assertEqual(identity.principal_type, "human")
        self.assertEqual(identity.issuer_ref, ISSUER)
        self.assertEqual(identity.environment_ref, "staging")

    def test_wrong_issuer_audience_expiry_and_algorithm_are_rejected(self) -> None:
        invalid_tokens = (
            self.token(iss="https://other.us.auth0.com/"),
            self.token(aud="https://other-api/"),
            self.token(exp=int(time.time()) - 61),
            jwt.encode(
                {"iss": ISSUER, "sub": "auth0|user-123", "aud": AUDIENCE, "iat": 1, "exp": 2},
                "not-an-rsa-key-with-at-least-thirty-two-bytes",
                algorithm="HS256",
                headers={"kid": "test-key"},
            ),
        )
        for token in invalid_tokens:
            with self.subTest(token=token[:12]), self.assertRaises(AuthenticationError):
                self.verifier.verify(f"Bearer {token}")

    def test_missing_bearer_token_or_jwks_failure_is_rejected(self) -> None:
        with self.assertRaises(AuthenticationError):
            self.verifier.verify(None)
        self.jwks_client.get_signing_key_from_jwt.side_effect = RuntimeError("unavailable")
        with self.assertRaises(AuthenticationError):
            self.verifier.verify(f"Bearer {self.token()}")

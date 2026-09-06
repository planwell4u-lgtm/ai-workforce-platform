"""Unit tests for SystemHealthApi and Webhook HMAC signature verification."""

import json
import unittest
from unittest.mock import MagicMock

from ai_workforce_backend.system_health import SystemHealthApi
from ai_workforce_digital_channel.whatsapp_adapter import WhatsAppCloudAdapter


class TestWhatsAppHmacSignature(unittest.TestCase):
    def test_valid_hmac_signature(self) -> None:
        payload = b'{"object":"whatsapp_business_account"}'
        secret = "meta_app_secret_key_123"
        # Generate expected hmac
        import hashlib
        import hmac
        expected_sig = "sha256=" + hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

        is_valid = WhatsAppCloudAdapter.validate_hmac_signature(payload, expected_sig, secret)
        self.assertTrue(is_valid)

    def test_invalid_hmac_signature(self) -> None:
        payload = b'{"object":"whatsapp_business_account"}'
        secret = "meta_app_secret_key_123"
        bad_sig = "sha256=invalid_hash_value"

        is_valid = WhatsAppCloudAdapter.validate_hmac_signature(payload, bad_sig, secret)
        self.assertFalse(is_valid)


class TestSystemHealthApi(unittest.TestCase):
    def setUp(self) -> None:
        self.verifier = MagicMock()
        self.memberships = MagicMock()
        self.store = MagicMock()
        self.audit_sink = MagicMock()
        self.cache = MagicMock()

        principal = MagicMock()
        principal.principal_ref = "auth0|owner"
        self.verifier.verify.return_value = principal

        membership = MagicMock()
        membership.tenant_ref = "staging-demo"
        membership.permissions = frozenset({"platform.owner"})
        self.memberships.resolve.return_value = membership

        self.cache.is_available.return_value = True

        self.api = SystemHealthApi(
            self.verifier,
            self.memberships,
            self.store,
            self.audit_sink,
            self.cache,
        )

    def test_get_system_health(self) -> None:
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/v1/owner/system-health",
            "HTTP_AUTHORIZATION": "Bearer token",
        }
        captured_status = []

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured_status.append(int(status.split()[0]))

        response = self.api(environ, start_response)
        self.assertEqual(captured_status[0], 200)
        data = json.loads(response[0].decode("utf-8"))
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["database"]["status"], "healthy")
        self.assertEqual(data["cache"]["provider"], "redis")


if __name__ == "__main__":
    unittest.main()

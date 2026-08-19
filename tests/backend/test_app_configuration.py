"""Backend composition configuration tests."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "backend" / "src"))

from ai_workforce_backend.app import create_app


class BackendConfigurationTests(unittest.TestCase):
    def test_auth0_configuration_is_required(self) -> None:
        with (
            patch.dict(os.environ, {}, clear=True),
            self.assertRaisesRegex(RuntimeError, "AUTH0_DOMAIN"),
        ):
            create_app()

    def test_auth0_configuration_creates_the_protected_api(self) -> None:
        with (
            patch.dict(
                os.environ,
                {
                    "AUTH0_DOMAIN": "example.us.auth0.com",
                    "AUTH0_AUDIENCE": "https://api.example/",
                    "APP_ENV": "staging",
                    "SUPPORT_FAQ_PATH": str(
                        ROOT
                        / "packages"
                        / "agent"
                        / "knowledge"
                        / "staging-demo"
                        / "approved-support-faqs.jsonl"
                    ),
                    "SUPPORT_TENANT_REF": "staging-demo",
                },
                clear=True,
            ),
            patch("ai_workforce_backend.app.create_tenant_store", return_value=Mock()),
            patch(
                "ai_workforce_backend.app.create_jira_support_ticket_action", return_value=Mock()
            ),
        ):
            self.assertEqual(create_app().route_ref, "platform.foundation.tenant-context.v1")

"""Safety tests for the disabled-by-default outbound pilot boundary."""

from __future__ import annotations

import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "integration" / "python" / "src"))

from ai_workforce_integration.outbound_pilot import (
    PILOT_GREETING,
    OutboundPilotDenied,
    OutboundPilotPolicy,
    OutboundPilotRequest,
    TwilioOutboundPilotClient,
)


class OutboundPilotPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = OutboundPilotPolicy("+12402159529", "+12406798305")
        self.request = OutboundPilotRequest(
            "+12402159529", "+12406798305", PILOT_GREETING, True, True
        )

    def test_final_approval_is_required_before_any_provider_call(self) -> None:
        with self.assertRaisesRegex(OutboundPilotDenied, "final_approval_required"):
            self.policy.authorize(self.request, datetime(2026, 8, 24, 18, 30))

    def test_authorized_call_is_limited_to_the_approved_numbers_greeting_and_hours(self) -> None:
        authorized = OutboundPilotRequest(
            "+12402159529", "+12406798305", PILOT_GREETING, True, True, True
        )
        self.policy.authorize(authorized, datetime(2026, 8, 24, 18, 30))
        with self.assertRaisesRegex(OutboundPilotDenied, "outside_recipient_quiet_hours"):
            self.policy.authorize(authorized, datetime(2026, 8, 24, 22, 0))

    def test_client_requires_the_three_dedicated_api_key_settings(self) -> None:
        with self.assertRaisesRegex(ValueError, "configuration is required"):
            TwilioOutboundPilotClient.from_environment({}, lambda request, timeout: None)

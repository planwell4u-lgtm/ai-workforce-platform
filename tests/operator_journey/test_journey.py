from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "operator" / "python" / "src"))
from ai_workforce_operator.journey import (
    EscalationRequest,
    OperatorDenied,
    OperatorJourney,
    OperatorView,
)


class OperatorJourneyTests(unittest.TestCase):
    def test_tenant_aware_view_and_escalation(self) -> None:
        journey = OperatorJourney()
        view = OperatorView("tenant-a", "agent:v1", "conversation-a", "uncertain")
        self.assertEqual(journey.view(view, "tenant-a", frozenset({"operator.status.read"})), view)
        request = EscalationRequest("tenant-a", "conversation-a", "ticket-1", "review timeout")
        self.assertEqual(
            journey.request_escalation(
                request, "tenant-a", frozenset({"operator.support-ticket.escalate"})
            ),
            "requested",
        )
        with self.assertRaises(OperatorDenied):
            journey.view(view, "tenant-b", frozenset({"operator.status.read"}))

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "integration" / "python" / "src"))

from ai_workforce_integration.support_ticket import (
    ActionDenied,
    LocalSupportTicketAction,
    SupportTicketRequest,
)


class SupportTicketActionTests(unittest.TestCase):
    def test_authorization_idempotency_and_uncertainty(self) -> None:
        action = LocalSupportTicketAction()
        request = SupportTicketRequest("tenant-a", "conversation-a", "request-1", "Need support")
        with self.assertRaises(ActionDenied):
            action.request(request, frozenset())
        pending = action.request(request, frozenset({"integration.support-ticket.create"}))
        self.assertEqual(pending.outcome, "pending")
        self.assertEqual(
            action.request(request, frozenset({"integration.support-ticket.create"})), pending
        )
        self.assertEqual(action.reconcile("request-1", "timeout").outcome, "uncertain")
        self.assertEqual(action.reconcile("request-1", "accepted").outcome, "uncertain")

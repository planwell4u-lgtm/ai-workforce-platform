"""Tests for the realtime agent's read-only FAQ context gate."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "apps" / "realtime-support-agent" / "faq_context.py"
SPEC = importlib.util.spec_from_file_location("realtime_faq_context", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ApprovedFaqContextTests(unittest.TestCase):
    def test_accepts_only_the_explicit_approved_faq_shape(self) -> None:
        metadata = json.dumps(
            {
                "mode": "support-faq",
                "source_ref": "support-faqs:v1:2",
                "support_context": "Sign in and check Order History for tracking details.",
            }
        )

        self.assertEqual(
            MODULE.approved_faq_context(metadata),
            "Sign in and check Order History for tracking details.",
        )

    def test_rejects_missing_or_untrusted_context(self) -> None:
        self.assertIsNone(MODULE.approved_faq_context("not-json"))
        self.assertIsNone(MODULE.approved_faq_context(json.dumps({"mode": "other"})))
        self.assertIsNone(
            MODULE.approved_faq_context(
                json.dumps({"mode": "support-faq", "source_ref": "faq:v1", "support_context": " "})
            )
        )
        self.assertIsNone(
            MODULE.approved_faq_context(
                json.dumps(
                    {
                        "mode": "support-faq",
                        "source_ref": "faq:v1",
                        "support_context": "x" * (MODULE.MAX_CONTEXT_CHARACTERS + 1),
                    }
                )
            )
        )

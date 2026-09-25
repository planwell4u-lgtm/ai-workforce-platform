"""Validate the single approved FAQ excerpt carried in LiveKit job metadata."""

from __future__ import annotations

import json
from typing import Final

MAX_CONTEXT_CHARACTERS: Final = 24_000


def approved_faq_context(metadata: str) -> str | None:
    """Return only a bounded, explicitly-labelled approved FAQ excerpt.

    Any absent, malformed, oversized, or differently scoped metadata is ignored.
    The caller then retains the generic safe-unavailable behavior.
    """

    try:
        payload = json.loads(metadata)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("mode") != "support-faq":
        return None
    source_ref = payload.get("source_ref")
    excerpt = payload.get("support_context")
    if not isinstance(source_ref, str) or not source_ref.strip():
        return None
    if not isinstance(excerpt, str):
        return None
    bounded_excerpt = excerpt.strip()
    if not bounded_excerpt or len(bounded_excerpt) > MAX_CONTEXT_CHARACTERS:
        return None
    return bounded_excerpt

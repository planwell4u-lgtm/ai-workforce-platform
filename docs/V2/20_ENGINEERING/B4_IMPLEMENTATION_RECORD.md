# B4 Implementation Record — Canonical Conversation and Turn Control

**Status:** Implemented locally; persistence integration follows the B2 adapter boundary.  
**Date:** 2026-08-10

- A Conversation has one tenant, one session, and one canonical reference.
- Events require correlation and contiguous ordering; repeated event identifiers are idempotent.
- A single active turn owns execution at a time. Competing or incorrectly completed turns fail closed.
- Terminal outcomes keep `succeeded`, `failed`, and `uncertain` distinct; uncertainty is never reported as success.
- Tests cover duplicate/out-of-order messages, competing turns, scope conflict, and uncertain recovery state.

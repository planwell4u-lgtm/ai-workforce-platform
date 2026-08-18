# LiveKit Voice Agent Starter Reference

**Date:** 2026-08-17  
**Status:** Reference only — implementation deferred to B6

## Source

- [LiveKit Examples organization](https://github.com/livekit-examples) — general discovery catalog for future B6 implementation decisions.
- [LiveKit + Supabase Voice Agent Starter](https://github.com/livekit-examples/supabase-hacker-starter)
- [LiveKit Agents Starter — Python](https://github.com/livekit-examples/agent-starter-python)
- [LiveKit Python Agents Examples](https://github.com/livekit-examples/python-agents-examples)

## Purpose

This public starter is a design and implementation reference for the first
LiveKit voice path. It is not a dependency to clone into this repository and
must not replace the established platform boundaries.

## Candidate Concepts for B6

- The Python LiveKit agent structure from `agent-starter-python` is the
  preferred reference for `apps/voice-agent-worker`.
- Turn detection, background-noise handling, agent evaluations, and
  voice-session lifecycle patterns from the Python starter.
- Focused implementation examples for listen/respond, verified context
  variables, tool calling, event monitoring, content filtering, SIP lifecycle,
  and warm handoff from the Python examples library.
- Python LiveKit Agent runtime structure.
- Voice session lifecycle and end-of-session reporting.
- Governed knowledge retrieval patterns.
- Session-scoped memory patterns.

## Required Platform Boundaries

- Auth0 remains the human identity provider; do not adopt the starter's
  Supabase anonymous-auth flow.
- The backend remains responsible for verified tenant membership and
  authorization; do not trust browser-supplied user or tenant identifiers.
- The B4 canonical Conversation/session record remains the source of truth for
  Digital Channel and Voice activity.
- Supabase secret keys remain server-side only. Every agent query must use a
  verified tenant scope and the approved Data boundaries.
- Starter migrations, RLS policies, sample users, orders, and frontend are not
  approved for direct reuse.

## Adoption Gate

Review the relevant Python-agent and session-report components only after B4
Canonical Conversation and Turn Control is complete. Any implementation must
then satisfy the B6 voice acceptance criteria, including interruption,
disconnect, delivery, and duplicate-response safety.

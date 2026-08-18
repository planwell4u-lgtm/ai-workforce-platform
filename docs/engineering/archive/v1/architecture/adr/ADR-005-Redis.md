# ADR 005: Redis for Caching and Session State

## Context
Voice pipelines and chat sessions need very fast read/write access to session state and caching of common lookups.

## Decision
We will deploy Redis as the platform's distributed cache and session store.

## Consequences
- Fast session retrieval for latency-sensitive voice calls.
- Simplifies scaling backend services horizontally.

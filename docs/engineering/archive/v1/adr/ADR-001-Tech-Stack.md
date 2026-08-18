# ADR-001: Core Technology Stack

## Status

Accepted

## Context

We need to establish the core tech stack for our application to support reliable, fast, and scalable development.

## Decision

- **Backend:** Node.js (TypeScript) & Go for high-performance microservices.
- **Frontend:** Next.js (React) for server-side rendering, SEO, and fast response times.
- **Database:** PostgreSQL for relational data and transactional integrity, with Redis for speed caching.

## Consequences

- Teams must be fluent in TypeScript and Go.
- Uniform deployment configurations will target containerized environments (Docker/Kubernetes).

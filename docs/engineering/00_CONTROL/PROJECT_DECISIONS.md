# PROJECT_DECISIONS

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document records project-wide engineering decisions that govern the implementation of the Voice Agent SaaS Platform.

Unlike Architecture Decision Records (ADRs), which document significant architectural choices, this file captures stable engineering conventions, implementation policies, and repository-wide standards that every contributor must follow.

These decisions are considered authoritative unless superseded by a future update or a related ADR.

---

# Guiding Principles

1. Production-first architecture.
2. Documentation before implementation.
3. Security by default.
4. Multi-tenancy is a core requirement.
5. Prefer simplicity over unnecessary complexity.
6. Favor maintainability over premature optimization.
7. Repository documentation is the single source of truth.

---

# Technology Stack

## Frontend

- Next.js (App Router)
- React
- TypeScript (Strict Mode)
- Tailwind CSS
- shadcn/ui

---

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

---

## Database

Primary Database

- PostgreSQL

Extensions

- pgvector

---

## Cache

- Redis

Redis is used for:

- Caching
- Session data
- Distributed locking
- Queue support
- Rate limiting
- Temporary conversation state

Redis is **not** the system of record.

---

## AI Platform

- OpenAI Models
- LangChain
- LangGraph

---

## Voice Platform

- Twilio
- LiveKit

---

## Infrastructure

Containerization

- Docker

Orchestration

- Kubernetes (production)

CI/CD

- GitHub Actions

---

# Multi-Tenant Policy

The platform is tenant-first.

Every business entity must belong to a tenant unless explicitly documented otherwise.

Examples:

- Users
- Agents
- Knowledge Bases
- Calls
- Campaigns
- Prompts
- Workflows
- Memory
- Analytics

Every query must enforce tenant isolation.

---

# Identifier Strategy

Primary identifiers:

- UUIDv7

External identifiers retain provider formats.

Examples:

- Twilio Call SID
- LiveKit Room ID
- Stripe IDs

UUIDs should never be exposed unnecessarily in public APIs when a domain-specific identifier is more appropriate.

---

# Time Policy

- Store all timestamps in UTC.
- Convert to local time only at presentation.
- Use ISO-8601 formatting for APIs.
- Never store local time in the database.

---

# Database Rules

## Soft Deletes

Business entities should support soft deletion where appropriate.

Use:

- deleted_at

Do not physically remove records unless required.

---

## Audit Fields

Standard audit fields:

- created_at
- updated_at
- deleted_at
- created_by
- updated_by

---

## Foreign Keys

Always use foreign key constraints unless there is a documented performance reason not to.

---

## Transactions

Business operations spanning multiple tables must use database transactions.

---

## Migrations

Schema changes must be managed exclusively through Alembic migrations.

Direct production schema modifications are prohibited.

---

# API Standards

REST APIs use:

- JSON
- HTTPS
- Versioned endpoints

Example:

/api/v1/

---

## Standard Headers

Every request should support:

- X-Request-ID
- X-Correlation-ID
- Idempotency-Key (where applicable)

---

## Error Responses

Use a consistent error structure.

Every error response should include:

- error_code
- message
- request_id
- details (optional)

---

## Pagination

List endpoints should support:

- page
- page_size

Large datasets should support cursor pagination when appropriate.

---

# Authentication

Authentication

- JWT

Authorization

- Role-Based Access Control (RBAC)

Future support:

- Attribute-Based Access Control (ABAC)

---

# Logging

Structured JSON logging only.

Every log should include:

- timestamp
- request_id
- correlation_id
- tenant_id (when applicable)
- user_id (when applicable)
- service
- severity

Never log:

- Passwords
- API keys
- Access tokens
- Refresh tokens
- Sensitive personal information

---

# Observability

Every service should expose:

- Health endpoint
- Metrics endpoint
- Readiness check
- Liveness check

Distributed tracing should be supported.

---

# Security

All communication must use TLS.

Secrets must never be committed to Git.

Secrets should be managed through secure secret management.

Principle of least privilege applies to every service.

---

# AI Platform Rules

Prompt templates must be versioned.

Knowledge retrieval should be deterministic where possible.

Every AI response should include sufficient metadata for tracing.

Prompt engineering should be centralized.

Model selection should be configurable.

---

# RAG Rules

Knowledge sources must be versioned.

Embeddings should be regenerated only when content changes.

Chunking strategy must be documented.

Vector searches should support metadata filtering.

Tenant isolation applies to vector search.

---

# Voice Platform Rules

Every call must generate a unique internal Call ID.

Provider identifiers must be preserved.

Call state transitions must be recorded.

Call events must be auditable.

Recording metadata must be retained even if recordings expire.

---

# Background Jobs

Background work should be idempotent.

Jobs must support retries.

Failures should be observable.

Dead-letter queues should be supported.

---

# Configuration

Configuration hierarchy:

1. Environment variables
2. Secret manager
3. Configuration files

Configuration values must never be hardcoded.

---

# Documentation Policy

Architecture changes require documentation updates.

Major decisions require an ADR.

Implementation changes affecting users must update the changelog.

Session work must update:

- PROJECT_STATE.md
- SESSION_LOG.md

---

# Testing Policy

Every production feature should include:

- Unit tests
- Integration tests

Critical workflows should include:

- End-to-end tests

Performance testing is required for:

- Voice pipeline
- AI inference
- Database queries
- Vector search

---

# Repository Rules

Feature branches should follow a consistent naming convention.

Every pull request should include:

- Description
- Testing evidence
- Documentation updates (if applicable)

Generated files should not be manually edited unless documented.

---

# Change Management

Updates to this document should be:

- Reviewed
- Versioned
- Recorded in the changelog

Breaking project-wide policy changes should reference an ADR.

---

# Future Decisions

The following areas may require future policy updates:

- Billing strategy
- Marketplace architecture
- Plugin ecosystem
- Workflow engine
- AI model routing
- Multi-region deployment
- Disaster recovery
- Compliance (SOC 2, HIPAA, GDPR)

---

# Summary

This document defines the engineering rules that keep the Voice Agent SaaS Platform consistent, maintainable, secure, and production-ready.

All contributors—human and AI—must follow these decisions unless a newer version or an approved ADR explicitly overrides them.
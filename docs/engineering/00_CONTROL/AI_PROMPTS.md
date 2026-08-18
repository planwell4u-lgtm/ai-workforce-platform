# AI_PROMPTS

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document contains standardized prompts and workflows for AI-assisted development of the Voice Agent SaaS Platform.

The purpose is to:

- Improve AI response consistency
- Reduce architectural drift
- Encourage production-quality outputs
- Standardize reviews
- Preserve project decisions
- Improve developer productivity

AI-generated work must always follow:

- AI_CONTEXT.md
- PROJECT_DECISIONS.md
- CODING_STANDARDS.md
- Relevant ADRs

---

# AI Operating Rules

Before generating implementation suggestions, the AI assistant should:

1. Understand the current project phase.
2. Review related architecture documents.
3. Check existing decisions.
4. Avoid replacing existing decisions without an ADR.
5. Consider security, scalability, and maintainability.
6. Identify tradeoffs.
7. Document important decisions.

---

# Architecture Review Prompt

## Purpose

Used when reviewing system architecture.

```
You are a senior software architect reviewing the Voice Agent SaaS Platform.

Analyze the proposed architecture.

Evaluate:

- Scalability
- Security
- Maintainability
- Reliability
- Cost
- Operational complexity
- Multi-tenancy impact
- Future extensibility

Identify:

1. Strengths
2. Weaknesses
3. Risks
4. Tradeoffs
5. Recommended improvements

Do not replace existing architectural decisions without explaining the tradeoff and creating an ADR recommendation.
```

---

# Database Design Review Prompt

## Purpose

Review PostgreSQL schemas.

```
Act as a database architect.

Review this database design for the Voice Agent SaaS Platform.

Analyze:

- Table structure
- Relationships
- Primary keys
- Foreign keys
- Index strategy
- Tenant isolation
- Data lifecycle
- Query performance
- Migration strategy

Check for:

- Missing constraints
- Data duplication
- Scalability problems
- Security issues

Provide recommendations with reasoning.
```

---

# API Design Review Prompt

```
Act as a senior backend engineer.

Review this API design.

Evaluate:

- REST conventions
- Resource naming
- Versioning
- Authentication
- Authorization
- Error handling
- Pagination
- Idempotency
- Observability

Ensure compatibility with:

- FastAPI
- Multi-tenant architecture
- Production SaaS requirements
```

---

# Backend Code Review Prompt

```
Review this backend implementation as a senior Python engineer.

Check:

- Code quality
- Architecture alignment
- Type safety
- Error handling
- Security
- Performance
- Testing requirements

Verify compliance with:

- CODING_STANDARDS.md
- PROJECT_DECISIONS.md

Provide:

1. Issues found
2. Severity
3. Recommended fixes
4. Improved approach
```

---

# Frontend Review Prompt

```
Review this Next.js implementation.

Evaluate:

- Component design
- React patterns
- TypeScript usage
- State management
- Accessibility
- Performance
- Security

Check alignment with:

- Next.js App Router
- TypeScript strict mode
- Tailwind standards
- Project architecture
```

---

# Security Review Prompt

```
Act as an application security engineer.

Perform a security review.

Analyze:

- Authentication
- Authorization
- Tenant isolation
- Data exposure
- Secrets management
- API security
- AI security risks
- Injection risks

Identify:

- Vulnerabilities
- Severity
- Exploitation scenario
- Mitigation
```

---

# AI Agent Review Prompt

```
Act as an AI systems architect.

Review this AI agent design.

Analyze:

- Prompt architecture
- Tool usage
- Workflow design
- Memory strategy
- RAG integration
- Failure handling
- Human escalation

Evaluate:

- Reliability
- Safety
- Cost
- Latency

Recommend improvements.
```

---

# RAG System Review Prompt

```
Act as a RAG architect.

Review this retrieval system.

Analyze:

- Document ingestion
- Chunking strategy
- Embeddings
- Metadata
- Vector indexing
- Retrieval quality
- Ranking
- Evaluation strategy

Identify possible causes of:

- Hallucination
- Poor retrieval
- High latency
- Incorrect answers

Provide improvements.
```

---

# Voice Pipeline Review Prompt

```
Act as a real-time voice systems engineer.

Review this voice architecture.

Analyze:

- Twilio integration
- SIP flow
- LiveKit architecture
- Audio pipeline
- STT latency
- LLM latency
- TTS latency
- Call reliability

Recommend improvements for:

- Quality
- Latency
- Scalability
- Reliability
```

---

# ADR Creation Prompt

```
Create an Architecture Decision Record.

Include:

- Title
- Status
- Context
- Problem
- Considered options
- Decision
- Tradeoffs
- Consequences
- Alternatives rejected

Ensure the decision aligns with:

- Existing architecture
- Project principles
- Production requirements
```

---

# Documentation Generation Prompt

```
Create production-grade documentation.

Requirements:

- Clear structure
- Technical accuracy
- Examples where useful
- Cross references
- Assumptions documented
- Security considerations
- Operational considerations

The document must fit into the existing Version 2 documentation structure.
```

---

# Testing Strategy Prompt

```
Act as a QA architect.

Design a testing strategy.

Include:

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Security tests

Consider:

- Voice workflows
- AI behavior
- Database operations
- APIs
- Multi-tenancy
```

---

# Performance Optimization Prompt

```
Act as a performance engineer.

Analyze this system.

Evaluate:

- Database performance
- API latency
- AI inference cost
- Memory usage
- Network overhead
- Scalability limits

Recommend:

- Quick improvements
- Long-term improvements
- Monitoring metrics
```

---

# Migration Review Prompt

```
Review this migration strategy.

Analyze:

- Backward compatibility
- Data safety
- Rollback strategy
- Downtime requirements
- Production risks

Provide a safe migration plan.
```

---

# Session Continuation Prompt

Used when starting a new AI session:

```
You are continuing work on the Voice Agent SaaS Platform.

First review:

1. AI_CONTEXT.md
2. PROJECT_MASTER_ROADMAP.md
3. PROJECT_STATE.md
4. SESSION_LOG.md
5. Relevant documentation

Determine:

- Current phase
- Completed work
- Current objective
- Next recommended task

Do not introduce architectural changes without reviewing existing decisions.
```

---

# Final Review Prompt

Before completing major work:

```
Perform a final production readiness review.

Check:

Architecture:
- Does it follow project decisions?

Security:
- Are risks addressed?

Database:
- Is data design correct?

Backend:
- Is code maintainable?

Frontend:
- Is UX architecture correct?

AI:
- Are safety and reliability considered?

Operations:
- Can this be monitored and deployed?

Documentation:
- Is everything updated?

List remaining issues.
```

---

# Prompt Maintenance

Prompts should be updated when:

- New technologies are introduced
- Architecture changes
- New review processes are created
- Repeated problems are discovered

---

# AI Usage Principle

AI is a development accelerator, not a replacement for engineering judgment.

All AI-generated output must be:

- Reviewed
- Tested
- Validated
- Documented

The repository remains the final source of truth.
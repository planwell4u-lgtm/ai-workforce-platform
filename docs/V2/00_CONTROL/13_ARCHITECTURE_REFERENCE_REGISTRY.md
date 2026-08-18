# 13_ARCHITECTURE_REFERENCE_REGISTRY

**Version:** 2.3

**Status:** Active

---

# Overview

The Architecture Reference Registry maintains the approved external references used during the design, implementation, and evolution of the AI Workforce Platform.

These references provide architectural guidance, implementation patterns, industry standards, and best practices.

The registry does **not** replace internal architecture documentation.

The AI Workforce Platform remains independently designed around its own architectural principles.

External references are evaluated to improve the platform—not to define it.

---

# Purpose

This registry exists to:

- Maintain a trusted catalog of architectural references.
- Prevent reliance on outdated or unofficial resources.
- Encourage evidence-based architectural decisions.
- Record why external references are used.
- Document what concepts were adopted or intentionally rejected.
- Support consistent engineering decisions over the lifetime of the project.

---

# Guiding Principle

> **Adopt ideas, not architectures.**

Every external reference must be evaluated against the project's own principles.

External projects should inspire improvements, not dictate the design.

The platform architecture is always driven by:

- One Brain, Multi-Channel
- Multi-Tenant SaaS
- Modular Platform Architecture
- Documentation-First Development
- Long-Term Maintainability

---

# Reference Classification

Every reference belongs to one or more categories.

| Classification | Purpose |
|----------------|---------|
| Official Documentation | Primary technical source of truth |
| Official Starter Project | Production implementation patterns |
| Reference Architecture | High-level architectural guidance |
| Technical Standard | Industry specifications and protocols |
| Research Material | Academic or engineering research |
| Community Example | Inspiration only |
| Internal Prototype | Internal experiments and proof of concepts |

---

# Adoption Rules

External references may influence:

- Architecture
- Runtime design
- Integration patterns
- Testing strategies
- Deployment practices
- Operational processes

External references must **not** be copied without evaluation.

The following require architectural review:

- Project structure
- Technology choices
- Business logic
- Security model
- Data model
- Multi-tenant design

---

# Reference Review Process

Before adopting ideas from any external source:

1. Review the official documentation.
2. Review the implementation.
3. Compare with existing platform architecture.
4. Identify benefits and trade-offs.
5. Decide whether to:
   - Adopt
   - Adapt
   - Reject
6. Record significant decisions in the Decision Log if they have long-term architectural impact.

---

# Review Frequency

| Reference Type | Review Frequency |
|----------------|------------------|
| Official Documentation | Before each related module |
| Starter Projects | Before implementation |
| SDK Documentation | Before coding |
| Standards | When applicable |
| Research Material | As needed |
| Community Examples | Optional |

---

# Approved References

## LiveKit Examples Organization

### Classification

- Official Example Catalog

### Repository

https://github.com/livekit-examples

### Purpose

Official discovery source for current LiveKit-maintained starter projects, client examples, agent examples, media examples, and proof-of-concept patterns.

### Review Before

- Voice Platform implementation
- Agent Platform implementation
- Integration Platform implementation
- Frontend/mobile client proof-of-concept work

### Adoption Decision

May Use:

- Repository discovery and comparison during implementation planning
- Candidate selection for separate, bounded proof-of-concept work

Do Not Adopt:

- The organization catalog as a production technology decision
- Any individual example without a specific owner review, license check, security/data assessment, and bounded mapping to internal platform contracts

### Required Guardrail

Each chosen repository must be registered or cited separately with its intended role, adoption limits, and review evidence. Examples remain references; they do not replace the platform's architecture, tenant model, canonical Conversation ownership, security controls, or release process.

### Status

Active discovery reference; no individual repository is implicitly adopted.

---

## LiveKit

### Classification

- Official Documentation

### Purpose

Primary reference for:

- Voice Platform
- WebRTC
- SIP
- LiveKit Agents
- Realtime Sessions
- Deployment

### Review Before

- Voice Platform
- Agent Runtime
- Backend implementation

### Status

Active

### Adoption

Adopt:

- Official APIs
- Runtime recommendations
- Deployment guidance
- Integration patterns

Do Not Adopt Automatically:

- Internal implementation details
- Platform-specific business logic

---

## LiveKit Agent Starter (Python)

### Classification

- Official Starter Project

### Repository

https://github.com/livekit-examples/agent-starter-python

### Purpose

Reference implementation for:

- Agent Runtime
- Voice execution
- Production project structure
- Evaluation framework
- Deployment

### Review Before

- Agent Platform
- Backend
- Voice Platform

### Adoption Decision

Adopt:

- Runtime patterns
- Lifecycle management
- Testing concepts
- Production practices

Do Not Adopt:

- Complete repository structure
- SaaS architecture
- Business logic

### Status

Active

---

## LiveKit Supabase Hacker Starter

### Classification

- Official Starter Project
- Reference Architecture

### Repository

https://github.com/livekit-examples/supabase-hacker-starter

### Purpose

Restricted evaluation reference for:

- LiveKit voice-agent integration patterns
- Supabase-backed prototype patterns for RAG, memory, user context, function-tool CRUD, and session reporting
- Local development, test-fixture, and proof-of-concept structure

### Review Before

- Voice Platform implementation
- Integration Platform implementation
- Memory and Knowledge proof-of-concept work
- Platform Foundation, Data, and Security review for any Supabase-derived pattern

### Adoption Decision

May Evaluate and Adapt:

- Bounded LiveKit client/agent wiring
- Synthetic RAG, memory, session-report, and tool-CRUD fixtures
- Local developer workflow and test patterns

Do Not Adopt:

- Repository structure, database schema, or shared data model
- Secret-key access pattern, anonymous-identity model, or Supabase RLS policy as production policy
- Agent tool implementation, direct database access, or external-effect authorization design
- Overall SaaS architecture, tenant model, canonical Conversation state, or business workflow

### Required Guardrails

Any proof of concept using this starter must run in a separate sandbox with dedicated credentials, synthetic data, explicit tenant scope, no real participant contact, and no production data. Reuse requires a documented bounded mapping to the owning platform contract and current Security, Data, Testing, and Operations review.

### Status

Active as a restricted evaluation reference; not adopted for production implementation.

---

# Planned References

## Supabase

Classification:

- Official Documentation
- Approved Technology Reference

Purpose:

- Managed PostgreSQL data foundation
- Controlled PostgreSQL extension management, including pgvector
- Development and operational support for Data Platform-owned persistence

Approved Scope:

- Managed PostgreSQL for platform persistence, subject to Data Platform schema, migration, backup, recovery, residency, and portability controls
- `pgvector` for Data Platform-managed embedding storage and vector similarity retrieval serving approved Knowledge and Memory contracts
- Supabase Auth, Storage, Realtime, Edge Functions, and other product capabilities only after a separate platform-owner decision; they are not implicitly part of this selection

Do Not Use As:

- A substitute for Platform Foundation tenant/membership/entitlement ownership
- The authority for Security authorization, secret management, audit, or compliance policy
- A direct database path from Agent, Conversation, Voice, Digital Channel, or frontend code
- A replacement for Knowledge/Memory governance, canonical records, retention, deletion, or provider portability requirements

Review Before:

- Data Platform implementation
- Knowledge and Memory retrieval implementation
- Platform Foundation and Security review of any Supabase product beyond managed PostgreSQL and pgvector

Status:

Active approved data-stack reference; implementation remains subject to Data, Security, and Operations controls.

---

## pgvector

Classification:

- PostgreSQL Extension
- Approved Technology Reference

Purpose:

- Store embeddings and perform vector similarity search within the approved PostgreSQL foundation

Approved Scope:

- Data Platform-managed vector representations for approved Knowledge and Memory retrieval use cases
- Tenant/purpose-filtered retrieval through internal domain contracts

Do Not Use As:

- A canonical Knowledge or Memory record store
- An authorization, tenant-isolation, publication, admission, or lifecycle decision engine
- A direct retrieval dependency from Agent or channel code

Status:

Active approved extension within the PostgreSQL/Supabase data foundation.

---

## OpenAI

Classification:

- Official Documentation

Purpose:

- Responses API
- Realtime API
- Tool Calling
- Embeddings

Review Before:

- AI Platform

Status:

Planned

---

## LangGraph

Classification:

- Official Documentation

Purpose:

- Agent orchestration
- State management
- Workflow execution

Review Before:

- Agent Platform

Status:

Planned

---

## FastAPI

Classification:

- Official Documentation

Purpose:

- Backend architecture
- Dependency injection
- API design

Review Before:

- Backend Platform

Status:

Planned

---

## PostgreSQL

Classification:

- Official Documentation

Purpose:

- Core relational database foundation through Supabase-managed PostgreSQL
- Transactional persistence, schema/migration, and performance foundation for Data Platform-owned services

Review Before:

- Data Platform

Status:

Active approved data-stack reference; see Supabase and pgvector entries for defined scope.

---

## Kubernetes

Classification:

- Official Documentation

Purpose:

- Infrastructure
- Scaling
- Deployment

Review Before:

- Operations Platform

Status:

Planned

---

# Version Tracking

Where practical, references should record:

- Version reviewed
- Review date
- Major changes affecting the project
- Reviewer

This information is particularly important for:

- SDKs
- APIs
- Runtime frameworks
- Standards

---

# Reference Lifecycle

Every reference has one of the following states.

| Status | Meaning |
|---------|---------|
| Planned | Approved but not yet reviewed |
| Active | Currently approved for use |
| Deprecated | No longer recommended |
| Archived | Retained for historical context |
| Replaced | Superseded by another reference |

References should not be removed.

Historical records help explain previous architectural decisions.

---

# Evaluation Criteria

Before adopting any external idea, ask:

- Is this an official source?
- Is it actively maintained?
- Is it production ready?
- Does it align with One Brain, Multi-Channel?
- Does it improve maintainability?
- Does it simplify the platform?
- Does it preserve modularity?
- Does it improve security?
- Does it avoid unnecessary coupling?

Only adopt ideas that strengthen the overall architecture.

---

# Architecture Influence Log

| Date | Reference | Module | Decision | Status |
|------|-----------|--------|----------|--------|
| TBD | LiveKit Agent Starter | Agent Platform | Runtime reference only | Planned |
| 2026-08-06 | LiveKit Supabase Hacker Starter | Voice, Integration, Memory, Knowledge | Restricted evaluation reference only; assess bounded patterns in a separate sandbox | Active |
| 2026-08-06 | LiveKit Examples Organization | Voice, Agent, Integration, Frontend | Official discovery catalog; register individual examples before evaluation or adoption | Active |

---

# Related Documents

- README.md
- 02_PROJECT_ROADMAP.md
- 03_ARCHITECTURE_PRINCIPLES.md
- 08_DECISION_LOG.md
- 12_DEVELOPMENT_WORKFLOW.md

---

# Revision History

| Version | Date | Changes |
|----------|------|---------|
| 2.0 | 2026-08-04 | Initial Architecture Reference Registry. |
| 2.1 | 2026-08-06 | Clarified the LiveKit Supabase Hacker Starter as a restricted Voice/Integration/Memory/Knowledge evaluation reference with explicit non-adoption guardrails. |
| 2.2 | 2026-08-06 | Registered the official LiveKit Examples organization as a discovery reference with individual-repository review requirements. |
| 2.3 | 2026-08-06 | Approved Supabase-managed PostgreSQL and pgvector as the scoped shared data-stack reference, with Data, Security, and Operations controls retained. |

# 08_DECISION_LOG

**Version:** 2.3

**Status:** Approved

---

# Overview

This document records important architectural, technical, and strategic decisions made during the development of the AI Workforce Platform.

The Decision Log preserves the reasoning behind decisions so future contributors can understand:

- What was decided.
- Why it was decided.
- What alternatives were considered.
- What consequences resulted.

This document acts as the historical memory of the platform architecture.

---

# Purpose

The purpose of this document is to:

- Preserve architectural knowledge.
- Record important decisions.
- Prevent repeated discussions.
- Provide historical context.
- Support future changes.
- Improve decision transparency.

---

# Decision Management Principles

## Record Important Decisions

Not every decision requires an entry.

A decision should be recorded when it:

- Affects architecture.
- Changes system boundaries.
- Introduces a major technology direction.
- Creates long-term impact.
- Removes important alternatives.
- Influences future engineering choices.

---

## Capture Reasoning

A decision record should explain:

- The problem.
- The context.
- The chosen approach.
- Alternatives considered.
- Expected consequences.

The goal is not only to record the result, but to preserve the reasoning.

---

## Decisions Can Evolve

Previous decisions may change when:

- New information becomes available.
- Requirements change.
- Better approaches are discovered.

Changes must create a new decision record rather than modifying history.

---

# Decision Categories

Decisions are grouped into categories.

## Architecture Decisions

Examples:

- System structure
- Platform boundaries
- Communication patterns
- Design principles

---

## Technology Decisions

Examples:

- Framework selection
- Infrastructure choices
- External technology adoption

---

## Process Decisions

Examples:

- Development workflow
- Documentation practices
- Engineering processes

---

# Decision Ownership

Each decision must identify ownership.

The decision owner is responsible for:

- Maintaining decision accuracy.
- Reviewing future changes.
- Approving superseding decisions.
- Ensuring related documents remain aligned.

Decision ownership follows:

| Decision Category | Owner |
|---|---|
| Architecture Decisions | Architecture Owner |
| Technology Decisions | Relevant Platform Owner |
| Security Decisions | Security Owner |
| Data Decisions | Data Platform Owner |
| Process Decisions | Project Owner |

---

# Decision Lifecycle

```
Proposal

   ↓

Review

   ↓

Accepted Decision

   ↓

Implementation

   ↓

Review / Supersede
```

---

# Decision Status

| Status | Meaning |
|---|---|
| Proposed | Under discussion and evaluation |
| Accepted | Current active decision |
| Rejected | Evaluated but not selected |
| Superseded | Replaced by a newer decision |

---

# Impact Level

Each decision should identify its impact.

| Level | Meaning |
|---|---|
| Critical | Changes overall architecture or platform direction |
| Major | Affects multiple modules or systems |
| Minor | Limited impact within a specific area |

---

# Decision Record Format

Each decision follows this structure:

```markdown
# ADR-XXX: Decision Title

## Category

Architecture | Technology | Process

## Impact

Critical | Major | Minor

## Status

Proposed | Accepted | Rejected | Superseded

## Owner

Responsible owner.

## Date

YYYY-MM-DD

## Context

Problem or situation requiring a decision.

## Decision

Chosen approach.

## Alternatives Considered

Other options evaluated.

## Consequences

Expected benefits and trade-offs.

## Supersedes

Previous decisions replaced.

## Superseded By

Future decisions replacing this decision.

## Related Documents

References.
```

---

# Decision Index

| ID | Decision | Category | Impact | Status |
|---|---|---|---|---|
| ADR-001 | One Brain, Multi-Channel Architecture | Architecture | Critical | Accepted |
| ADR-002 | Modular Platform Architecture | Architecture | Critical | Accepted |
| ADR-003 | Documentation-First Development | Process | Major | Accepted |
| ADR-004 | Explicit Platform Foundation and Digital Channel Boundaries | Architecture | Major | Accepted |

---

# ADR-001: One Brain, Multi-Channel Architecture

## Category

Architecture

## Impact

Critical

## Status

Accepted

## Owner

Architecture Owner

## Date

2026-08-03

---

## Context

The platform needs to support multiple communication channels including:

- Voice
- Web Chat
- SMS
- WhatsApp
- Future channels

Traditional channel-specific architectures duplicate business intelligence inside each communication channel.

This creates:

- Inconsistent behavior.
- Higher maintenance cost.
- Difficult agent evolution.

---

## Decision

The platform will follow:

**One Brain, Multi-Channel Architecture**

A centralized Agent Brain owns:

- Reasoning
- Identity
- Personality
- Knowledge access
- Memory access
- Tool decisions

Channels provide communication interfaces only.

---

## Alternatives Considered

### Separate Intelligence Per Channel

Rejected because:

- Logic duplication.
- Different user experiences.
- Difficult maintenance.

---

### Channel-Centric Architecture

Rejected because:

- Business logic becomes coupled to communication methods.

---

## Consequences

Benefits:

- Consistent intelligence across channels.
- Faster channel expansion.
- Centralized improvements.

Trade-offs:

- Requires strong separation between intelligence and communication layers.

---

# ADR-002: Modular Platform Architecture

## Category

Architecture

## Impact

Critical

## Status

Accepted

## Owner

Architecture Owner

## Date

2026-08-03

---

## Context

The platform contains multiple capabilities:

- Agents
- Voice
- Knowledge
- Memory
- Integrations
- Security

A single tightly coupled system would limit independent evolution.

---

## Decision

The platform will be organized into independent capability platforms.

Each platform has:

- Clear responsibility.
- Defined boundaries.
- Independent evolution.

---

## Alternatives Considered

### Single Application Architecture

Rejected because:

- Creates tight coupling.
- Limits scalability.

---

### Fully Independent Microservices From Day One

Rejected because:

- Adds unnecessary operational complexity.

---

## Consequences

Benefits:

- Clear ownership.
- Better maintainability.
- Easier scaling.

Trade-offs:

- Requires disciplined boundaries.

---

# ADR-003: Documentation-First Development

## Category

Process

## Impact

Major

## Status

Accepted

## Owner

Project Owner

## Date

2026-08-03

---

## Context

The platform combines:

- AI systems.
- Voice infrastructure.
- Data systems.
- Cloud infrastructure.

Without documentation, architectural knowledge becomes fragmented.

---

## Decision

Major architecture and platform decisions must be documented before implementation.

Documentation is treated as an engineering asset.

---

## Alternatives Considered

### Code First, Document Later

Rejected because:

- Architecture becomes unclear.
- Knowledge depends on individuals.

---

## Consequences

Benefits:

- Better planning.
- Easier collaboration.
- Reduced architectural drift.

Trade-offs:

- Requires additional planning effort.

---

# ADR-004: Explicit Platform Foundation and Digital Channel Boundaries

## Category

Architecture

## Impact

Major

## Status

Accepted

## Owner

Architecture Owner

## Date

2026-08-06

---

## Context

The roadmap requires tenant/organization control-plane, configuration, API-edge, and non-voice multi-channel capabilities. These responsibilities were named as deliverables but had no single module owner. Leaving them implicit would either duplicate them across modules or make one platform an accidental owner.

## Decision

Establish Platform Foundation as the owner of tenant-aware control-plane, shared configuration, entitlement facts, API-edge policy, and service-discovery contracts. Establish Digital Channel Platform as the owner of non-voice channel adapters, delivery behavior, channel identities, and channel-specific consent evidence.

Security retains authentication, authorization, secrets, audit infrastructure, and compliance controls. Conversation remains canonical for interaction state. Integration retains generic connector infrastructure. Frontend retains experience composition. Voice remains the separate real-time voice channel.

## Alternatives Considered

### Distribute the responsibilities across existing modules

Rejected because it leaves no primary owner for shared control-plane and channel transport behavior, inviting duplicated policies and inconsistent tenant or delivery handling.

### Make Integration own all channels and control-plane responsibilities

Rejected because generic connector implementation differs from participant-channel delivery, and neither concern should own tenant and organization lifecycle.

## Consequences

Benefits:

- Every roadmap capability now has an explicit primary owner.
- Digital channels can expand without duplicating Conversation or Voice ownership.
- SaaS control-plane behavior can evolve independently of feature modules.

Trade-offs:

- Two new module document sets must be maintained.
- Cross-platform contracts require disciplined review before implementation.

---

# ADR-005: Supabase-Managed PostgreSQL and pgvector Data Foundation

## Category

Technology

## Impact

Major

## Status

Accepted

## Owner

Architecture Owner with Data Platform Owner

## Date

2026-08-06

---

## Context

The platform requires a relational data foundation and vector similarity capability for governed Knowledge and Memory retrieval. PostgreSQL was already identified as the database foundation, and the approved LiveKit reference ecosystem includes Supabase-based examples. A clear decision is needed so a starter project's incidental use of Supabase does not become an undocumented or overbroad architecture choice.

## Decision

Use Supabase-managed PostgreSQL as the approved shared data-stack reference and use the PostgreSQL `pgvector` extension for Data Platform-managed embedding storage and vector similarity retrieval.

This decision selects only the managed PostgreSQL and pgvector foundation. It does not automatically adopt Supabase Auth, Storage, Realtime, Edge Functions, database schema, RLS policy, secret-key patterns, or any starter-repository architecture. Data Platform owns physical data implementation; Knowledge and Memory own their domain contracts; Platform Foundation owns tenant control-plane facts; Security owns authorization, secrets, audit infrastructure, and compliance controls.

## Alternatives Considered

### Separate dedicated vector database

Deferred. A separate vector store may be evaluated later if scale, capability, or operational evidence requires it, but it would add a second persistence boundary without current need.

### Self-managed PostgreSQL from the outset

Deferred. It preserves hosting control but adds operational work before the platform's data and operational requirements have been implemented and validated.

### Adopt the Supabase starter architecture directly

Rejected. A starter project does not satisfy the platform's ownership, tenant, authorization, portability, lifecycle, and production-governance requirements.

## Consequences

Benefits:

- Establishes a consistent relational and vector foundation for implementation planning.
- Keeps vector retrieval close to governed PostgreSQL persistence.
- Enables a narrow initial RAG and Memory vertical slice without adopting a separate vector database.

Trade-offs:

- Data, Security, and Operations must define migration, residency, backup/recovery, access, portability, and extension/index operational controls before production use.
- Supabase product capabilities beyond PostgreSQL and pgvector remain separate decisions.

---

# Decision Maintenance Rules

Future decisions should:

- Reference existing decisions.
- Avoid contradicting accepted decisions without review.
- Document alternatives.
- Explain consequences.
- Create new records when replacing old decisions.

---

# Related Documents

- 03_ARCHITECTURE_PRINCIPLES.md
- 04_SYSTEM_BOUNDARIES.md
- 05_MODULE_OWNERSHIP.md
- 06_DOCUMENTATION_STANDARDS.md
- 09_CHANGE_MANAGEMENT.md

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-03 | Initial decision log structure. |
| 2.1 | 2026-08-03 | Added ownership, categories, impact levels, status definitions, and superseding rules. |
| 2.2 | 2026-08-06 | Recorded ADR-004 establishing Platform Foundation and Digital Channel Platform boundaries. |
| 2.3 | 2026-08-06 | Recorded ADR-005 selecting Supabase-managed PostgreSQL and pgvector as the scoped shared data foundation. |

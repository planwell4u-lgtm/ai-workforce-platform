# AI-Driven Enterprise SaaS Development Playbook

**Version:** 2.0  
**Status:** Approved  
**Owner:** Project Architecture Owner and Engineering Owner  
**Last Reviewed:** 2026-08-07  
**Review Frequency:** Quarterly during active development and after a material process change

---

# Overview

This playbook defines the operating procedure for humans and AI coding agents working on the AI Workforce Platform. It turns the platform's existing governance, architecture, change-management, and documentation standards into a repeatable implementation workflow.

It is an operating guide, not a second architecture specification. The authoritative documents named below govern product intent, system boundaries, module ownership, decisions, current state, and change approval.

---

# Purpose

Use this playbook to ensure that AI-assisted work is scoped, traceable, testable, secure, and recoverable from the repository six months or six years after it was performed.

The intended outcome is production-grade, multi-tenant SaaS delivery without undocumented decisions, duplicate capabilities, unreviewed AI-generated code, or reliance on chat history.

---

# Scope

This playbook applies to code, tests, migrations, infrastructure changes, operational configuration, and documentation created or changed with AI assistance.

It does not define product requirements, platform architecture, module boundaries, API contracts, database schemas, security controls, or release policy. Those belong to their authoritative documents.

---

# Authority and Source of Truth

The repository is the source of truth. Chat history and AI memory are working context only.

| Concern | Authoritative source |
|---|---|
| Product vision and objectives | `01_PROJECT_CHARTER.md` |
| Roadmap, phases, and milestones | `02_PROJECT_ROADMAP.md` |
| Architecture rules | `03_ARCHITECTURE_PRINCIPLES.md` |
| System boundaries and capability ownership | `04_SYSTEM_BOUNDARIES.md` |
| Module responsibilities | `05_MODULE_OWNERSHIP.md` |
| Documentation standards and lifecycle | `06_DOCUMENTATION_STANDARDS.md` |
| Documentation discovery and ownership map | `07_DOCUMENTATION_INDEX.md` |
| Significant decisions and their rationale | `08_DECISION_LOG.md` |
| Change approval process | `09_CHANGE_MANAGEMENT.md` |
| Current project state, risks, and priorities | `10_PROJECT_STATUS.md` |
| Shared terminology | `11_TERMINOLOGY_GLOSSARY.md` |
| Standard development lifecycle | `12_DEVELOPMENT_WORKFLOW.md` |
| Module-specific design and contracts | The applicable platform directory |

If this playbook conflicts with an approved source above, the source above prevails. Propose a documented change rather than resolving the conflict in code.

---

# Roles and Decision Rights

## Human Owner

The human owner approves product direction, material scope changes, architecture decisions, security-sensitive choices, external spend or vendor commitments, and production deployment.

## Architecture and Module Owners

Architecture and module owners resolve ownership conflicts, approve material changes in their domain, and maintain the governing documents.

## AI Coding Agent

The coding agent reads applicable repository context, proposes and implements a bounded change, writes and runs appropriate validation, identifies conflicts, and records evidence. It must not silently redefine architecture or make irreversible decisions.

---

# Agent Context Protocol

## Required Reading Order

Before a non-trivial change, an agent must read:

1. `PROJECT_CONTEXT.md` if present; otherwise `01_PROJECT_CHARTER.md` and this playbook.
2. `03_ARCHITECTURE_PRINCIPLES.md`, `04_SYSTEM_BOUNDARIES.md`, and `05_MODULE_OWNERSHIP.md`.
3. `10_PROJECT_STATUS.md`, relevant entries in `08_DECISION_LOG.md`, and the applicable roadmap milestone.
4. Relevant module documents, contracts, code, and tests.
5. `09_CHANGE_MANAGEMENT.md` for a material or production-sensitive change.

Read only the context needed for the task after the control layer. A large unrelated context window is not a substitute for identifying authoritative documents.

## Task Brief

Every non-trivial task must state:

- Objective and expected outcome
- Authoritative documents reviewed
- Owning and supporting modules
- In-scope and out-of-scope work
- Security, tenant, data, API, event, and operational constraints as applicable
- Acceptance criteria and validation required
- Required documentation or decision-log updates

If a required item is unknown, classify it as blocking, non-blocking, or deferred. Do not guess about ownership, tenant isolation, authorization, a source of truth, or a public contract.

---

# Change Classes and Minimum Gates

| Class | Typical work | Minimum gates |
|---|---|---|
| A — Local | Typo, focused test, small refactor, documentation clarification | Related validation; focused review; no unrelated cleanup |
| B — Feature | Endpoint, workflow node, UI capability, background job, connector capability | Written plan, tests, documentation alignment, architecture-consistency review |
| C — Architecture | New service, database, event backbone, runtime model, tenant strategy, authentication mechanism | Approved proposal, decision-log entry, impact and migration analysis, security and operational review |
| D — Production-critical | Identity, authorization, billing, data deletion/export, secrets, call routing/recording, migrations, deployment | Formal review, failure analysis, rollback or recovery plan, integration and security tests, staged-release evidence |

When unsure, use the higher class.

---

# Standard AI-Assisted Delivery Loop

## 1. Define and Locate Ownership

Confirm the problem, acceptance criteria, primary owner, supporting owners, data owner, interface owner, and operational owner. Stop for clarification when ownership is unclear.

## 2. Check for Existing Capability

Search relevant module documentation, code, tests, decisions, APIs, schemas, jobs, and events before creating an abstraction. Reuse the established owner and interface where one exists.

## 3. Plan Before Editing

For Class B–D changes, produce a file-level plan covering code, interfaces, data or migrations, authorization, tenant scope, observability, tests, documentation, and rollback or recovery where applicable. Identify decisions requiring approval before editing.

## 4. Implement the Smallest Complete Slice

Prefer a vertical slice that includes the domain behavior, persistence or interface change, validation, authorization, observability, and tests required to prove the change. Avoid speculative frameworks and broad unrelated refactors.

## 5. Validate and Review

Run the required formatter, linting, type checks, tests, contract checks, migration checks, security checks, and build checks that apply. Report every command run and every required check not run, with the reason.

Review the result for ownership, duplication, multi-tenancy, authorization, error and retry behavior, observability, maintainability, backward compatibility, and documentation alignment.

## 6. Record Durable State

Update affected documentation, `10_PROJECT_STATUS.md` when project state, risks, blockers, or next work changes, and `08_DECISION_LOG.md` when a material decision is made. Follow `09_CHANGE_MANAGEMENT.md` for approvals and history.

The closeout must let the next contributor understand the change without chat history: what changed, why, evidence, decisions, risks, assumptions, and the next action.

---

# Non-Negotiable Engineering Rules

- Every capability has one primary owning module; cross-module access uses documented interfaces, events, service APIs, or shared contracts.
- Tenant context must be established from trusted authentication or execution context. Tenant-owned data, caches, events, jobs, and observability must preserve isolation.
- Do not accept a tenant identifier from an untrusted request when trusted tenant context already exists.
- Do not add a service, database, message broker, framework, deployment pattern, authentication mechanism, platform-wide dependency, or new source of truth without the required review and decision record.
- Do not claim a check passed unless it was run. Do not suppress tests, validation, authorization, or errors merely to make a change pass.
- Do not log secrets or sensitive payloads. Follow applicable security and data-retention documents.
- Preserve backward compatibility unless its change is approved and a migration or release path is documented.
- Change generated artifacts only through their governing source, unless the repository explicitly says otherwise.

---

# Domain-Specific Review Prompts

Apply the following questions only when the change touches the domain; the platform documents define the detailed rules.

## Data and Migrations

Confirm data ownership, tenant scope, constraints, indexes, lifecycle and deletion behavior, migration upgrade and rollback/recovery behavior, realistic-volume impact, and documentation updates.

## APIs, Events, and Jobs

Confirm authentication, authorization, tenant scope, stable schemas, error behavior, idempotency, pagination or rate limiting where relevant, schema/version compatibility, correlation identifiers, retries, dead-letter or recovery behavior, and observability.

## Voice and Realtime

Confirm lifecycle states and transitions, timeouts, interruption and transfer handling, provider failure behavior, recording and consent, tenant ownership, data retention, regional compliance, latency, and cost visibility.

## AI Runtime and Tooling

Confirm versioned prompt/configuration sources, tool permissions, knowledge and memory access, model/fallback choice, cost and timeout limits, guardrails, evaluation evidence, audit traces, and retention implications. Tool execution must be permission-controlled, validated, timeout-bound, observable, and idempotent where possible.

---

# Definition of Ready

A feature is ready when its problem, scope, acceptance criteria, ownership, tenant and security behavior, data and interface impacts, dependencies, test strategy, and open decisions are known or explicitly deferred. Blocking ambiguity must be resolved before implementation.

# Definition of Done

A feature is done when approved scope and acceptance criteria are met; required validation has passed; tenant isolation, security, failure behavior, and observability are addressed; documentation and project state are aligned; known limitations are recorded; and a rollback or recovery path is understood where relevant.

---

# Required Change Evidence

Every Class B–D pull request or change record must include:

- Summary and rationale
- Owning module and authoritative documents reviewed
- Interfaces, schemas, events, migrations, and behavior changed
- Security, authorization, tenant, privacy, and audit implications
- Validation commands and results, including checks not run
- Documentation and decision records updated
- Compatibility, rollout, rollback/recovery, and known risks

---

# Anti-Patterns

Do not use AI for architecture-free bulk generation, documentation that is never consulted, chat-only continuity, hidden tenant assumptions, post-hoc testing, premature microservices, framework-first design, unreviewable multi-module edits, or temporary decisions that are not recorded.

---

# Six-Month Maintainability Rule

This playbook must remain executable by a contributor who did not participate in its creation. Therefore:

- Use stable responsibility-based references, not chat links or tool-specific memory.
- Keep detailed rules in their authoritative document and reference them here.
- Update the authority table when control-file names, owners, or locations change.
- Review this playbook after a new AI tool, material process failure, architecture change, or major project phase, and at least quarterly while active.
- Deprecate or redirect obsolete guidance rather than leaving conflicting instructions in place.

---

# Related Documents

- `03_ARCHITECTURE_PRINCIPLES.md`
- `04_SYSTEM_BOUNDARIES.md`
- `05_MODULE_OWNERSHIP.md`
- `06_DOCUMENTATION_STANDARDS.md`
- `07_DOCUMENTATION_INDEX.md`
- `08_DECISION_LOG.md`
- `09_CHANGE_MANAGEMENT.md`
- `10_PROJECT_STATUS.md`
- `12_DEVELOPMENT_WORKFLOW.md`

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Initial playbook. |
| 2.0 | 2026-08-07 | Finalized as a concise operating guide; replaced duplicate governance content with authoritative references, corrected the control-document map, added change classes, evidence requirements, and six-month maintenance rules. |

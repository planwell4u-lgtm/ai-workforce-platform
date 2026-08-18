# 08_ARCHITECTURE_PRINCIPLES_APPLICATION

**Title:** Architecture Principles Application Guide  
**Version:** 2.1  
**Status:** Approved

---

# Overview

This document turns the platform's approved architecture principles into practical design and implementation checks. It helps contributors apply One Brain, Multi-Channel; clear ownership; tenant isolation; API/event contracts; security by design; and production readiness consistently without creating a second source of architectural policy.

The authoritative principles remain in `00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md`; module documents define the detailed rules for their own domains.

# Purpose

This document exists to:

- Convert high-level architecture principles into feature and change decisions.
- Prevent duplicate ownership, hidden coupling, and implementation-driven boundary drift.
- Define minimum questions for interfaces, data, security, operations, and tests.
- Establish a repeatable review path for changes that need architecture or owner attention.
- Preserve decisions so implementation remains understandable six months from now.

# Application Model

```text
Proposed capability or change
        |
        v
Identify outcome, owner, scope, and authoritative contracts
        |
        v
Apply tenant, security, data, API/event, operational, and test checks
        |
        +--> Fits existing boundary: implement through owner contract
        +--> Material gap or conflict: change/architecture review
        |
        v
Validate evidence, document durable state, and monitor outcome
```

Architecture principles guide implementation. They do not authorize a contributor to change ownership, policy, data lifecycle, or public contracts without the required owner and change process.

# Principle-to-Decision Map

| Principle | Apply it by | Reject or escalate when |
|---|---|---|
| One Brain, Multi-Channel | Reuse the approved Agent, Conversation, channel, Knowledge, Memory, and Integration contracts for every interaction. | A channel proposes its own reasoning, prompt/tool loop, knowledge store, memory system, or canonical conversation. |
| Single capability ownership | Assign one primary module owner and identify supporting contracts. | Two modules persist the same canonical fact or make the same policy/behavior decision. |
| Multi-tenant first | Obtain tenant scope from trusted context; preserve it in records, jobs, events, caches, telemetry, and access checks. | Tenant scope is client-supplied, inferred from environment/provider identity, omitted in async work, or crossed for convenience. |
| API/event first | Use versioned APIs, events, or shared contracts with explicit error/outcome, authorization, correlation, and compatibility rules. | A module reads/writes another module's internal database or couples to an undocumented internal implementation. |
| Security by design | Apply current identity, authorization, secret, privacy, audit, and least-privilege controls before execution. | A shortcut requires client-side policy, shared credentials, broad access, hidden secrets, or an undocumented exception. |
| Data and lifecycle governance | Keep logical ownership with the domain and physical mechanisms with Data; define retention/deletion/recovery impact. | A feature introduces unowned storage, copies protected data without a purpose, or treats a cache/provider object as canonical fact. |
| Production readiness | Include failure behavior, observability, tests, operations, recovery, documentation, and rollout/reversal before production. | “We will add security/tests/monitoring later” is the only plan for a material capability. |
| Configuration over hardcoding | Use approved versioned configuration with ownership, validation, rollout, and reversal. | Configuration becomes an unreviewed policy engine, secret store, or tenant-authority substitute. |

# Feature Design Checklist

Before implementation, define:

1. user/business outcome, explicit non-goals, acceptance criteria, and the smallest safe vertical slice;
2. primary owner, supporting owners, authoritative documents, and whether a capability already exists;
3. trusted identity, tenant, membership, entitlement, authorization, consent, and data-classification inputs;
4. canonical records, transient state, data owner, retention/deletion/restore implications, and prohibited data paths;
5. APIs/events/jobs: version, schema, correlation/idempotency, authorization, errors, retries, ordering, compatibility, and reconciliation;
6. user/channel behavior: capability limits, delivery/outcome semantics, unsafe/unknown cases, and safe-defer path;
7. observability, audit, privacy/redaction, operational support, runbook, capacity, rollout, rollback/recovery, and incident impact;
8. test strategy: unit, contract, integration, tenant/security negative, failure/recovery, end-to-end, and evaluation/accessibility evidence as applicable; and
9. required documentation, decision, change approval, migration, and follow-up work.

Unknown ownership, tenant authority, authorization, public contract, canonical state, or irreversible data/external effect is blocking ambiguity—not a reason to guess in code.

# Interface and Event Application Rules

An interface exposes only the capability its owner intends to provide. It identifies caller identity/authorization context, tenant scope, version, correlation/idempotency reference, expected outcome categories, error/retry behavior, timeout/deadline, and observability/audit requirements.

Events are facts published by the owning module, not commands that let consumers rewrite ownership. Consumers remain idempotent, tenant-safe, version-compatible, and prepared for duplicates, delays, ordering changes, and uncertain outcomes. A consumer may request an approved action through the responsible contract; it must not mutate another module's state directly.

# Data, AI, and Channel Application Rules

Knowledge is governed organizational information owned by Knowledge Platform; Memory is governed participant continuity owned by Memory Platform. Neither is copied into agent/channel configuration or used outside approved purpose, tenant, authorization, and lifecycle controls.

Agent Platform owns reasoning and tool-selection intent. Integration owns authorized execution and external-effect handling. Conversation owns canonical session/routing/handoff state. Voice and Digital Channel platforms own transport/delivery mechanics. An implementation that mixes these roles requires redesign or architecture review, even if it appears faster for a first release.

AI behavior changes are versioned, evaluated, reversible, observable, and subject to tool/knowledge/memory/security constraints. Model output, a provider callback, or a visible UI state is not sufficient proof of authorization, factual correctness, participant delivery, or completed business action.

# Change Classification and Review

| Change type | Examples | Minimum path |
|---|---|---|
| Local implementation | Documentation clarification, contained bug fix, internal refactor with no contract/data/security behavior change. | Owner review, focused validation, documentation alignment. |
| Feature | New endpoint, user flow, workflow node, channel capability, background job, or connector behavior. | Written design, owner contracts, proportionate Security/Data/Operations/Testing review, evidence, and documentation. |
| Architecture | New shared service/store/event backbone, changed ownership, new trust model, tenant strategy, or materially changed contract. | Approved proposal, impact/migration/recovery analysis, decision/change record, cross-owner review. |
| Production-critical | Authorization, secret, data deletion/export, billing, call routing/recording, migration, release, or incident/recovery control. | Formal Security/Operations/Data review, failure/rollback plan, integration evidence, staged release criteria. |

When uncertain, use the higher-impact path. An urgent condition follows the documented emergency procedure and does not remove accountability, evidence preservation, least privilege, or retrospective review.

# Architecture Review Questions

Reviewers ask:

- Does exactly one module own each canonical fact, behavior decision, and external effect?
- Does the design preserve trusted tenant/identity/authorization context end to end?
- Is the interface/event contract versioned, observable, idempotent where relevant, and safe under delay, duplicate, failure, and uncertainty?
- Does the design preserve One Brain, Multi-Channel rather than duplicate intelligence by channel?
- Are knowledge, memory, secrets, participant data, and telemetry minimized and handled under the correct owner controls?
- Are deployment, operations, observability, testing, recovery, and customer-impact implications explicit?
- Can an independent contributor understand the owner, rationale, evidence, and next action without chat history?

Any “no” or unresolved material ambiguity is recorded and resolved through the applicable owner or change process before implementation proceeds.

# Initial Implementation Application

For the first vertical slice, apply this guide to one tenant-aware API foundation, one approved agent/version, one canonical conversation path, one Voice and one Digital Channel path, one bounded Integration action, one authorized operator view, and the supporting Security/Data/Operations/Deployment/Observability/Testing evidence.

Do not broaden the initial slice with extra channels, direct provider/database access, autonomous configuration changes, broad administration, unsupported cross-tenant features, or unreviewed infrastructure. Prove the end-to-end architecture boundary first, then expand through the same rules.

# Related Documents

- `01_SYSTEM_OVERVIEW.md`
- `02_ONE_BRAIN_MULTI_CHANNEL.md`
- `03_PLATFORM_LAYER_MODEL.md`
- `04_MULTI_TENANT_ARCHITECTURE.md`
- `05_SYSTEM_DATA_FLOW.md`
- `06_EVENT_DRIVEN_ARCHITECTURE.md`
- `07_HIGH_LEVEL_SERVICE_MAP.md`
- `00_CONTROL/03_ARCHITECTURE_PRINCIPLES.md`
- `00_CONTROL/09_CHANGE_MANAGEMENT.md`
- `00_CONTROL/AI_DRIVEN_ENTERPRISE_SAAS_DEVELOPMENT_PLAYBOOK.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-09 | Created the architecture-principles application guide. |
| 2.1 | 2026-08-09 | Finalized after ownership, implementation-readiness, overlap, and maintainability review. |

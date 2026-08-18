# 05_MEMORY_RETRIEVAL_AND_CONTEXT

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines how an authorized caller requests, receives, and uses Memory evidence as bounded context. Retrieval selects the minimum eligible Memory revisions for a specific participant and purpose; it does not provide a general profile dump, decide an agent's action, or authorize access on its own.

Eligibility is evaluated before relevance. A useful preference that is suppressed, expired, out of scope, prohibited by consent/purpose, or unavailable under authorization is not usable context.

---

# Purpose

The retrieval model protects personal memory from overexposure while giving approved platform capabilities the context needed for continuity. It creates explicit outcomes, provenance, freshness, and restriction behavior that remain safe under policy change, lifecycle events, failures, and provider/index variation.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory retrieval request/result contract, eligibility, selection policy, context assembly, Memory evidence, and outcomes | Memory Platform |
| Agent reasoning, prompt composition, model invocation, response/action decisions, and tool use | 02_AGENT_PLATFORM |
| Canonical interaction context, session, routing, and handoff | 03_CONVERSATION_PLATFORM |
| Memory capture/admission and record/profile semantics | 03_MEMORY_CAPTURE_AND_ADMISSION.md and 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md |
| Correction, suppression, expiry, retention, deletion, and lifecycle decisions | 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md |
| Enterprise authorization, identity, secrets, security policy engines, and audit infrastructure | 09_SECURITY_PLATFORM |
| Tenant/membership/entitlement/configuration facts | 16_PLATFORM_FOUNDATION |
| Retrieval storage/index/cache/queue implementation | 08_DATA_PLATFORM |
| Channel transport and delivery behavior | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |

Memory applies the current enterprise controls and referenced platform facts to its own eligibility policy. It does not replace those systems or expose their internals.

---

# Retrieval Principles

## Purpose-Bound and Subject-Bound

Every request is tied to one server-resolved tenant, one authorized requester context, one approved `MemorySubjectBinding`, one stated purpose, and one requested representation. Broad tenant-wide or anonymous semantic search is not a Memory retrieval mode.

## Eligibility Before Relevance

The service applies tenant, subject, authorization, purpose/consent, audience, classification, lifecycle, freshness, representation, and retention constraints before matching, ranking, or assembling context. A relevance score cannot override a restrictive condition.

## Minimum Necessary Context

The result includes only records, fields, evidence, and provenance appropriate to the requested purpose and representation. It favors a small number of high-value facts over a comprehensive profile or hidden profile score.

## Evidence, Not Instructions

Memory returns a bounded fact, its applicable scope/freshness, and an explanation/reference appropriate for the consumer. It does not return prompt instructions, reasoning recommendations, action permissions, or raw transcripts.

## Currentness Is Explicit

Every supported result indicates observed/effective/freshness state and applicable limitations. An unknown, stale, or representation-lagged record is not silently presented as current.

## Safe Absence

No supported memory is a valid and often preferred result. Result shape, counts, errors, timing, and diagnostic text must not reveal hidden, restricted, deleted, or cross-subject memory.

---

# Retrieval Request Contract

| Field | Requirement |
|---|---|
| `request_id` and `correlation_id` | Stable request and trace identifiers for audit, idempotent handling where applicable, and diagnostics. |
| `tenant_ref` | Resolved and validated server-side; a caller-provided value is never sufficient. |
| `requester_context` | Authorized principal, role/service identity, current authorization inputs, and allowed representation context. |
| `subject_binding_ref` | Validated Memory subject scope; must not be guessed from free text or external address alone. |
| `purpose` | An approved, specific use such as service continuity, participant transparency, or authorized operator review. |
| `requested_representation` | Bounded view such as operational context, participant transparency, or operator review. |
| `interaction_or_case_ref` | Optional constrained reference used only when scope or preference specificity requires it. |
| `context_budget` | Maximum allowed records, fields, bytes/tokens, and sensitivity level; server policy may reduce it. |
| `freshness_requirement` | The caller's permitted freshness need; it cannot relax record or policy limits. |

The contract carries opaque canonical references. It does not accept raw profile data, unrestricted natural-language search terms, provider IDs, or client-asserted consent/authorization as a basis for retrieval.

---

# Eligibility Pipeline

```text
Validated request
    |
    +--> resolve tenant, requester, subject, purpose, representation
    |
    +--> verify authorization, entitlement, and current policy inputs
    |
    +--> select profile/records in the same tenant and subject scope
    |
    +--> filter lifecycle, suppression, deletion, retention, classification,
    |    audience, purpose/consent, effective, expiry, and freshness constraints
    |
    +--> apply deterministic preference specificity/precedence
    |
    +--> select minimum necessary eligible revisions and representations
    |
    +--> verify representation lineage/currentness and apply context budget
    |
    +--> return explicit outcome with permitted evidence
```

The pipeline can use indexed, structured, lexical, or semantic lookup internally only after mandatory scope predicates are established. Every derived lookup result is revalidated against canonical current state before it is returned.

---

# Selection and Context Assembly

## Selection Inputs

Selection uses only approved, explainable inputs:

- record type and semantic schema;
- subject/purpose/channel/relationship/case scope;
- current participant instruction where supplied through an authorized interaction;
- precedence rules from `04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md`;
- freshness, confidence, source authority, and verification state; and
- context budget and requested representation.

Inferred affinity, hidden behavioral scoring, cross-participant similarity, unrestricted semantic similarity, and opaque provider ranking must not select personal memory unless explicitly governed by a later approved policy and model change.

## Context Budgeting

The service applies policy-defined limits on number of records, value detail, evidence detail, sensitivity, and representation size. When eligible content exceeds the budget, it selects the most specific/current verified facts and returns an explicit truncation indicator only when doing so cannot reveal hidden information.

## Representation Levels

| Representation | Permitted content |
|---|---|
| `operational_context` | Minimum facts needed for an authorized interaction, plus scope/freshness and concise provenance indicator. |
| `participant_transparency` | The participant's permitted memory values, explanation/source category, applicable constraints, and correction/suppression actions. |
| `operator_review` | Authorized values, evidence references, admission/lifecycle state, conflicts, constraints, and audit links. |
| `governance_quality` | Aggregated/minimized signals only; no personal-memory values unless separately authorized. |

No representation may expose a raw provider payload, full transcript, unrelated evidence, hidden decision rationale, or an internal credential/reference unnecessary for the consumer.

---

# Result Contract and Outcomes

| Outcome | Meaning | Permitted response behavior |
|---|---|---|
| `supported` | One or more eligible Memory revisions can be returned within budget. | Return minimum permitted facts, currentness, constraints, and provenance appropriate to the representation. |
| `unsupported` | No eligible Memory evidence exists for the request. | Return no values; do not imply whether a hidden/restricted record exists. |
| `restricted` | Authorization, purpose/consent, classification, lifecycle, audience, or policy prevents use. | Return a privacy-safe restriction outcome without hidden-value details. |
| `stale` | An otherwise applicable record fails required freshness/currentness conditions. | Return no unsafe value; include only permitted remediation/refresh indication. |
| `degraded` | A bounded safe result is available while an approved dependency/representation is impaired. | Mark degradation and omit any result whose eligibility/currentness cannot be proven. |
| `unavailable` | Safe retrieval cannot complete. | Return no values and preserve a correlation reference for authorized support. |

The outcome vocabulary is intentionally limited. Callers must handle all outcomes safely and cannot treat `unsupported`, `restricted`, `stale`, `degraded`, or `unavailable` as permission to invent, reuse cached, or ask for broader personal context.

---

# Freshness, Cache, and Representation Rules

- Canonical Memory revision and lifecycle state are authoritative; an index, cache, embedding, or summary is never authoritative.
- Every derived representation is linked to tenant, subject binding, revision, constraints, representation version, and invalidation state.
- Cache keys include tenant, subject binding, purpose, requester/representation scope, policy/constraint version where required, and freshness boundary. Shared generic profile caches are prohibited.
- A lifecycle or consent/policy change invalidates affected representations before they can support a result; if invalidation completion is uncertain, the relevant result is restricted, stale, degraded, or unavailable.
- A fallback can use only independently revalidated canonical/derived data that preserves all eligibility conditions. It cannot broaden scope or return a previously cached record by default.

---

# Access and Privacy Protections

- The service resolves tenant and subject scope server-side and applies mandatory predicates at every data/representation access.
- Purpose and representation are authorization inputs, not display labels. A caller may not upgrade them through a client parameter.
- Support, export, and exceptional access routes use dedicated, audited contracts; ordinary retrieval APIs do not become an operator backdoor.
- Logs, metrics, traces, errors, and quality signals use identifiers and minimized metadata. Raw personal values and evidence are excluded unless a governed secure diagnostic path requires them.
- Retrieval limits, anomaly signals, and abuse controls protect against enumeration, similarity probing, repeated guessing, and cross-tenant discovery.

---

# Failure and Recovery Behavior

| Condition | Required behavior |
|---|---|
| Authorization/policy/consent evaluation unavailable | Fail closed as `unavailable` or `restricted` according to safe policy; do not reuse a stale grant. |
| Lifecycle/invalidation state uncertain | Do not return affected value; return `stale`, `degraded`, or `unavailable`. |
| Index/cache/provider unavailable | Revalidate an approved fallback or return `degraded`/`unavailable`; never expose unverified cached context. |
| Duplicate/replayed request | Preserve audit correlation and idempotent response semantics without changing Memory state. |
| Partial result assembly | Return only independently eligible facts with `degraded`, or no values if safe bounds cannot be proved. |
| Cross-tenant/subject mismatch | Return a privacy-safe non-disclosing failure and record a security signal. |

Retrieval never changes a MemoryRecord. Query quality or absence may create a governed quality/gap signal, but it cannot auto-capture, auto-correct, or auto-admit memory.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_MEMORY_DOMAIN_MODEL.md | Defines retrieval request/result and representation entities. |
| 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md | Defines preference scope and deterministic precedence. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines state changes and invalidation obligations. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines detailed authorization and isolation requirements. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines purpose/consent policy and review requirements. |
| 09_MEMORY_QUALITY_AND_EVALUATION.md | Defines quality measures and improvement proposals. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines threat, privacy, and secure-operation requirements. |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | Defines broader recovery and operational resilience. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory retrieval and context model with eligibility-first selection, bounded results, privacy protections, and safe failure behavior. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

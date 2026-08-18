# 07_MEMORY_ACCESS_AND_TENANT_ISOLATION

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines how Memory Platform enforces tenant, subject, requester, purpose, representation, and lifecycle boundaries. Personal Memory is more restrictive than a tenant-scoped document collection: an authorized tenant user does not automatically have access to every participant's durable context.

The model applies Security and Platform Foundation controls to Memory-domain decisions. It does not replace enterprise identity or authorization systems.

---

# Purpose

The access model prevents cross-tenant exposure, cross-subject profiling, purpose drift, unauthorized operational access, and stale derived-data use. It makes every Memory access attributable and safe across APIs, workers, indexes, caches, exports, support tooling, analytics, and external providers.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory access requirements, subject binding rules, representation policy, retrieval enforcement, and Memory-domain access evidence | Memory Platform |
| Authentication, authorization engines, RBAC/ABAC policy infrastructure, secrets, cryptography, audit infrastructure, and compliance controls | 09_SECURITY_PLATFORM |
| Tenant, organization, membership, entitlement, service identity, configuration, and API-edge claims | 16_PLATFORM_FOUNDATION |
| Canonical participant, interaction, session, routing, and handoff authority | 03_CONVERSATION_PLATFORM |
| Channel participant address, delivery consent, and channel transport access | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |
| Storage IAM, physical partitioning, backup, cache/index infrastructure, and data operations | 08_DATA_PLATFORM |
| User/operator interface rendering and user-experience flow | 10_FRONTEND_PLATFORM |

Memory owns the decision inputs and result semantics for its records. Security owns the mechanisms that authenticate and authorize; Foundation owns the control-plane facts those mechanisms rely on.

---

# Access Principles

## Server-Resolved Scope

Tenant, requester, subject, purpose, and representation are resolved or verified by trusted server-side components. A client-supplied tenant ID, subject ID, role, consent flag, or purpose string is an untrusted request attribute until validated against the relevant owner.

## Explicit Subject Relationship

Tenant membership alone is insufficient. Each Memory operation requires an approved relationship between the requester/service and the `MemorySubjectBinding` for the requested purpose, such as the participant themselves, an authorized current interaction, a permitted operational role, or a governed support/privacy workflow.

## Deny by Default

The absence of an applicable grant, binding, policy, consent/use basis, eligible representation, or current lifecycle state produces a privacy-safe denial. The system never falls back to a broader tenant profile or a guessed subject match.

## Eligibility and Authorization Are Both Required

Authorization determines whether a requester may attempt a Memory operation. Memory eligibility determines whether a particular record/revision/representation may be used for that request. A successful authorization check cannot expose suppressed, expired, deleted, out-of-purpose, or restricted memory.

## Least Data and Least Representation

Access is granted to the smallest representation and fields needed for the purpose. Operational context, participant transparency, operator review, governance, export, and support use distinct contracts; a privileged view is never an accidental parameter of an ordinary retrieval request.

## Every Representation Is Isolated

Tenant and subject scope are mandatory for canonical records, indexes, embeddings, caches, queues, worker messages, exports, analytics, logs, traces, and provider calls. A data store feature, similarity search, cache locality, or service-account role does not relax the Memory contract.

---

# Access Context

Every Memory operation uses a validated access context:

| Element | Requirement |
|---|---|
| `tenant_ref` | Resolved from trusted control-plane/security context; mandatory and immutable through the operation. |
| `requester` | Authenticated user, service, agent execution identity, or support/privacy role with auditable credentials. |
| `subject_binding_ref` | Exact approved subject scope; no free-text or cross-subject discovery fallback. |
| `purpose` | A specific approved use, such as service continuity, participant transparency, authorized operator review, deletion fulfilment, or governed quality review. |
| `operation` | Read context, admit candidate, correct, suppress, delete, export, administer policy, or operate/reconcile a dependency. |
| `representation` | Operational context, participant transparency, operator review, governance/quality, export, or secure diagnostic form. |
| `relationship_context` | Optional validated interaction/case/service relation required to prove a narrow grant. |
| `constraints` | Current authorization result, entitlement, consent/use, classification, residency, lifecycle, freshness, and data-minimization limits. |
| `correlation_id` | Traceable identifier used for access evidence, alerting, and authorized investigation. |

The context is assembled once at a trusted boundary and propagated immutably. Services and workers revalidate it when crossing an asynchronous, delegated, long-lived, or external boundary.

---

# Authorization and Eligibility Pipeline

```text
Authenticated requester or service
    |
    +--> resolve tenant, membership/service identity, entitlement, operation
    |
    +--> verify subject binding and approved requester-to-subject relationship
    |
    +--> verify requested purpose and representation are allowed
    |
    +--> resolve Memory records only inside mandatory tenant + subject predicates
    |
    +--> apply lifecycle, consent/use, classification, audience, freshness,
    |    retention, and representation constraints
    |
    +--> minimize fields and evidence; record access evidence
    |
    +--> execute operation or return privacy-safe result
```

Every filter is mandatory. Retrieval relevance, cached authorization, operator convenience, or internal service trust cannot skip a predicate. A decision at a prior stage must be refreshed when its validity window, policy version, lifecycle state, or delegation boundary changes.

---

# Operation Matrix

| Operation | Minimum grant and Memory conditions | Result scope |
|---|---|---|
| Operational retrieval | Authorized service/requester relationship, approved live purpose, eligible revision, permitted representation. | Minimum context facts only. |
| Participant transparency | Verified participant/self-service relationship and applicable rights/identity verification. | The participant's permitted values, explanations, and available actions. |
| Operator review | Named operational/privacy/compliance role, reason, approved relationship, and stronger audit. | Only records/evidence allowed by role and case scope. |
| Candidate admission | Authorized origin and separation-of-duties/review conditions plus all admission gates. | Candidate/decision and resulting record only. |
| Correction/suppression/deletion | Participant or authorized delegate/role, verified scope, policy/hold review, and accountable decision. | Affected record/profile scope and lifecycle result. |
| Export | Dedicated right/administrative workflow, verified subject/tenant scope, minimization, and secure delivery. | Explicitly approved export package only. |
| Reconciliation/operations | Scoped service identity, time-bound operational grant, and no ordinary content access unless separately approved. | Identifiers, target state, and minimal permitted diagnostics. |
| Quality/governance analysis | Authorized policy/quality role, approved dataset/purpose, minimization, and access-controlled environment. | Aggregated or de-identified signals by default. |

No operation obtains a universal profile read. Elevated access is an explicit, short-lived, auditable workflow, not a broader query flag.

---

# Representation and Field Controls

| Representation | Default exposure | Additional protection |
|---|---|---|
| `operational_context` | Minimal active, eligible facts needed for the current approved interaction. | No raw evidence, hidden constraints, or operator notes. |
| `participant_transparency` | Participant-permitted values, source category/explanation, and correction/suppression options. | Strong identity verification and no internal security rationale. |
| `operator_review` | Scoped values, allowed evidence references, decision/lifecycle state, and audit links. | Reason capture, role/case relationship, time-bound access, enhanced audit. |
| `governance_quality` | Aggregated/minimized indicators by default. | Re-identification and individual-value access require separately approved path. |
| `export` | Explicitly approved records and required metadata for the verified requester. | Secure delivery, retention/expiry, download audit, and no hidden implementation data. |
| `secure_diagnostic` | Minimum content necessary for an approved incident/support investigation. | Break-glass approval, redaction, isolated environment, and post-access review. |

Field-level constraints apply after representation selection. A requester permitted to see a preference may not see its sensitive evidence, confidence rationale, external locator, or another representation's fields without an explicit grant.

---

# Isolation by Technical Boundary

| Boundary | Required enforcement |
|---|---|
| API and event contract | Carry trusted scope/correlation references; reject missing/mismatched tenant, subject, purpose, or delegation claims. |
| Canonical data query | Enforce tenant and subject predicates in the server-side data-access layer; never rely solely on caller filtering. |
| Search/index/embedding | Partition or filter by tenant and subject before candidate matching; revalidate canonical eligibility before use. |
| Cache | Scope keys by tenant, subject, requester/representation/purpose/constraint version as needed; expire and invalidate on lifecycle/access change. |
| Queue/worker | Use scoped job envelopes and least-privilege service identity; revalidate delayed or replayed work. |
| Provider egress | Minimize/transform content, enforce allowed class/residency/tenant conditions, and restrict provider credential/data scope. |
| Export/support tool | Dedicated workflow, secure storage/delivery, short retention, immutable access evidence, and no generic browse capability. |
| Telemetry | Use minimized identifiers and redaction; protect correlation/audit lookup separately from ordinary operational access. |

---

# Exceptional Access and Break-Glass

Exceptional access is allowed only for a documented operational, security, privacy, legal, or participant-support purpose. It requires a named accountable actor, scoped subject/tenant, reason, approval where policy requires, short expiry, stronger logging, and post-access review.

Break-glass access cannot override a deletion/suppression state for ordinary use, alter a record, broaden a provider's data rights, or create a durable Memory candidate by itself. The exceptional workflow returns only the narrowest permitted representation and triggers alerts for unusual volume, scope, or timing.

---

# Access Evidence and Detection

For every material operation, Memory emits privacy-safe evidence containing the operation, requester/service, tenant, subject scope reference, purpose, representation, decision/outcome, policy/constraint version, time, correlation ID, and exceptional-access marker where applicable.

The evidence supports review of denied attempts, scope mismatch, enumeration patterns, cross-tenant probes, repeated restricted requests, expired delegation, support access, exports, lifecycle-sensitive access, and provider egress. It excludes raw memory values unless a separately governed secure audit path requires minimal content.

---

# Failure and Revocation Behavior

- Missing, invalid, expired, or unverifiable access context fails closed with a privacy-safe result.
- A change to authorization, membership, entitlement, purpose, consent/use, subject binding, lifecycle, or representation constraint invalidates affected grants and caches promptly.
- Long-running, asynchronous, delegated, or external work rechecks authorization/eligibility at the required boundary and stops when a revocation takes effect.
- Partial authorization or index/cache failure returns only independently proven eligible data with `degraded`, or no content with `restricted`/`unavailable`.
- A tenant/subject mismatch, forged context, or policy-bypass attempt is denied, safely logged, and treated as a security signal.

---

# Integrity Invariants

- No Memory operation can run without a server-resolved tenant, subject scope, requester, purpose, operation, and representation context.
- Tenant and subject predicates are mandatory before matching, retrieval, caching, processing, or provider egress.
- Authorization success never overrides Memory lifecycle, consent/use, classification, retention, or representation restrictions.
- An ordinary retrieval endpoint cannot become an export, support, governance, or diagnostic endpoint through parameters alone.
- An actor cannot infer hidden Memory from identifiers, result counts, errors, timing, cache behavior, or alternate representations.
- Access evidence is attributable and privacy-minimized; logging access does not create an unrestricted copy of personal memory.

---

# Related Documents

| Document | Relationship |
|---|---|
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines eligibility-first retrieval and result behavior. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines lifecycle state, invalidation, and deletion requirements. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, consent, review, and participant rights. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines threat model and security/privacy controls. |
| 11_MEMORY_OBSERVABILITY.md | Defines access and security signal requirements. |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | Defines safe recovery and operational behavior. |
| 16_PLATFORM_FOUNDATION/README.md | Defines tenant, entitlement, and API-edge ownership. |
| 09_SECURITY_PLATFORM/README.md | Defines enterprise security control ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory access and tenant-isolation model with subject-bound access, representation controls, technical enforcement, and revocation behavior. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

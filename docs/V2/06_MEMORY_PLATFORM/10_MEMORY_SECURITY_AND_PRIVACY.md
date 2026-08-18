# 10_MEMORY_SECURITY_AND_PRIVACY

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines the Memory-domain security and privacy requirements for durable participant/customer context. Memory is sensitive because individually low-risk preferences, relationship facts, and continuity signals can become harmful when combined, retained too long, exposed to the wrong subject, or reused beyond their original purpose.

Memory Platform defines the domain threats, classifications, controls, and evidence requirements. Security Platform owns shared identity, authorization mechanisms, cryptography, secrets, audit infrastructure, compliance capabilities, and incident-response governance.

---

# Purpose

The security and privacy model protects Memory from unauthorized capture, inference, disclosure, purpose drift, tenant/subject crossover, provider leakage, manipulation, retention failure, and deletion failure. It ensures that safety constraints are applied before useful-but-risky context reaches an agent, channel, operator, provider, or analytics workflow.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory data classification, domain threat model, Memory-specific control requirements, secure capture/retrieval/lifecycle behavior, and privacy evidence | Memory Platform |
| Authentication, authorization engines, secrets, encryption/key management, enterprise audit infrastructure, security monitoring, incident governance, and compliance controls | 09_SECURITY_PLATFORM |
| Tenant/membership/entitlement/configuration/API-edge claims | 16_PLATFORM_FOUNDATION |
| Channel delivery consent, provider message transport, and telephony/media protections | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |
| Canonical conversations/interactions and their security controls | 03_CONVERSATION_PLATFORM |
| Physical storage, backup, network/data-service operation, and provider infrastructure | 08_DATA_PLATFORM and approved providers |
| Source connectors/external workflows and callback implementation | 07_INTEGRATION_PLATFORM |

Memory applies shared controls to its domain and specifies the contract requirements other owners must preserve when they handle Memory data. It does not become the enterprise security platform.

---

# Security and Privacy Principles

## Treat Personal Context as Sensitive by Default

Memory is classified before storage, retrieval, egress, telemetry, evaluation, or export. Unknown classification follows the safest permitted path and cannot become broadly retrievable by default.

## Minimize at Every Boundary

Capture the smallest allowed value, store the least sensitive representation, return only required fields, redact diagnostics, restrict provider egress, and delete/expire derived copies. Convenience summaries, broad profile views, and "send everything for context" patterns are prohibited.

## Verify Scope Before Content

Tenant, subject, requester relationship, purpose, operation, representation, lifecycle, consent/use basis, classification, and current authorization are evaluated before any content lookup or similarity operation. A service identity, index, or cache does not provide blanket access.

## Preserve Provenance and Integrity

Candidates, evidence, admission decisions, revisions, policy/use-basis references, lifecycle decisions, and invalidation/deletion outcomes are attributable and tamper-evident through approved Security/Data mechanisms. An external callback or model output cannot rewrite Memory truth.

## Separate Operational Use from Audit/Investigation Retention

Security, legal, dispute, or audit retention may preserve minimized restricted evidence for a defined purpose. It never restores ordinary retrieval, agent context, channel delivery, or profile visibility.

## Design for Revocation

Withdrawal, suppression, policy narrowing, expiry, deletion, compromised credential, or authorization change must promptly stop new Memory use and invalidate derived representations. Recovery, replay, and restore paths reapply current restrictions before exposing data.

---

# Data Classification and Handling

| Class | Examples | Default handling |
|---|---|---|
| Restricted personal memory | Sensitive accommodation, protected relationship fact, high-risk preference, disputed value, or security-sensitive context. | Explicit policy/use basis, strict representation/access, enhanced audit, limited egress, short retention, and required review. |
| Confidential personal memory | Approved operational preference or continuity fact tied to a participant. | Tenant/subject/purpose enforcement, minimization, controlled retrieval, standard audit, and defined retention. |
| Internal metadata | Policy/version IDs, minimized lifecycle/audit markers, aggregate quality signal. | No raw value by default; role-restricted operational/governance use. |
| Public or non-personal | Not ordinarily a Memory record. | Keep outside Memory unless a documented category/purpose requires a binding. |

Classification is evaluated at candidate, revision, representation, request/result, export, telemetry, evaluation, and provider boundaries. A lower-risk derived form must be proven to retain its intended classification; truncation or embedding alone does not declassify personal data.

---

# Threat Model

| Threat | Example | Required Memory control |
|---|---|---|
| Unauthorized capture | Agent/model extracts a personal claim from a transcript and stores it automatically. | Candidate-only intake, policy/use-basis/evidence gate, risk review, and no auto-admission beyond approved low-risk rules. |
| Purpose drift | A support preference is reused for marketing, scoring, or unrelated automation. | Purpose-bound records/retrieval, restrictive constraints, policy review, and denied cross-purpose use. |
| Cross-tenant or cross-subject disclosure | Cache/index query exposes another customer's context. | Server-resolved scope, mandatory predicates, isolated keys/jobs, canonical revalidation, and adversarial tests. |
| Identity/relationship spoofing | Caller claims a participant or delegate relationship. | Security/Foundational verification, explicit subject binding, relationship validation, and privacy-safe denial. |
| Inference/profiling expansion | Similarity/model logic creates sensitive behavioral or demographic assumptions. | Narrow categories, minimization, prohibited inference, governed high-risk review, and quality/harm controls. |
| Evidence or callback tampering | Forged CRM/webhook result alters a memory record. | Connector validation, source integrity, immutable evidence/decision lineage, idempotency, and reconciliation. |
| Prompt/content injection | Memory content instructs an agent or changes policy. | Treat values as data, structured representation, agent-side isolation, no instruction fields, and source/candidate controls. |
| Provider egress/leakage | Unapproved content is sent to embedding/model/OCR/provider service. | Classification/egress policy, adapter allowlist, minimization, scoped credentials, residency/retention terms, and audit. |
| Representation residue | Suppressed/deleted data survives in embeddings, summaries, caches, exports, or backups. | Lifecycle-driven invalidation/deletion targets, acknowledgements, reconciliation, and restoration revalidation. |
| Enumeration and side channel | Repeated requests infer profile existence/value from timing/counts/errors. | Safe outcome vocabulary, rate/abuse controls, uniform privacy-safe responses, and detection. |
| Privileged misuse | Support/operator uses broad profile access without need. | Dedicated reason-bound workflow, least representation, short grants, enhanced audit, and post-review. |
| Secret/credential compromise | Provider credential enables broad Memory access or egress. | Security-managed secrets, scoped service identity, rotation, egress controls, and rapid revocation/invalidation. |

---

# Control Requirements by Lifecycle

| Lifecycle point | Required controls |
|---|---|
| Capture | Validate tenant/subject/origin, minimize values/evidence, classify, block prohibited types, verify policy/use basis, protect ingress, and record privacy-safe evidence. |
| Admission | Enforce separation of duties/risk review, immutable decisions, duplicate/conflict handling, approved provider use, and no publication of a candidate as truth. |
| Storage and representation | Use approved Data/Security controls, tenant/subject isolation, encryption/protection as classified, least privilege, lineage, and rebuild/invalidation capability. |
| Retrieval | Server-resolved scope, current authorization, purpose/use basis, lifecycle/freshness/classification/representation filters, minimization, and safe outcomes. |
| Agent/channel consumption | Pass evidence as data through bounded contracts; no raw profile dump, prompt instruction field, or delivery permission inference. |
| Export/support/governance | Dedicated workflow, verified authority, narrow scope, secure delivery/environment, enhanced audit, retention/expiry, and post-access review. |
| Lifecycle/deletion | Immediate non-use on restriction, tracked invalidation/deletion targets, exception/hold controls, provider/backup evidence, and reconciliation. |
| Evaluation/telemetry | Synthetic/minimized data by default, restricted access, redaction, data-specific retention, and no shadow copy of operational memory. |

---

# Provider and External-System Controls

Before Memory data leaves the platform boundary, the owner must establish:

- permitted data class, record type, purpose, subject/tenant scope, and minimum representation;
- provider location/residency, contractual/privacy terms, retention/training restrictions, and deletion mechanism;
- transport, identity, credential, access, logging, incident, and subprocessor controls through approved Security/Data processes;
- adapter contract that records provider/model/parser/version/capability without exposing provider control planes in public Memory contracts;
- timeout, retry, fallback, error/redaction, and outage behavior that fails safely; and
- an exit path that preserves canonical Memory records, lifecycle state, and deletion evidence independently of the provider.

No provider receives a universal profile, unrestricted transcript, hidden evaluator rationale, secret, or broader subject dataset for convenience. A provider capability is disabled for a data class when the required conditions cannot be proven.

---

# Privacy Rights and Sensitive Operations

Participant transparency, correction, suppression, withdrawal, deletion, export, and delegate requests use the governed workflow defined in `08_MEMORY_GOVERNANCE_AND_CONSENT.md`. Security supplies required identity/delegate verification and compliance controls; Memory applies the result to scoped records and representations.

Sensitive operations require a purpose-specific representation, enhanced evidence, and stronger review where policy requires. They include restricted-class retrieval, delegate access, export, broad correction/deletion scope, support/break-glass access, high-risk category admission, provider egress, and policy exception. An approval for one sensitive operation never grants another.

---

# Incident and Revocation Behavior

On suspected or confirmed Memory security/privacy incident:

1. Security leads incident governance; Memory identifies affected tenants, subject bindings, records, revisions, representations, and provider/consumer targets using minimized evidence.
2. Apply the approved containment action: hold, suppression, access revocation, credential rotation, egress stop, provider disablement, or deletion assessment.
3. Block operational use of affected memory until scope and remediation are verified.
4. Preserve only authorized incident/audit evidence, protect it from ordinary retrieval, and follow applicable notification/compliance processes.
5. Reconcile all derived representations, caches, exports, queues, and providers before closure; validate recovery with adversarial and rights scenarios.

An incident workflow does not silently restore use because a dependency recovered or a cached grant remains available.

---

# Security and Privacy Evidence

Required evidence includes current classification, policy/use-basis references, access and exceptional-access outcome, origin/evidence integrity, representation lineage, provider egress decision, encryption/secret/control attestation references where appropriate, lifecycle/invalidation/deletion targets, incident/hold state, and privacy-safe audit correlation.

Evidence is minimized, access-controlled, retained under a defined purpose, and separated from ordinary profile/retrieval content. Audit completeness cannot be achieved by copying every personal value into logs.

---

# Integrity Invariants

- Personal Memory is classified, tenant-scoped, subject-bound, purpose-limited, and lifecycle-aware before capture, use, egress, or telemetry.
- No agent, provider, connector, cache, or channel may bypass candidate admission, access eligibility, suppression, retention, or deletion requirements.
- An authorization success, active record, or channel opt-in never overrides a stricter policy/use basis, lifecycle, classification, or participant restriction.
- Derived data and provider copies are traceable to canonical revisions and are ineligible when their source is restricted or deleted.
- Security/audit/hold retention never becomes an operational Memory access path.
- Incident, recovery, and restore operations reapply the newest access, policy, lifecycle, and deletion requirements before content is usable.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines secure candidate/admission behavior. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines eligibility, minimization, and safe result behavior. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines invalidation, deletion, holds, and recovery. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines access scope and technical isolation. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, rights, review, and exceptions. |
| 09_MEMORY_QUALITY_AND_EVALUATION.md | Defines security/privacy-relevant evaluation evidence. |
| 11_MEMORY_OBSERVABILITY.md | Defines privacy-safe operational signals. |
| 09_SECURITY_PLATFORM/README.md | Defines shared Security Platform ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Memory security and privacy requirements with classification, threat model, lifecycle controls, provider controls, and incident behavior. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

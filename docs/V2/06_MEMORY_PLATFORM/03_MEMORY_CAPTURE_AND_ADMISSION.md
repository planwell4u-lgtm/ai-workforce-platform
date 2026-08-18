# 03_MEMORY_CAPTURE_AND_ADMISSION

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines the controlled path from an observed fact or proposed preference to an admitted Memory revision. It prevents conversation text, agent output, connector data, model inference, or channel metadata from becoming durable personal memory merely because it is available.

Capture creates a `MemoryCandidate`. Admission is the separate, accountable decision that may create or revise a `MemoryRecord` as defined in `02_MEMORY_DOMAIN_MODEL.md`.

---

# Purpose

The capture-and-admission model makes personal-memory creation evidence-bound, minimal, consent-aware, and reversible. It enables useful continuity while preventing silent profile expansion, unsupported inference, duplicated records, and use of stale or withdrawn information.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Candidate schema, evidence requirements, admission state, conflict semantics, and Memory revision creation | Memory Platform |
| Agent proposal generation and reasoning | 02_AGENT_PLATFORM |
| Canonical interactions and participant/session references | 03_CONVERSATION_PLATFORM |
| Voice and digital transport facts, delivery signals, and channel opt-ins | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |
| External-system/CRM connector implementation and callback validation mechanics | 07_INTEGRATION_PLATFORM |
| Tenant, membership, entitlement, and configuration facts | 16_PLATFORM_FOUNDATION |
| Authentication, authorization, secrets, policy engines, audit infrastructure, and compliance controls | 09_SECURITY_PLATFORM |
| Physical persistence, queues, cache, backup, and data operations | 08_DATA_PLATFORM |

Memory records the evidence and policy/consent references needed for its decision. It does not take ownership of the source platform's records or of the enterprise controls used to validate them.

---

# Admission Principles

## Propose, Do Not Auto-Remember

Every input begins as a non-retrievable `MemoryCandidate`. Agent extraction, model classification, speech transcription, a customer statement, a CRM change, or a user-interface submission is a proposal source, not durable memory authority.

## Evidence Is Specific

A candidate identifies the source reference/locator, observation time, capture method, proposed record type/value, tenant and subject binding, purpose, classification, and integrity/verification context. A raw transcript, opaque model score, or external record ID alone is insufficient evidence.

## Minimum Necessary Capture

The candidate must be limited to the smallest statement needed for its stated purpose. Capture does not retain broad interaction content, unbounded model reasoning, or unrelated external profile fields as a convenience.

## Consent, Purpose, and Policy Precede Use

The evaluator determines whether durable capture and later use are permitted under current Memory policy, consent/use basis, classification, subject scope, record type, and tenant configuration. Channel delivery opt-in is evidence only; it is not automatically consent to durable memory.

## Human Review Is Risk-Based

Low-risk, high-confidence, policy-permitted candidates may use controlled automatic admission. Sensitive, disputed, inferred, externally changed, low-confidence, or policy-changing candidates require the configured human or accountable-system review. No candidate bypasses the same evidence and policy gates.

## Admission Is Idempotent

Repeated proposals, retries, duplicate callbacks, or replayed events must resolve to one recorded decision or a safely linked duplicate. Admission cannot create multiple durable records for the same candidate because delivery was repeated.

---

# Candidate Model

| Required field | Meaning |
|---|---|
| `candidate_id` | Stable Memory identifier for the proposal and idempotency boundary. |
| `tenant_ref` and `subject_binding_ref` | Server-resolved scope; caller-provided scope is validated, never trusted alone. |
| `proposed_type` and `proposed_value` | The minimal normalized claim requested for memory; schema version is recorded. |
| `capture_purpose` | The specific approved reason to consider durable capture. |
| `evidence_refs` | One or more immutable source/locator references with observed time and capture method. |
| `origin` | Approved source class such as participant assertion, authorized operator input, validated interaction fact, or approved external-system fact. |
| `classification` and sensitivity | Proposed data handling level and any uncertainty. |
| `policy_and_consent_refs` | The inputs or references evaluated; not a caller assertion that consent exists. |
| `confidence` and verification state | How the claim was derived, verified, disputed, or uncertain. |
| `correlation_id` and idempotency key | Traceability across request, event, review, and retry paths. |

The candidate contains no agent chain-of-thought, raw provider credential, unrestricted transcript copy, or implementation-specific identity as a substitute for an approved reference.

---

# Allowed Origins and Default Disposition

| Origin | Default disposition | Additional requirement |
|---|---|---|
| Participant assertion through an authorized interaction or interface | Candidate; review/verification according to type and policy. | Preserve interaction/UI evidence and capture notice where required. |
| Authorized operator correction or entry | Candidate; may follow a privileged review route. | Record accountable actor, reason, and applicable authority. |
| Validated conversation fact | Candidate only. | Conversation reference, participant association, and context integrity must be verified. |
| Approved external-system fact | Candidate only. | Connector validation, source authority, freshness, and field-level permission must be proven. |
| Agent or model extraction/inference | Candidate only; never sufficient on its own for sensitive or consequential memory. | Record model/method/version and apply the stricter confidence/review policy. |
| Voice/digital channel metadata or opt-in signal | Candidate only where policy allows. | Separate channel-delivery consent from Memory capture/use authorization. |
| Unverified, anonymous, cross-tenant, malformed, or unauthorized input | Rejected. | Record a privacy-safe rejection outcome; do not retain prohibited content. |

---

# Admission Workflow

```text
Receive candidate
    |
    +--> validate tenant, subject binding, origin, schema, and idempotency
    |
    +--> classify and minimize proposed value/evidence
    |
    +--> evaluate current policy, consent/use basis, purpose, and authorization
    |
    +--> match duplicates and potential conflicts
    |
    +--> apply risk tier and required review
    |
    +--> reject / hold / merge / admit
                         |
                         +--> create immutable AdmissionDecision
                         +--> create or revise MemoryRecord
                         +--> create required representations asynchronously
```

All terminal and non-terminal outcomes are auditable. Representation creation occurs only after admission and never turns a candidate into an admitted record.

---

# Validation and Policy Gates

| Gate | Required result on failure |
|---|---|
| Tenant and subject binding | Reject or hold; do not search other tenants or guess a subject. |
| Origin integrity | Reject or hold; preserve only permitted diagnostic evidence. |
| Schema, type, and value minimization | Reject or return for correction; do not retain excess fields. |
| Classification and sensitive-data rule | Hold or reject pending required policy/review path. |
| Capture purpose and consent/use basis | Restrict, hold, or reject; channel opt-in does not satisfy this gate by itself. |
| Requester authorization and separation of duties | Reject or route to an accountable reviewer. |
| Evidence sufficiency and freshness | Hold, reject, or require verification. |
| Duplicate/conflict evaluation | Merge, supersede candidate, hold, or create a controlled revision proposal. |
| Retention/residency/provider constraints | Reject or use an approved local/limited path; never send prohibited content externally. |

The order may be optimized internally, but no relevance, confidence, or convenience score can override a failed safety, scope, or rights gate.

---

# Conflict, Duplicate, and Correction Handling

## Duplicate

Equivalent candidates for the same tenant, subject, type, normalized value, and compatible purpose are linked to the existing candidate, decision, or current record. New evidence may strengthen a controlled revision but does not create a duplicate profile fact.

## Conflict

Conflicting values, freshness, source authority, consent basis, or classification produce a `held` candidate or a review route. The evaluator must not silently choose a more useful value. The conflict outcome records why a value was selected, superseded, or excluded.

## Correction and Dispute

A participant or authorized operator may submit a correction/dispute request. It creates a candidate and LifecycleDecision path with the original record/evidence reference. Until resolved, policy may suppress the disputed record or restrict its representation. Correction is not an in-place edit.

---

# Risk Tiers and Review

| Risk tier | Examples | Minimum admission evidence |
|---|---|---|
| Low | Explicit, low-sensitivity preference with current evidence and permitted purpose. | Automated validation, policy/consent check, duplicate check, auditable decision. |
| Moderate | Externally sourced fact, relationship context, or confidence uncertainty. | All low-tier checks plus verification/freshness evidence and configured review. |
| High | Sensitive, inferred, disputed, consequential, or broadly reusable personal context. | Explicit policy allowance, strong evidence, accountable human approval where required, enhanced audit, and restrictive retrieval policy. |
| Prohibited | Disallowed category, unauthorized subject, prohibited source, or unapproved purpose. | Reject without durable memory creation; retain only minimal permitted security/audit evidence. |

Risk tiers and thresholds are configuration/policy inputs; they do not grant authorization on their own.

---

# Admission Outcomes

| Outcome | Meaning | Retrievable? |
|---|---|---|
| `admitted` | Candidate passed required gates and created/revised a controlled MemoryRecord. | Only after representation, lifecycle, and retrieval eligibility checks. |
| `merged` | Candidate was safely linked to an existing candidate/record and did not create duplicate truth. | Only the linked record may be eligible. |
| `held` | More evidence, review, policy decision, or conflict resolution is required. | No. |
| `rejected` | Candidate is invalid, unauthorized, prohibited, unsupported, or insufficient. | No. |
| `withdrawn` | Proposal was withdrawn before admission. | No. |
| `superseded` | A later candidate/decision replaces the proposal path. | No, unless an admitted linked record remains independently eligible. |

An `AdmissionDecision` records the result, evaluator, time, policy/consent references, reasoning summary appropriate for audit, and the resulting Memory revision or linked record where applicable. It must not retain hidden model reasoning or prohibited source content.

---

# Failure and Recovery Requirements

- A timeout, provider outage, queue retry, duplicate callback, or worker restart leaves a candidate non-retrievable until an admission decision is durably recorded.
- A decision write and Memory revision creation are atomic from the logical contract perspective; recovery reconciles partial technical effects without exposing a partially admitted record.
- If policy, consent, subject binding, or authorization cannot be evaluated, the outcome is hold or safe failure—not admission.
- Delayed external evidence is revalidated for current tenant, purpose, classification, consent/use, and freshness before a retry may proceed.
- Dead-letter, reconciliation, and manual repair paths preserve idempotency, access control, and complete audit evidence.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_MEMORY_PLATFORM_ARCHITECTURE.md | Defines the Memory ownership and candidate-to-admission principle. |
| 02_MEMORY_DOMAIN_MODEL.md | Defines `MemoryCandidate`, `MemoryEvidence`, `AdmissionDecision`, and related entities. |
| 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md | Defines profile/preference semantics after admission. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines correction, suppression, expiry, retention, and deletion outcomes. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines requester, subject, tenant, and representation enforcement. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, consent, review, and audit authority. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines sensitive-data and privacy-control requirements. |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | Defines broader recovery and safe-degradation behavior. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory capture and admission model with candidate controls, policy gates, risk tiers, outcomes, and recovery requirements. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

# 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines how durable Memory changes, becomes ineligible, expires, is corrected, is suppressed, is retained for required evidence, and is deleted. Lifecycle is authoritative: a useful value must stop being usable when its evidence, consent/use basis, purpose, scope, freshness, or retention conditions no longer permit it.

The model governs Memory-domain decisions and requirements. Data Platform operates physical storage/deletion mechanisms, Security Platform supplies enterprise control and compliance capabilities, and other platforms retain their own records and lifecycles.

---

# Purpose

The lifecycle model prevents stale, disputed, withdrawn, or deleted personal context from surviving in profiles, indexes, embeddings, summaries, caches, exports, telemetry, provider copies, or consumer-held context. It preserves enough minimized evidence to explain a decision without preserving the prohibited value itself.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory state, revision/lifecycle decisions, retention requirements, deletion eligibility, invalidation requirements, and Memory audit semantics | Memory Platform |
| Physical deletion, backup recovery, storage retention, queue/cache mechanics, and provider data operations | 08_DATA_PLATFORM with applicable provider owners |
| Enterprise legal/compliance controls, authorization, security incident response, audit infrastructure, and secrets | 09_SECURITY_PLATFORM |
| Participant transparency, correction, suppression, consent, and governance policy requirements | 08_MEMORY_GOVERNANCE_AND_CONSENT.md |
| Canonical interaction, channel consent, external CRM, Agent, and Knowledge record lifecycle | Their respective platform or external system owners |

Memory may issue requirements and attest logical completion, but it cannot claim that another platform's source record, backup, channel, or external system has been erased unless that owner supplies governed completion evidence.

---

# Lifecycle Principles

## Lifecycle State Determines Eligibility

The canonical `MemoryRecord`, its current `MemoryRevision`, current constraints, and applicable `MemoryLifecycleDecision` determine whether a value is eligible. An index hit, cache entry, prompt copy, or old result is never evidence that Memory remains usable.

## Change Is Append-Only

Corrections, disputes, supersession, suppression, expiry, deletion, and restoration create accountable decisions and revisions. History is not overwritten; audit retention is minimized, access-controlled, and separated from ordinary retrieval.

## Suppression Is Immediate for Use

When an authorized suppression, rights withdrawal, safety hold, or deletion request takes effect, ordinary retrieval must stop returning the value immediately according to policy, even while physical deletion and dependent-system acknowledgement are still in progress.

## Retention Is Purpose-Specific

Retention has an explicit purpose, policy source, effective time, minimum/maximum period where applicable, and disposition action. Retaining a record for audit, dispute, legal hold, or security investigation does not make it eligible for operational context.

## Deletion Is a Distributed Outcome

Deletion covers canonical values, derived representations, caches, indexes, queues, exports, provider copies, and permitted backup handling. The system tracks each required target and does not report complete deletion while required acknowledgements or exception handling remain unresolved.

## Restoration Is Exceptional

A suppressed, expired, or pending-deletion record may be restored only through an explicit, authorized policy path. Deleted content is not restored from an ordinary backup; any permitted recovery is a new governed admission/revision process with recorded authority.

---

# Lifecycle States

| State | Meaning | Retrieval eligibility |
|---|---|---|
| `active` | Current revision is potentially usable if all other constraints pass. | Conditional. |
| `held` | Use is paused pending policy, evidence, dispute, security, or review outcome. | No. |
| `superseded` | A newer revision or controlled successor replaces the record for its relevant scope. | No, except governed historical/audit access. |
| `suppressed` | Use is deliberately blocked by participant request, consent withdrawal, safety, policy, or investigation. | No. |
| `expired` | Effective/freshness/retention condition ended the operational value. | No. |
| `pending_deletion` | Deletion is authorized and required processing remains. | No. |
| `deleted` | Required logical deletion and tracked disposition are complete or a governed exception is recorded. | No. |
| `rejected` | Candidate did not become a durable record. | No. |

`active` does not override authorization, purpose, classification, representation, consent/use, or currentness checks. `held`, `suppressed`, `expired`, `pending_deletion`, and `deleted` take precedence over relevance and preference selection.

---

# Lifecycle Triggers and Decisions

| Trigger | Required decision | Typical effect |
|---|---|---|
| Participant correction or dispute | Correct, hold, suppress, reject, or create a new revision. | Original value may become ineligible while resolved. |
| Authorized operator correction | Validate authority and create controlled revision/lifecycle decision. | Previous revision is preserved but superseded or held. |
| Newer or stronger evidence | Review conflict, authority, confidence, and scope. | Supersede only within the relevant scope. |
| Consent/use withdrawal or purpose removal | Suppress or begin deletion as policy requires. | Immediate operational ineligibility and dependent invalidation. |
| Freshness/expiry reached | Expire or require verification. | No use until a new eligible revision exists. |
| Retention expiry | Authorize deletion/disposition. | Pending-deletion then deletion tracking. |
| Security/privacy incident or investigation | Hold, suppress, restrict, or initiate deletion. | Preserve only authorized incident/audit evidence. |
| Tenant/subject binding closure | Review all affected records against policy. | Suppress, retain for a defined purpose, or delete. |
| Source/evidence rights withdrawal | Suppress or delete affected revisions. | Invalidate all dependent representations. |

Every `MemoryLifecycleDecision` records the trigger, authority, effective time, scope, affected revisions/representations, policy or legal basis reference, disposition requirements, and a privacy-safe explanation for the appropriate audience.

---

# Correction and Supersession

1. Create a correction/dispute candidate with a reference to the disputed record and permitted evidence.
2. Validate tenant, subject, authority, purpose, classification, and policy/consent conditions.
3. Hold or suppress the old value when immediate non-use is required.
4. Resolve conflict through a new AdmissionDecision and immutable MemoryRevision; do not edit the old revision in place.
5. Mark the former revision superseded or retain it in a governed historical/audit state.
6. Invalidate every affected representation and notify only permitted consumers.

Supersession is scoped. A new channel-specific preference does not silently erase a still-valid preference for another approved purpose or channel.

---

# Suppression and Rights Withdrawal

Suppression is a reversible operational block when policy permits; deletion is the irreversible logical removal of ordinary Memory content. A suppression request identifies scope: record, record category, representation, purpose, channel, profile, or subject binding. Broadening scope requires explicit authority.

On effective suppression or withdrawal:

- ordinary retrieval immediately returns no supported value from the affected scope;
- profile views, context caches, search indexes, embeddings, summaries, queues, and active work receive invalidation requirements;
- downstream consumers must drop or stop using held context at their next safe boundary, with an expedited path for high-risk data;
- audit retains only the minimum authorized decision evidence; and
- a deletion assessment is started when the policy or request requires removal rather than non-use.

Channel delivery opt-out remains owned by Digital Channel Platform. It may trigger a Memory candidate/constraint change, but Memory does not claim to change the channel's delivery state.

---

# Retention and Deletion Model

## Retention Schedule

Each record category and revision has a policy-governed retention schedule containing:

- approved purpose and policy source;
- effective start, review, expiry, and deletion/disposition time;
- subject/tenant/regional constraints;
- legal hold, dispute, security, or audit exception rules;
- required deletion targets and acknowledgement expectations; and
- the minimum metadata allowed to survive deletion for audit or security purposes.

No open-ended default retention is permitted. A missing or conflicting schedule is a hold/review or safe non-admission condition, not permission to retain indefinitely.

## Deletion Workflow

```text
Authorized deletion trigger
    |
    +--> validate scope, authority, hold/exception, and policy
    |
    +--> set pending_deletion and immediately make content ineligible
    |
    +--> create deletion work for canonical, derived, export, cache, queue,
    |    index, provider, and backup/disposition targets
    |
    +--> collect acknowledgements or governed exception evidence
    |
    +--> verify ordinary retrieval and views cannot return the content
    |
    +--> record deleted outcome, remaining restricted audit metadata, and any exception
```

## Holds and Exceptions

An approved legal, security, dispute, or regulatory hold can defer physical deletion only for the documented purpose and minimum period. It never re-enables operational retrieval. Holds are time-bounded, reviewed, access-restricted, and audited. When a hold ends, deletion resumes from the tracked state.

---

# Derived Data and Consumer Invalidation

| Target | Requirement |
|---|---|
| Search/index/embedding | Remove or mark ineligible before the representation may support another result. |
| Cache/session/context assembly | Evict or block at the next safe boundary; high-risk revocation uses expedited invalidation. |
| Summary/projection/profile view | Rebuild or suppress from current eligible revisions only. |
| Queue/job/dead-letter item | Prevent processing/use, redact/delete where required, and retain only allowed operational metadata. |
| Export/report/analytics dataset | Apply approved deletion/suppression and record completion/exception evidence. |
| External provider copy | Use approved deletion/retention mechanism and retain provider acknowledgement or exception evidence. |
| Backup/archive | Follow Data/Security-approved retention and restoration controls; restored material must not become operationally eligible without revalidation. |

Invalidation completion is observed and reconciled. If a required target's status is unknown, the relevant Memory value remains unusable and operations follow the escalation/runbook path.

---

# Failure and Recovery Requirements

- Lifecycle decisions are durably recorded before any outcome is presented as complete.
- An interruption after suppression/pending-deletion never re-enables ordinary retrieval on retry or recovery.
- Duplicate/out-of-order lifecycle events are idempotently reconciled using decision and revision identifiers.
- A deletion worker failure, provider outage, or backup constraint creates a visible incomplete target/exception; it does not falsely claim deletion complete.
- Restore, migration, and disaster-recovery procedures reapply the newest lifecycle, suppression, consent/use, and invalidation state before material is made available.
- Reconciliation detects orphaned representations, stale caches, unacknowledged provider copies, and deleted records that still appear in a profile view or retrieval test.

---

# Integrity Invariants

- A lifecycle decision is append-only, attributable, scoped, and linked to the affected record/revision/representation set.
- No derived representation may outlive the eligibility of its source revision.
- A current restriction, suppression, pending-deletion state, or deletion state overrides a prior supported result and relevance score.
- Audit/hold retention does not authorize operational Memory retrieval.
- Deletion completion means all required targets are acknowledged or a governed, visible exception exists; it never means unverified best effort.
- An external source or provider cannot restore a deleted/suppressed Memory value by replaying an old callback or record.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_MEMORY_DOMAIN_MODEL.md | Defines lifecycle decisions, revisions, and representations. |
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines correction as a controlled candidate/admission path. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines retrieval ineligibility and revalidation. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines access enforcement through lifecycle state. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, participant rights, consent, and hold authority. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines privacy/security incident and data-protection requirements. |
| 11_MEMORY_OBSERVABILITY.md | Defines lifecycle/deletion signals and evidence. |
| 12_MEMORY_RELIABILITY_AND_FAILURE_HANDLING.md | Defines recovery, reconciliation, and runbook requirements. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory lifecycle, retention, deletion, invalidation, and recovery model. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

# 04_MEMORY_PROFILE_AND_PREFERENCE_MODEL

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines how admitted Memory records are organized into a governed participant-specific `MemoryProfile`, with particular rules for preferences, relationship context, and continuity facts. It defines semantic structure after admission; it does not authorize capture, implement retrieval ranking, or replace identity, CRM, or Conversation records.

The model favors small, explainable facts over a comprehensive behavioral portrait. A profile is a constrained Memory view for one approved subject binding, not an independent customer database.

---

# Purpose

The profile and preference model lets an authorized capability use a current, relevant preference consistently across interactions while preserving origin, scope, confidence, consent/purpose constraints, correction, suppression, expiry, and deletion behavior.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Profile container, memory record types, preference semantics, scopes, precedence, and Memory-specific relationship/continuity facts | Memory Platform |
| Candidate creation, validation, evidence sufficiency, consent/policy gate, and admission decision | 03_MEMORY_CAPTURE_AND_ADMISSION.md |
| Canonical identity, organization/workspace membership, entitlement, and control-plane configuration | 16_PLATFORM_FOUNDATION and 09_SECURITY_PLATFORM |
| Canonical participant, conversation, interaction, session, and transcript | 03_CONVERSATION_PLATFORM |
| External CRM/contact/profile schema and synchronization mechanics | External system via 07_INTEGRATION_PLATFORM |
| Purpose-bound retrieval contract, eligibility filtering, and context budget | 05_MEMORY_RETRIEVAL_AND_CONTEXT.md |
| Correction, suppression, retention, deletion, and record lifecycle transition | 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md |

---

# Profile Model

## MemoryProfile

A `MemoryProfile` is a tenant-scoped container associated with exactly one `MemorySubjectBinding`. It organizes eligible Memory records and exposes no independent claim about the subject's identity, contact address, account ownership, legal status, or external-system profile.

| Property | Rule |
|---|---|
| Scope | One tenant and one subject binding for its entire lifetime. |
| Identity | References canonical subject identity; it does not duplicate or resolve identity. |
| Contents | Contains only admitted Memory records and their eligible revisions. |
| Visibility | Determined per request by current authorization, purpose, constraints, and lifecycle state; there is no universally visible profile. |
| Lifecycle | Profile status can prevent retrieval, but it does not override individual record suppression, expiry, or deletion. |
| Portability | Logical records and their evidence/lifecycle outcomes are exportable under policy; provider representations are derived. |

An empty profile is valid. The absence of a profile or record means no supported Memory evidence exists; it must not be interpreted as a personal trait.

---

# Record Categories

| Category | Definition | Example | Exclusions |
|---|---|---|
| Preference | A stated or verified choice about how a participant wants an approved service interaction handled. | Preferred language for support; accessible communication format. | A guessed preference, broad marketing segment, or unverified demographic inference. |
| Relationship context | A limited fact needed to serve an approved current relationship. | Authorized account relationship reference; named service role where policy permits. | Full CRM replication, account balance, or unrestricted contact directory. |
| Continuity fact | A time-bounded fact needed to continue approved work across interactions. | Confirmed follow-up constraint; open-case communication preference. | Canonical case workflow, task state, or conversation/session history. |
| Accommodation or sensitivity indicator | A tightly controlled fact enabling an approved accessibility, safety, or privacy accommodation. | Do not expose visual-only instructions. | Diagnosis, inferred condition, or broader sensitive profile not explicitly authorized. |

New categories require a documented purpose, evidence standard, sensitivity/classification rule, consent/use basis, retention rule, retrieval audience, misuse analysis, and governance approval before they can be admitted.

---

# Preference Model

## Preference Dimensions

Each preference is represented as a `MemoryRecord` with a typed semantic schema. Initial dimensions are limited to:

| Dimension | Permitted meaning | Typical scope |
|---|---|---|
| Communication language | The language a participant prefers for an approved interaction. | Tenant service or approved channel. |
| Communication format | A preferred accessible or presentation format. | Specific interaction type or channel. |
| Contact timing | A permitted/preferred window for an approved contact purpose. | Purpose and jurisdiction-aware channel. |
| Channel preference | A preferred approved channel, subject to current delivery consent and channel availability. | Specific purpose/channel. |
| Continuity preference | A bounded interaction preference needed for ongoing work. | Specific service relationship or case context. |

A preference never overrides law, safety policy, current channel opt-in/opt-out, authorization, operational availability, participant request in the current interaction, or a more restrictive Memory constraint.

## Preference Scope

A preference has explicit scope fields rather than a hidden global default:

- tenant;
- subject binding;
- approved purpose;
- applicable channel or interaction type where relevant;
- relationship or case reference where relevant;
- effective/expiry/freshness period; and
- audience/representation restrictions.

No preference is treated as universal merely because a value exists. A request outside its scope returns no supported preference evidence.

## Preference Precedence

When multiple eligible preferences could apply, the consumer applies this deterministic order before any relevance choice:

1. current participant instruction in the authorized interaction, if it is valid and permitted;
2. active suppression, opt-out, safety, legal, or policy restriction;
3. a more specific eligible Memory scope (purpose + relationship/case + channel);
4. a less specific eligible Memory scope;
5. a platform or tenant default supplied by the appropriate owner.

At every level, the current authorization, consent/use basis, freshness, classification, and lifecycle constraints still apply. Equal-specificity conflicts are not silently ranked: the result is restricted, unsupported, or a review/correction path according to policy.

---

# Relationship Context Model

Relationship context records only the minimum fact needed to make an approved service interaction coherent. They must use a reference-first design:

| Field class | Rule |
|---|---|
| External relationship reference | Keep a protected reference to the authorized system of record where a live lookup is required. |
| Memory assertion | Store only the approved, time-bounded contextual statement needed for continuity. |
| Authority and freshness | Identify the source authority and when it was observed; do not assume an external fact remains current. |
| Access and representation | Restrict exposure to the audience/purpose that needs the context; avoid displaying implementation references unnecessarily. |
| Lifecycle | Expire, suppress, correct, or delete independently of the external source unless a governed synchronization rule applies. |

Memory must not use relationship context to infer household, employment, health, financial, behavioral, or social-network attributes unless a separately approved category and policy explicitly permits it.

---

# Profile Views and Representation

There is no single raw "profile payload." Memory produces a purpose-bound profile view composed from the minimum eligible records.

| View | Permitted content | Consumer example |
|---|---|---|
| Operational context | Minimal approved preferences or continuity facts plus freshness/provenance indicators. | Agent through an authorized Conversation request. |
| Participant transparency view | The participant's permitted records, sources/explanations, correction/suppression actions, and required notices. | Customer portal. |
| Operator review view | Authorized evidence, decision history, constraints, conflict/correction state, and audit links. | Support or compliance operator. |
| Governance/quality view | Aggregated, minimized, access-controlled signals about record quality or policy outcomes. | Authorized policy reviewer. |

Views are representations, not new records. They must enforce their own audience, redaction, tenant, purpose, and retention controls and cannot bypass an individual record's lifecycle state.

---

# Conflict and Change Semantics

- A profile can contain several records of different categories, but it must not contain two equally applicable active preference revisions that assert incompatible values without an explicit conflict state.
- A current participant instruction affects the current interaction first; whether it becomes durable Memory follows the capture-and-admission process.
- A correction creates a candidate and a new controlled revision/lifecycle decision. It does not mutate previous evidence or erase required audit history.
- An external-system change is a candidate, not a profile overwrite. It is re-evaluated for authority, freshness, purpose, and consent/use requirements.
- A profile-level suspension prevents profile retrieval where required but never restores records that are individually suppressed, expired, or deleted.

---

# Integrity Invariants

- A `MemoryProfile` never substitutes for a canonical identity or external CRM profile.
- Every exposed preference or context fact is traceable to an admitted Memory revision, evidence, and applicable constraints.
- Preference precedence cannot override a current restriction, opt-out, suppression, authorization denial, or legal/safety obligation.
- A channel preference does not grant channel delivery permission; Digital Channel validates current channel consent and delivery conditions.
- A profile view cannot reveal hidden record counts, restricted values, deleted content, or another subject's/tenant's information.
- Derived summaries, embeddings, caches, and UI views become ineligible when the source record is corrected, suppressed, expired, or deleted.

---

# Related Documents

| Document | Relationship |
|---|---|
| 02_MEMORY_DOMAIN_MODEL.md | Defines the canonical entities and revision invariants used here. |
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Defines how profile records are proposed, validated, and admitted. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Defines retrieval eligibility and context assembly for profile views. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Defines change, suppression, expiry, and deletion processing. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Defines access, tenant, subject, and representation enforcement. |
| 08_MEMORY_GOVERNANCE_AND_CONSENT.md | Defines policy, consent, review, and accountability requirements. |
| 17_DIGITAL_CHANNEL_PLATFORM/README.md | Defines channel delivery and delivery-opt-in ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Memory profile and preference model with scoped records, precedence, views, and boundary protections. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

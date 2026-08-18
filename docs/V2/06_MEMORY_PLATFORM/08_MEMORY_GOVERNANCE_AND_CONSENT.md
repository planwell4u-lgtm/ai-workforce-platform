# 08_MEMORY_GOVERNANCE_AND_CONSENT

**Version:** 1.1
**Status:** Approved
**Owner:** Memory Platform Owner
**Phase:** Memory Platform

---

# Overview

This document defines the Memory-domain governance needed to decide which durable personal context may exist, for what purpose it may be used, who may review it, and how participant rights take effect. Governance makes memory policy explicit, reviewable, and reversible rather than allowing an agent, channel, connector, or provider to expand a profile silently.

Consent is one possible authorization basis for capture or use. It is not a generic checkbox, a channel-delivery opt-in, or a substitute for tenant policy, legal requirements, enterprise authorization, or lifecycle controls.

---

# Purpose

The governance model provides accountable control over memory types, evidence standards, risk tiers, purposes, consent/use bases, review, participant transparency, correction, suppression, deletion, exceptions, and audit. It protects participants while giving operators a clear path to administer authorized continuity context.

---

# Scope and Boundaries

| Topic | Owner |
|---|---|
| Memory policy requirements, record-category governance, consent/use interpretation for Memory, risk-tier review, participant-rights workflow, Memory decisions, and audit semantics | Memory Platform |
| Enterprise authorization, identity verification, compliance capabilities, audit infrastructure, security investigations, legal requirements, and secrets | 09_SECURITY_PLATFORM |
| Tenant/organization ownership, memberships, configuration, entitlement, and API-edge policy | 16_PLATFORM_FOUNDATION |
| Channel delivery opt-in/opt-out, message consent, and provider-specific channel rules | 04_VOICE_PLATFORM and 17_DIGITAL_CHANNEL_PLATFORM |
| Candidate intake/admission mechanics | 03_MEMORY_CAPTURE_AND_ADMISSION.md |
| Record correction, suppression, retention, deletion, hold, and invalidation mechanics | 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md |
| User/operator interface and notices | 10_FRONTEND_PLATFORM |

Memory governance uses Security and Foundation controls as inputs. It does not issue enterprise identity or legal determinations, nor does it manage channel delivery consent.

---

# Governance Principles

## Policy Before Category Enablement

A Memory record category is disabled until its approved policy defines purpose, eligible origins, evidence threshold, sensitivity, consent/use basis, retention, access audience, representation, review tier, quality criteria, and deletion obligations.

## Separate Capture, Use, and Delivery Permissions

Permission to receive a channel message does not automatically allow durable Memory capture. Permission to capture does not automatically allow every future use. A current interaction instruction may affect immediate service behavior without becoming durable Memory. Each decision has its own scope and evidence.

## Restrictive Rule Wins

When tenant policy, participant choice, classification, jurisdiction, security posture, source rights, channel rules, or legal/compliance guidance conflict, the most restrictive applicable rule governs ordinary capture and use until an accountable resolution is recorded.

## Participant Agency Is Operational

Where policy and law require it, participants can understand applicable memory, correct it, suppress use, withdraw a basis, request deletion/export, and use an authorized delegate. These requests change Memory lifecycle and access behavior; they are not merely support annotations.

## Automation Is Bounded

Automation may validate deterministic conditions and admit only low-risk candidates permitted by policy. It cannot create a new record category, broaden a purpose, weaken evidence, override a participant restriction, approve a high-risk inference, or resolve a material conflict without the configured accountable review.

## Governance Is Traceable

Policies, consent/use records, reviews, exceptions, participant requests, lifecycle decisions, and change approvals are versioned, attributable, time-bound, and linked to the affected Memory records/representations.

---

# Governance Objects

| Object | Meaning | Minimum content |
|---|---|---|
| `MemoryPolicy` | Versioned rule set for a Memory category/type and tenant/region scope. | Purpose, origins, evidence, classification, use basis, retention, access, review, quality, and deletion rules. |
| `UseBasisRecord` | Evidence that a specific capture or use is permitted under the applicable rule. | Basis type/reference, scope, subject, purpose, time, status, source, and withdrawal/expiry behavior. |
| `PolicyDecision` | Accountable application of policy to a candidate, record, request, or exception. | Policy version, evaluator, outcome, reason summary, effective time, and linked entities. |
| `ReviewAssignment` | Configured responsibility for a policy, candidate, conflict, participant request, or exception. | Role/actor, scope, due time, separation-of-duties requirement, and decision authority. |
| `ParticipantRequest` | A request for transparency, correction, suppression, withdrawal, deletion, export, or dispute. | Verified subject/delegate scope, request type, evidence, status, due/review time, and outcome. |
| `GovernanceException` | Time-bound approved deviation from a non-absolute rule. | Authority, reason, scope, compensating controls, expiry, and review cadence. |
| `GovernanceAuditEvent` | Privacy-minimized evidence of policy, review, request, access, or exception outcome. | Who/what/when/scope/decision/policy version/correlation reference. |

`UseBasisRecord` records Memory-domain applicability. It does not replace the Security Platform's authorization decision or a channel provider's consent state.

---

# Policy Requirements

Every enabled MemoryPolicy defines:

| Area | Required rule |
|---|---|
| Scope | Tenant, region/jurisdiction where applicable, record category/type/schema, and subject relationship. |
| Purpose | Specific allowed capture/use purposes and prohibited purposes; no generic "personalization" default. |
| Sources | Approved origin classes, source authority, verification, integrity, and freshness requirements. |
| Data handling | Classification, minimization, sensitive-data restrictions, residency/egress, and representation limits. |
| Use basis | Required basis type/evidence, capture-vs-use separation, withdrawal/expiry behavior, and notice requirements. |
| Admission | Risk tier, deterministic checks, review/separation-of-duties requirements, and conflict handling. |
| Access | Authorized audiences, operations, views/fields, exceptional-access conditions, and audit level. |
| Lifecycle | Freshness, expiry, retention, suppression, deletion, hold, restoration, and invalidation rules. |
| Quality | Accuracy, confidence, review, feedback, and harmful-memory-risk thresholds. |
| Operations | Monitoring, incident/escalation, test evidence, change approval, and provider constraints. |

An absent, expired, conflicting, or unapproved policy disables new admission and restricts use to the safest permitted outcome. It does not permit default capture or indefinite retention.

---

# Use-Basis and Participant Choice Model

## Basis Evaluation

For every capture and retrieval/use decision, Memory evaluates the current `UseBasisRecord` against the record category, tenant, subject, purpose, representation, region, time, and any required notice/verification condition. The evaluation is repeated when a decision is reused across a long-lived, asynchronous, delegated, or provider boundary.

## Withdrawal and Change

Withdrawal, suppression, opt-out, correction, or policy change takes effect according to its authorized scope and timing. It triggers lifecycle action and invalidation for affected records and representations. It must not be interpreted more broadly than its verified scope, but an ambiguous request is held/reviewed rather than narrowed for convenience.

## Delegates and Representatives

An authorized delegate can act only after subject relationship, authority, scope, and expiry have been verified through the appropriate Foundation/Security controls. Delegate access is purpose- and operation-specific and is recorded separately from the participant's own action.

## Notices and Transparency

Notices explain the Memory purpose, category, source class, available choice/correction path, and material limitations appropriate to the interaction. Notice delivery is not proof of consent/use basis unless the governing policy explicitly says so and records the required evidence.

---

# Decision Authority and Review

| Decision | Accountable authority | Minimum control |
|---|---|---|
| Enable/change Memory category or policy | Memory policy owner with Security/privacy and affected-owner review. | Versioned approval, impact assessment, tests, rollout/rollback. |
| Admit low-risk candidate | Authorized automated evaluator or reviewer defined by policy. | Deterministic evidence/policy/duplicate checks and audit. |
| Admit high-risk/inferred/disputed candidate | Configured accountable human or approved review body. | Strong evidence, separation of duties, enhanced audit, restrictive default. |
| Resolve conflict/correction | Authorized reviewer or participant-rights authority. | Evidence comparison, lifecycle action, outcome notice where required. |
| Suppress/delete/export request | Verified participant/delegate or authorized privacy role. | Scope verification, holds/exceptions review, completion evidence. |
| Grant exception | Named authority defined by policy. | Narrow scope, compensating controls, expiry, periodic review; never bypass absolute law/safety controls. |
| Restore restricted content | Authorized authority and new policy/evidence review. | New accountable decision; no silent restoration from storage/provider history. |

No actor may both introduce a high-risk policy change and be the sole required approver. A review assignment cannot be redirected to an agent/model without explicit policy and accountable human oversight.

---

# Participant Rights Workflow

```text
Verified participant or delegate request
    |
    +--> identify subject and requested scope without broad profile disclosure
    |
    +--> verify authority, request type, policy, and hold/exception conditions
    |
    +--> create ParticipantRequest and immediate lifecycle/access action if required
    |
    +--> review, correct/suppress/delete/export, or explain outcome
    |
    +--> invalidate representations, notify permitted consumers, and record evidence
    |
    +--> close only when required completion/exception evidence exists
```

Requests have visible status, accountable owner, due/review time, and privacy-safe communications. A request cannot force disclosure of protected internal evidence or another subject's information.

---

# Policy Change Management

A policy change affecting a record category, purpose, evidence threshold, consent/use basis, classification, access, retention, provider egress, or automated admission requires:

1. documented change proposal and affected-record assessment;
2. Security/privacy, Data, channel, Conversation, Agent, or Integration review where their boundary is affected;
3. compatibility/migration, invalidation, participant-notice, and rollback plan;
4. test evidence for positive, adverse, tenant, subject, rights, deletion, and provider cases;
5. versioned approval and staged release where risk requires; and
6. re-evaluation, suppression, or deletion of previously admitted records when the new policy narrows eligibility.

Policy changes never silently broaden an existing record's use. A broader purpose, audience, category, or representation requires a new valid basis and any required participant/owner review.

---

# Exceptions, Holds, and Incidents

An exception is allowed only for a non-absolute rule and is never a general bypass. It is narrow, time-bound, attributable, access-controlled, monitored, and removable. It cannot override tenant isolation, verified subject scope, an active security restriction, or a rule designated non-waivable by applicable policy/law.

Legal, security, dispute, and incident holds may preserve restricted evidence for a defined purpose, but they do not restore operational use. Incident response follows Security ownership; Memory supplies the affected-record, representation, lifecycle, and invalidation evidence needed to contain and remediate the impact.

---

# Governance Evidence and Metrics

Memory maintains privacy-minimized evidence for policy version/application, basis evaluation, review assignment/outcome, participant request state, exception, lifecycle result, access representation, and invalidation/deletion completion.

Required governance measures include policy coverage by record type, admission/rejection/hold rate by risk tier, review aging, correction/dispute rate, withdrawal/suppression time, deletion/exception completion, unauthorized/blocked access patterns, stale-policy use attempts, and quality/harm signals. Metrics inform review; they never auto-expand capture or policy scope.

---

# Integrity Invariants

- No Memory category or automated admission path is enabled without an approved current MemoryPolicy.
- Channel delivery consent, tenant membership, and authorization alone do not prove Memory capture or use permission.
- A withdrawal, suppression, policy narrowing, or lifecycle restriction overrides convenience, relevance, and a prior grant.
- Participant-rights requests have accountable ownership, tracked scope, lifecycle effect, and completion/exception evidence.
- Exceptions are narrow, expiring, reviewed, and never create an unbounded override or permanent policy change.
- Governance/audit evidence is minimized and access-controlled; it does not become a shadow personal-memory store.

---

# Related Documents

| Document | Relationship |
|---|---|
| 03_MEMORY_CAPTURE_AND_ADMISSION.md | Applies policy and review to candidate admission. |
| 05_MEMORY_RETRIEVAL_AND_CONTEXT.md | Applies purpose/use basis and representation constraints to retrieval. |
| 06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md | Applies participant requests, holds, and policy changes to lifecycle. |
| 07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md | Enforces governance decisions through access context. |
| 09_MEMORY_QUALITY_AND_EVALUATION.md | Uses governed quality signals and improvement proposals. |
| 10_MEMORY_SECURITY_AND_PRIVACY.md | Defines Security and privacy threat/control requirements. |
| 17_DIGITAL_CHANNEL_PLATFORM/README.md | Defines channel-delivery consent and transport ownership. |
| 09_SECURITY_PLATFORM/README.md | Defines enterprise authorization, compliance, audit, and incident ownership. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Memory governance and consent model with policy, use-basis, participant-rights, review, exception, and audit requirements. |
| 1.1 | 2026-08-06 | Finalized after review for completeness, ownership overlap, and long-term maintainability. |

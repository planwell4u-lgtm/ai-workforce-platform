# 18A_AGENT_MEMORY_INTEGRATION_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `18_AGENT_MEMORY_INTEGRATION.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Memory integration boundary.  

---

# Purpose

This draft defines how an Agent Platform execution uses governed Memory Platform capabilities. An agent may request an authorized memory recall, receive a bounded result, propose an observation for Memory admission, and use the returned context subject to current policy.

Memory Platform remains the authoritative owner of memory domain semantics: admission, profile and preference models, retrieval policy, persistence, lifecycle, retention, deletion, consent, quality, and governance. Data Platform supplies physical mechanisms, and Security Platform supplies the applicable identity, authorization, privacy, cryptographic, and audit controls.

---

# Ownership and Non-Ownership

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Memory admission, classification, consolidation, correction, suppression, and deletion | Memory Platform | Propose a bounded candidate observation only through the approved admission contract. |
| Memory profile, preference, relationship, and retrieval semantics | Memory Platform | Request a policy-approved recall and use the returned context only for the authorized execution. |
| Storage, vectors, cache, backup, restore, and lifecycle mechanisms | Data Platform | Never access storage directly or treat a cached value as canonical memory authority. |
| Identity, authorization, consent enforcement, encryption, secrets, and audit controls | Security Platform; consuming platforms apply them | Supply trusted execution context and honor denial, redaction, revocation, and scope changes. |
| Conversation/session continuity and canonical interaction state | Conversation Platform | Use supplied conversation context; do not create independent durable conversation memory. |
| Agent behavior, instructions, reasoning, and context composition | Agent Platform | Determine whether and how an authorized memory result can inform the current bounded execution. |

Memory returned to an Agent is context, not an instruction, permission, or source of truth that can override current policy, user input, or canonical domain records.

---

# Permitted Integration Flow

```text
Authorized execution begins with trusted tenant, subject, purpose, and conversation context
        ↓
Agent requests a policy-approved memory recall through the Memory Platform contract
        ↓
Memory Platform evaluates scope, consent, lifecycle, quality, and retrieval policy
        ↓
Agent receives a minimized, provenance-bearing result or a safe denial/no-result disposition
        ↓
Agent uses the result as bounded context under instruction and authorization controls
        ↓
Agent may propose a candidate observation through Memory admission; Memory decides whether to retain it
```

An Agent must not write a memory record, modify a profile, infer consent, retain recalled content outside approved bounds, or use a prior recall after material revocation, lifecycle, tenant, or policy change.

---

# Recall Request and Result Contract

A recall request contains only trusted and policy-required inputs:

- tenant, subject, actor, purpose, and execution references resolved by approved services;
- the authorized memory purpose and requested scope;
- relevant conversation or task references, not unrestricted prompt text or raw identifiers;
- a correlation reference and applicable policy/version information.

The Memory Platform returns a normalized result that can include:

- permitted, minimized memory items or a no-result/denial disposition;
- provenance, freshness, confidence, classification, and use constraints;
- consent, retention, redaction, or policy restrictions necessary for safe use;
- correlation and audit references without exposing internal storage or security details.

The Agent must treat all returned content as potentially incomplete and must not expose, summarize, or act on it outside the returned constraints and the current caller's authorization.

---

# Candidate Observation Contract

An agent can propose a memory candidate only when an approved behavior, purpose, and policy permit it. The candidate must be:

- narrowly scoped to an observed fact, preference, correction, or explicit request;
- attributed to the originating interaction and agent/version evidence;
- classified and minimized before transfer;
- free of secrets, prohibited content, speculative inference, and untrusted instructions;
- submitted through Memory admission, not direct persistence.

Memory Platform determines whether to accept, merge, defer, reject, redact, expire, or delete the candidate. An admission acknowledgement is not a claim that the information is correct, permanent, retrievable, or visible to the current participant.

---

# Context-Use Rules

- Memory may inform tone, relevance, clarification, and eligible behavior; it cannot override the current user, policy, instruction hierarchy, or authoritative domain data.
- The Agent must disclose or seek confirmation when required by Memory, Security, or product policy.
- Recalled context must be minimized in prompts, tool requests, telemetry, and participant-visible output.
- An agent must not use memory to link identities, infer sensitive attributes, make eligibility decisions, or expand access without explicit authorized policy.
- Memory use must be re-evaluated after tenant suspension, consent change, subject merge/split, deletion request, profile correction, or security containment.

---

# Failure and Safe Degradation

If Memory is unavailable, returns a denial, is stale, or is under reconciliation, the Agent proceeds only with the current authorized conversation context and an approved fallback. It must not manufacture continuity, use stale local copies, retry admission indefinitely, or treat absence of a memory response as permission.

Deletion, revocation, and correction events invalidate affected cached or assembled Agent context according to Memory and Security requirements. Any in-flight execution that cannot safely revalidate must restrict, defer, or terminate the memory-dependent behavior.

---

# Security, Privacy, and Tenant Isolation

Memory requests, results, and candidate observations are tenant-scoped, subject-scoped, purpose-limited, classification-aware, auditable, and minimized. The Agent must not receive or retain raw credentials, storage identifiers, unrestricted cross-subject results, or provider-internal details.

The Agent Platform does not implement memory retention, residency, erasure, legal hold, encryption, backup, or restore. It consumes the Memory, Data, and Security contracts that enforce those controls.

---

# Evidence and Validation

The integration must prove that:

- recall and admission require trusted tenant, subject, purpose, and authorization context;
- denied, revoked, expired, deleted, or cross-tenant content is not used or disclosed;
- an agent cannot write or mutate memory outside the Memory admission contract;
- provenance and use constraints survive context composition and downstream requests;
- Memory outages and uncertain outcomes degrade safely without fabricated continuity;
- sensitive values are minimized and excluded from unapproved prompts, logs, exports, and telemetry;
- correction and deletion events invalidate affected Agent context promptly enough for the relevant risk.

---

# Authoritative References

- `06_MEMORY_PLATFORM/03_MEMORY_CAPTURE_AND_ADMISSION.md`
- `06_MEMORY_PLATFORM/04_MEMORY_PROFILE_AND_PREFERENCE_MODEL.md`
- `06_MEMORY_PLATFORM/05_MEMORY_RETRIEVAL_AND_CONTEXT.md`
- `06_MEMORY_PLATFORM/06_MEMORY_LIFECYCLE_RETENTION_AND_DELETION.md`
- `06_MEMORY_PLATFORM/07_MEMORY_ACCESS_AND_TENANT_ISOLATION.md`
- `06_MEMORY_PLATFORM/08_MEMORY_GOVERNANCE_AND_CONSENT.md`
- `06_MEMORY_PLATFORM/10_MEMORY_SECURITY_AND_PRIVACY.md`
- `08_DATA_PLATFORM/09_DATA_ACCESS_AND_TENANT_ISOLATION.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`

---

# Approval Conditions

The Agent and Memory review confirmed this document's admission, recall, provenance, consent, lifecycle, invalidation, and failure boundaries. `18_AGENT_MEMORY_INTEGRATION.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.

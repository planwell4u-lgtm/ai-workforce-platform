# 10_CONVERSATION_SECURITY

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines the security requirements that apply specifically to canonical conversations, participants, interactions, sessions, context, routing, handoff, state changes, events, and operational access.

Conversation security protects the platform's One Brain, Multi-Channel model: a participant can continue an approved conversation across channels without a channel address, provider thread, session token, or agent execution becoming proof of identity, authorization, tenant membership, or entitlement.

---

# Purpose

The Conversation Security Model establishes how the Conversation Platform consumes enterprise security controls and applies them to conversation-domain decisions.

It ensures that every conversation operation is tenant-safe, purpose-bound, policy-checked, auditable, resilient to untrusted channel input, and limited to the minimum data and authority required.

---

# Objectives

The Conversation Security Model must:

- Apply identity, authentication, authorization, tenant, environment, purpose, consent, classification, residency, and retention checks to conversation operations.
- Treat channel/provider input, participant content, agent output, event payloads, external references, and derived views as untrusted until validated for their intended use.
- Prevent cross-tenant, cross-participant, cross-channel, stale-session, and confused-deputy access.
- Enforce least privilege and data minimization for participants, agents, human operators, workflows, services, and operational staff.
- Keep channel continuity separate from identity assurance and authorization.
- Protect handoff, context, state mutation, delivery, replay, recovery, and operational support paths.
- Produce useful security evidence without placing sensitive content, secrets, or private reasoning in routine telemetry.
- Support revocation, incident response, compliance review, and recovery without silently weakening controls.

---

# Scope

This document defines conversation-domain assets, principals, trust boundaries, authorization, identity assurance, input validation, data handling, lifecycle security, incident response, audit, testing, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise identity provider, credential issuance, MFA, key management, secrets vault, network security, SIEM, or organization-wide compliance program | 09_SECURITY_PLATFORM |
| Physical storage, encryption implementation, backup, replication, deletion execution, or residency infrastructure | 08_DATA_PLATFORM and 12_DEPLOYMENT_PLATFORM |
| Channel protocol, telephony/media security, provider credential management, or webhook transport implementation | 04_VOICE_PLATFORM and relevant Channel Platforms |
| Agent safety, tool permission, model/prompt security, private reasoning handling, or execution sandboxing | 02_AGENT_PLATFORM |
| MCP, external connector, CRM, ticketing, webhook, workflow-engine, or broker implementation | 07_INTEGRATION_PLATFORM |
| Generic event-broker authorization, telemetry infrastructure, incident operations, or enterprise monitoring implementation | Security, Observability, Integration, and Operations Platforms |
| Business retention schedules, legal interpretation, or enterprise data-classification policy | Security and Data Platforms with governance owners |

---

# Security Assets and Principals

## Protected Conversation Assets

| Asset | Security concern |
|---|---|
| Canonical conversation and state history | Unauthorized read, mutation, reopening, ownership change, or cross-tenant correlation. |
| Participant association and identity evidence | Impersonation, account linking error, visibility leakage, and inappropriate assurance reuse. |
| Interaction references and channel mappings | Provider-thread takeover, address exposure, replay, and cross-channel confusion. |
| Context snapshots and handoff grants | Oversharing, stale access, sensitive-content disclosure, and prompt-injection propagation. |
| Routing, ownership, queue, and handoff records | Unauthorized assignment, denial of service, conflicting participant action, and privilege escalation. |
| Events, projections, caches, and operational evidence | Tenant leakage, unauthorized replay, stale data use, and forensic gaps. |
| Policy, consent, classification, retention, and residency references | Bypass, stale evaluation, or improper lifecycle handling. |

## Principals

A principal is a participant, human operator, supervisor, agent service, workflow, channel gateway, integration service, event consumer, support operator, or automated recovery process acting through an authenticated identity.

Every principal is evaluated in relation to tenant, environment, role, purpose, conversation/participant scope, operation, assurance, classification, consent, lifecycle, and current authorization. A service identity is not a blanket entitlement to all conversations.

---

# Trust Boundaries

~~~text
Untrusted Participant / Provider / External System
    |
    v
Channel Validation and Normalization Boundary
    |
    v
Conversation Authorization and State Boundary
    |
    +--> Agent / Workflow Request Boundary
    +--> Context and Handoff Grant Boundary
    +--> Event and Projection Consumer Boundary
    +--> Human Operations and Support Boundary
~~~

## Channel and Provider Boundary

Provider callbacks, webhooks, caller identifiers, messaging addresses, browser/device claims, channel metadata, recordings, transcripts, attachments, and delivery reports are untrusted until channel-specific authenticity, replay, source-binding, normalization, tenant mapping, and schema checks succeed.

A verified provider request does not itself prove participant identity, consent, authority, or entitlement to protected conversation data.

## Conversation Boundary

Conversation Platform validates canonical identifiers, tenant/environment scope, principal, purpose, requested operation, lifecycle state, expected version where applicable, participant visibility, current policy, and authorization before it reads protected data or changes state.

## Cross-Platform Boundary

Agent, workflow, integration, event, analytics, and operations consumers receive only a defined contract and current authorization decision. Events, context references, routing assignments, handoffs, and sessions are not reusable credentials.

---

# Conversation Threat Model and Control Map

The Conversation Platform maintains a threat model that maps conversation-domain threats to preventive, detective, recovery, and test controls. The Security Platform owns the enterprise control implementations; Conversation Platform owns the domain conditions, evidence, and enforcement integration that make those controls effective.

| Threat | Required Conversation-domain control |
|---|---|
| Participant impersonation or unsafe account linking | Assurance-aware identity checks, explicit association evidence, operation-specific re-verification, and safe denial/fallback. |
| Cross-channel takeover | Current channel binding, recipient/visibility checks, consent evaluation, and no disclosure based only on a known address or provider thread. |
| Forged or replayed provider input | Authenticity, source binding, timestamp, schema, idempotency, and tenant/channel mapping validation before normalization. |
| Prompt injection or malicious content | Treat all received content as untrusted data; prevent it from changing policy, tenant, authority, routing, context scope, or operator instructions. |
| Sensitive-context or handoff leakage | Purpose-bound, minimum, expiring, revocable context grants with current authorization at retrieval. |
| Operator misuse or support browsing | Least privilege, purpose binding, separated capabilities, restricted views, audit, review, and break-glass controls. |
| Confused deputy or stale consumer action | Re-evaluate current policy, ownership, lifecycle, and recipient eligibility; events and references never confer permission. |

The threat model is reviewed whenever a new channel, identity-assurance route, context source, handoff/export path, high-risk state transition, or materially sensitive data category is introduced or changed.

---

# Authorization Model

## Authorization Decision

Each material conversation operation evaluates:

1. authenticated principal and service identity;
2. tenant, organization, and environment scope;
3. operation and requested resource scope;
4. principal role, relationship, and approved purpose;
5. participant identity-assurance and consent status;
6. classification, residency, retention, legal-hold, and lifecycle restrictions;
7. current conversation, work-owner, routing, handoff, session, and context conditions;
8. policy version and decision evidence.

Authorization is deny-by-default. A failed, unavailable, ambiguous, stale, or mismatched policy decision cannot be interpreted as permission for protected read, mutation, delivery, handoff, context access, replay, or operational repair.

## Least Privilege and Separation of Duties

Permissions are scoped to the operation and minimum conversation/participant/work segment required. Read, mutate, route, hand off, deliver, export, replay, repair, approve, and administer are separate capabilities.

No individual or service may both request and approve an exceptional repair, cross-tenant operation, high-risk export, or policy override unless a specifically governed emergency procedure permits it with enhanced audit.

## Purpose Binding

A permitted purpose is recorded for protected access, such as handling an active interaction, completing an approved handoff, resolving a controlled incident, performing retention work, or conducting authorized quality review. A broad operational role does not authorize unrelated browsing of conversations.

## Delegated and Support Access

Delegated access is explicit, limited, and auditable. An operator acting on behalf of a participant, tenant administrator, or support function records the delegating authority or approved support purpose, the permitted operation, affected scope, expiry, and any required participant notification.

Support access uses a restricted view by default. It must not silently impersonate a participant, inherit the participant's identity assurance, expose unrelated conversations, or perform participant-facing delivery without a separately authorized operation. Elevated support action follows the break-glass and separation-of-duties rules.

---

# Identity, Session, and Channel Continuity

## Identity Assurance

The platform records relevant assurance level and verification evidence reference, not unbounded credential material. Higher-risk operations may require stronger or refreshed verification according to policy.

Identity assurance is evaluated per participant and operation. It may not be silently transferred from one participant to another, from one tenant to another, or from a less secure to a more sensitive channel.

## Session and Device Binding

Sessions are bounded and cannot become permanent authorization artifacts. A session, device, browser, call, or provider identifier must be bound to current tenant, participant, channel, expiry, and assurance conditions before it can support an authorized conversation operation.

Session expiry, sign-out, revocation, account change, participant removal, suspicious activity, consent withdrawal, or policy change invalidates dependent conversation access according to current policy.

## Cross-Channel Continuation

Channel continuity requires explicit mapping and authorization. A known phone number, email address, messaging account, browser token, or provider thread alone must not reveal a conversation, attach to it, or receive a sensitive summary without the required identity and consent checks.

---

# Input, Content, and Reference Validation

## Untrusted Content

Participant text, voice transcription, attachments, provider metadata, tool results, retrieved documents, event payloads, and agent-generated content are data, not instructions or permission. They cannot override system policy, authorize an action, select a tenant, modify routing, expand context, or direct an operator to disclose protected data.

## Inbound Validation

Before a channel input becomes a normalized interaction or state-transition candidate, the platform validates source authenticity where available, replay/idempotency, schema, size/type limits, malware/content scanning where applicable, tenant/channel binding, recipient/destination mapping, timestamp/clock tolerance, and correlation safety.

Rejected or quarantined input retains only the restricted evidence required for security, operations, and legal policy.

## Reference Integrity

Conversation, participant, session, interaction, context, routing, handoff, event, and external-work references are opaque identifiers. A reference must be validated within current tenant, environment, resource relationship, authorization, and purpose; possession of an identifier is not authorization.

## Abuse and Fraud Safeguards

Conversation Platform supplies the domain signals needed for enterprise abuse and fraud controls: interaction/request rate, repeated denied verification, unusual channel association, repeated handoff or export attempt, suspicious replay, recipient mismatch, rapid ownership change, and policy-denial pattern.

Rate limits, quotas, detection engines, and operational response infrastructure are owned by Security and Operations Platforms. When a configured threshold or signal applies, Conversation Platform enforces the registered domain response: throttle, require stronger verification, defer to a safe queue, restrict a high-risk operation, suspend ordinary processing, or escalate for authorized review. A protective action is recorded with reason, scope, expiry, and recovery path.

---

# Data Handling and Context Protection

## Data Minimization

Conversation state, event envelopes, routing records, handoff records, audit evidence, logs, traces, and metrics contain the minimum identifiers and protected references needed for their purpose. They do not carry secrets, raw credentials, unrestricted transcripts, recordings, attachments, personal data, hidden instructions, or private model reasoning by default.

## Classification and Visibility

Every protected operation applies current classification, participant visibility, consent, residency, retention, and legal-hold restrictions. A conversation membership or handoff relationship does not automatically permit a participant, agent, operator, workflow, or supervisor to see all content or all participants.

## Context and Handoff Grants

Context snapshots and handoff grants are purpose-bound, scope-bound, expiry-bound, and revocable. Retrieval rechecks current authorization. A recipient may not reuse a reference after handoff completion, session expiry, participant removal, consent withdrawal, access downgrade, or policy revocation.

## Export and Disclosure

Conversation export, transcript/recording retrieval, summary delivery, cross-channel sharing, external ticket update, and data-subject response use separate approved operations. They record destination, purpose, classification, recipient assurance, minimization, authorization, delivery result, and audit evidence.

---

# Secure State, Routing, and Handoff Operations

## State Mutation

Every mutation uses the controlled state-operation contract with authenticated principal, expected version, allowed transition, policy decision, tenant scope, idempotency, and audit evidence. Events, projections, caches, and provider callbacks never directly write canonical state.

## Routing and Delivery

A routing result is not a delivery permission. Before participant-facing output, the active owner and channel path revalidate tenant, recipient/participant visibility, consent, channel eligibility, lifecycle, classification, delivery policy, and current authorization.

## Handoff and Human Access

A handoff creates no blanket human access. The receiving party obtains only the approved, time-bounded context and operations for its work segment. Queue membership, supervisor role, or support access is evaluated at use time and must not expose a full conversation by default.

## High-Risk and Emergency Operations

Exceptional recovery, repair, urgent safety escalation, and incident response use a pre-approved break-glass process where policy permits. It requires explicit reason, minimum scope, time limit, elevated authentication where available, independent review, immutable audit evidence, and post-use revocation/review. Emergency access does not bypass tenant isolation or legal constraints.

---

# Event, Projection, and Operational Security

Conversation event publication and consumption follows 07_CONVERSATION_EVENTS.md. Event receipt does not grant conversation, tool, workflow, delivery, or state-mutation authority.

Projection, cache, search, analytics, support, and quality-review access is separately authorized and version/freshness-aware. Restricted data is redacted, minimized, or unavailable according to current policy; a historical projection or log cannot override current consent or authorization.

Replay, dead-letter inspection, reconciliation, repair, and backup/restore operations are controlled, tenant-scoped, classification-aware activities. They validate current policy and external-side-effect risk before acting.

---

# Revocation, Incident Response, and Recovery

## Revocation

The platform responds to revoked identity, session, role, consent, channel mapping, participant association, context/handoff grant, tenant access, or policy eligibility by denying subsequent use and invalidating relevant derived views and active grants according to policy.

Revocation is not dependent on expiry alone. Where active execution or external delivery may still be in progress, the platform records the revocation effect and invokes controlled cancellation, safe drain, or reconciliation through the owning Agent, Channel, or Integration contract.

## Incident Handling

A suspected unauthorized access, cross-tenant reference, forged provider input, suspicious continuity attempt, data leak, policy bypass, or integrity failure is quarantined and correlated with tenant/classification, principal, resource scope, evidence, impact, and required escalation.

Conversation Platform preserves the minimum evidence needed for investigation and invokes Security/Operations incident procedures. It does not independently decide breach notification, legal disclosure, credential rotation, or enterprise remediation.

## Security Change Review

Before activation, a material conversation change receives security review appropriate to its risk. Review is required for a new channel or provider, identity/continuity path, sensitive context source, export/disclosure destination, human handoff path, high-risk lifecycle transition, delegated-access capability, or change to authorization/visibility semantics.

The change record identifies affected assets and principals, threat-model updates, policy/control dependencies, data classification, tenant/residency implications, abuse considerations, test evidence, rollback/revocation path, and accountable approver. The review does not replace normal release, privacy, or operational approval.

---

# Audit and Observability

Audit evidence records the principal/service category, operation, tenant/environment, conversation/participant scope, purpose, decision result, policy/authorization references, assurance, classification, correlation, timing, and outcome. It avoids raw sensitive content unless a separately governed security record requires it.

Security signals include authentication/authorization failure, tenant mismatch, reference misuse, suspicious channel association, invalid provider input, replay, repeated denial, privilege escalation attempt, restricted-context retrieval, export/disclosure attempt, break-glass use, stale session, integrity mismatch, and failed revocation.

---

# Testing Strategy

## Authorization and Isolation Tests

Validate deny-by-default behavior, tenant/environment isolation, participant visibility, least privilege, purpose binding, role separation, session/device binding, and current-policy re-evaluation.

## Adversarial Input Tests

Simulate forged webhook, provider replay, malformed or oversized input, prompt injection in participant content, malicious attachment/reference, confused tenant mapping, spoofed caller/address, stale browser/session token, and manipulated event payload.

## Lifecycle and Recovery Tests

Simulate consent withdrawal, participant removal, channel change, handoff completion, session expiry, policy downgrade, legal hold, break-glass access, revocation during active execution, dead-letter inspection, replay, repair, and incident quarantine. Prove no test creates unauthorized access, state change, content disclosure, or participant-facing action.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation authorization matrix | Defines principal, operation, resource scope, purpose, assurance, policy, and denial behavior | Conversation Platform with Security owner |
| Trust-boundary and input-validation contract | Defines channel/provider, agent/workflow, event, reference, and operations validation requirements | Conversation Platform with Channel, Agent, Integration, and Security owners |
| Participant assurance and continuity policy | Defines identity-assurance, channel binding, cross-channel continuation, session, and revocation rules | Conversation Platform with Security and Channel owners |
| Context/handoff access policy | Defines grant scope, minimization, expiry, revocation, export, and audit | Conversation Platform with Context, Handoff, and Security owners |
| Conversation threat model and control map | Defines threats, applicable domain controls, evidence, review triggers, and test coverage | Conversation Platform with Security owner |
| Abuse and delegated-access policy | Defines domain signals, safe protective responses, support scope, impersonation prevention, and review | Conversation Platform with Security and Operations owners |
| Security event and incident playbook | Defines detection, quarantine, evidence, escalation, and incident boundary | Conversation Platform with Security and Operations owners |
| Conversation security test suite | Validates authorization, isolation, adversarial input, lifecycle, revocation, and recovery | Conversation Platform with Testing Platform |

---

# Anti-Patterns

## Phone Number or Thread Equals Identity

A channel address or provider thread can support continuity only after current identity and authorization checks. It is never sufficient proof of identity or access.

## Event Receipt Grants Permission

An event is a fact. It cannot authorize a consumer to read conversation content, change state, run a tool, or send a message.

## Handoff Grants Full Transcript Access

A handoff grants only a limited, purpose-bound context view; it does not make a recipient a permanent owner of all conversation data.

## Provider Validation Equals Business Authorization

A valid signed webhook confirms a source claim; it does not prove participant consent, tenant entitlement, or permission for a protected operation.

## Cached State Is Treated as Current Policy

A cache or projection cannot decide sensitive access or participant-facing delivery without required current-state and policy validation.

## Emergency Access Has No End

Break-glass access must be narrow, temporary, auditable, reviewed, and revoked. It is not a general operational shortcut.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform security boundaries. |
| 03_CONVERSATION_MODEL.md | Defines protected conversation, participant, interaction, and mapping references. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines session continuity and lifecycle. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines context authorization, snapshots, and lifecycle. |
| 06_CONVERSATION_ROUTING.md | Defines safe destination eligibility and routing. |
| 07_CONVERSATION_EVENTS.md | Defines conversation-event contracts and consumer controls. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines controlled transfer and human collaboration. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines canonical state, mutation, integrity, and recovery. |
| 02_AGENT_PLATFORM | Defines agent-specific safety, execution, tools, and permissions. |
| 04_VOICE_PLATFORM | Defines voice and telephony security details. |
| 07_INTEGRATION_PLATFORM | Defines external connection and workflow implementation. |
| 08_DATA_PLATFORM | Defines data storage and lifecycle implementation. |
| 09_SECURITY_PLATFORM | Defines enterprise security controls and compliance governance. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Conversation Security document. |
| 2.1 | 2026-08-06 | Added threat/control mapping, abuse safeguards, delegated-support controls, and security-change review requirements. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

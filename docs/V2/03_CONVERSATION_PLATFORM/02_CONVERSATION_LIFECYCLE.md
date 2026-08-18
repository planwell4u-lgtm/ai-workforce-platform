# 02_CONVERSATION_LIFECYCLE

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines the canonical lifecycle of a conversation from creation through active interaction, waiting, handoff, suspension, closure, archival, and deletion or anonymization where policy permits.

A conversation lifecycle is distinct from a call, browser session, agent runtime execution, workflow instance, or delivery attempt. Those may occur within a conversation, but Conversation Platform owns the durable canonical lifecycle.

---

# Purpose

The purpose of the Conversation Lifecycle Model is to make conversation state explicit, auditable, tenant-safe, and recoverable across channels and participants.

It prevents silent reopening, abandoned state, conflicting ownership, unsafe context reuse, and inconsistent behavior when interactions arrive late, duplicate, out of order, or after closure.

---

# Objectives

The Conversation Lifecycle Model must:

- Define canonical states, transitions, ownership, and terminal behavior.
- Preserve safe continuity across approved channel changes, agent executions, workflows, and human handoff.
- Re-evaluate tenant, identity, consent, classification, authorization, and purpose before continuation or reopening.
- Support inactivity, closure, reopening, archival, retention, deletion, and controlled restoration.
- Provide durable history, events, concurrency, audit, recovery, and observability evidence.
- Prevent duplicate, delayed, or conflicting interactions from corrupting canonical state.
- Remain independent of channel providers, storage engines, and workflow frameworks.

---

# Scope

This document defines states, transitions, triggers, guards, inactivity, handoff, suspension, closure, reopening, archival, recovery, events, security, tenant controls, observability, and lifecycle testing.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Channel call, media, provider thread, or delivery lifecycle | Voice and relevant Channel Platforms |
| Agent execution, reasoning, model invocation, capability, and tool lifecycle | 02_AGENT_PLATFORM |
| Workflow process state and business compensation lifecycle | 07_INTEGRATION_PLATFORM |
| Session coordination details | 04_CONVERSATION_SESSION_MODEL.md |
| Conversation record and participant/channel mapping schema | 03_CONVERSATION_MODEL.md |
| Context composition and snapshot lifecycle | 05_CONVERSATION_CONTEXT_MODEL.md |
| Routing and handoff assignment policy | 06_CONVERSATION_ROUTING.md and 08_CONVERSATION_HANDOFF_MODEL.md |
| Storage, backup, legal hold, deletion, and residency implementation | 08_DATA_PLATFORM and 09_SECURITY_PLATFORM |

---

# Lifecycle Principles

## Canonical State Has One Owner

Only Conversation Platform transitions canonical conversation lifecycle state. Channels, agents, workflows, tools, and humans request transitions through governed contracts; they do not write lifecycle state directly.

## Closed Does Not Mean Forgotten

Closure ends ordinary active interaction. It does not erase audit history, retention obligations, or access controls. Archived history is not automatically loaded into a new context.

## Reopening Is a New Decision

A closed or archived conversation must pass current tenant, identity, participant relationship, purpose, classification, consent, and authorization checks before it is reopened. Historical association is not perpetual permission.

## State Changes Are Durable Facts

A transition is durably recorded before dependent events are acknowledged. It includes actor/source, reason, expected/resulting state, tenant, policy references, correlation, and audit evidence.

## Lifecycle Is Channel Independent

A call ending, email delivery, or browser closure does not automatically close the canonical conversation. Policy considers purpose, waiting work, participants, channel constraints, and tenant rules.

---

# Lifecycle States

~~~text
Created
    -> Active
    -> Waiting
    -> Handed Off
    -> Suspended
    -> Closed
    -> Archived
    -> Deleted or Anonymized
~~~

| State | Meaning |
|---|---|
| Created | Tenant-scoped record and initial policy/participant/channel evidence exist; processing may not yet be eligible |
| Active | Authorized interactions may be accepted and routed |
| Waiting | The conversation awaits a participant, verification, workflow, external result, or scheduled continuation |
| Handed Off | An authorized human queue/operator or collaboration mode owns the next step |
| Suspended | Ordinary processing is blocked by security, tenant, policy, legal, integrity, or incident condition |
| Closed | Active interaction reached controlled completion, termination, or expiry; normal continuation requires reopening |
| Archived | Retained outside normal active processing with restricted authorized access |
| Deleted or Anonymized | Removed or irreversibly de-identified under approved lifecycle policy |

---

# State Transition Rules

| From | To | Trigger | Required guard |
|---|---|---|---|
| Created | Active | Valid interaction or approved continuation | Tenant, participant, purpose, classification, and routing eligibility valid |
| Created | Suspended | Security/policy/tenant block found | Durable reason and safety disposition recorded |
| Active | Waiting | Awaiting participant, workflow, verification, or external result | Reason, owner, expiry, and continuation path recorded |
| Waiting | Active | Approved participant/event/workflow continuation | Current tenant, identity, consent, lifecycle, and dependency checks pass |
| Active or Waiting | Handed Off | Escalation, review, or participant request | Queue/role, allowed context, and handoff policy valid |
| Handed Off | Active | Authorized return to agent/collaboration mode | Human disposition, policy, and routing eligibility valid |
| Active, Waiting, or Handed Off | Suspended | Security, tenant, integrity, legal, or incident condition | Authorized source and safe disposition recorded |
| Suspended | Active or Waiting | Authorized remediation/resumption | Tenant, policy, identity, consent, and integrity revalidated |
| Active, Waiting, Handed Off, or Suspended | Closed | Completion, request, expiry, or controlled termination | Closure reason, unresolved work, and retention reference recorded |
| Closed | Active | New eligible continuation or explicit reopen | Reopen decision and current policy/participant checks valid |
| Closed | Archived | Retention transition | Archive policy conditions satisfied |
| Archived | Active | Exceptional restore/reopen | Current legal, tenant, purpose, access, and data checks valid |
| Archived | Deleted or Anonymized | Retention/deletion policy | Authorized Data/Security lifecycle action completed |

No transition is valid solely because a channel/provider reports activity.

---

## Transition Authority Matrix

| Transition class | May request | May authorize | Executes canonical transition |
|---|---|---|---|
| Create or activate | Validated channel/API/event source, agent/workflow boundary, human operator | Routing and policy controls | Conversation Platform |
| Wait or resume | Agent/workflow outcome, participant input, scheduler, human operator | Lifecycle/routing policy | Conversation Platform |
| Handoff or return | Agent, participant, workflow, queue, human operator | Handoff/routing and permission policy | Conversation Platform |
| Suspend or withdraw | Security, tenant, incident, governance, or authorized operator process | Applicable security/tenant/operations authority | Conversation Platform |
| Close or reopen | Participant, agent/workflow outcome, scheduler, human operator | Lifecycle, participant, purpose, consent, and policy checks | Conversation Platform |
| Archive, restore, delete, anonymize | Data lifecycle, legal, tenant, or authorized operator process | Data/Security/retention policy | Conversation Platform records transition after owning action |

Requesting a transition is not approval. The Conversation Platform validates current state, tenant, policy, expected version, and required authority before recording the resulting state.

---

# Creation and Activation

A conversation may be created by a validated channel interaction, authorized API request, approved event, scheduled workflow interaction, human support action, or controlled migration/restore process.

Creation records source, tenant, participant evidence, channel mapping, purpose, classification, correlation, and idempotency key. Repeated source input resolves to the existing controlled outcome rather than creating a duplicate conversation.

A Created conversation becomes Active only after policy validates that processing is allowed. Activation may route to an agent, human queue, verification path, or safe deferment. It does not grant destination access to all conversation data or permission to act externally.

---

# Waiting, Handoff, and Suspension

## Waiting

Waiting state records reason, owner, expiry, reminder/follow-up policy, channel restrictions, and safe fallback. A delayed input cannot awaken it automatically; continuation re-evaluates current policy, tenant, identity, consent, classification, and idempotency.

## Handoff

Handoff changes conversation ownership or collaboration mode, not tenant, classification, or permission scope. Human operators receive only authorized context. Return to an agent creates a new authorized execution/session association; it does not revive an old execution.

## Suspension

Suspension blocks ordinary processing while permitting only authorized notice, review, or recovery. It records reason, owner, allowable actions, review/expiry, and resumption or closure path. It is not a hidden retry queue.

---

## Lifecycle Time Policy

Tenant policy defines bounded durations for active inactivity, waiting, handoff, suspension review, reopening eligibility, archival, and deletion/anonymization. Durations may vary by risk, channel, classification, participant expectation, regulatory obligation, and business purpose.

Every time-bound state records policy version, start time, expiry, owner, reminder/follow-up behavior, and safe disposition at expiry. A timeout does not authorize less-secure-channel delivery, automatic external action, or bypass of current identity and consent checks.

## Participant Notification

The notification policy identifies which state transitions require participant notice, approved channel, wording/disclosure, delivery confirmation, fallback, and human ownership. Typical notification candidates include handoff, suspension that materially affects the user, deferred work, closure where confirmation is expected, and authorized reopen.

Failure or uncertainty in notification is recorded separately from the lifecycle transition. The platform does not claim a participant was informed merely because a delivery request was submitted.

---

# Closure, Reopening, Archival, and Retention

## Closure

Closure records business disposition, reason, final participant/handoff state, unresolved work references, last authorized delivery outcome, active-session disposition, retention classification, and audit evidence.

Closure does not claim that uncertain external actions succeeded. Such outcomes remain linked to reconciliation or controlled follow-up.

## Reopening

Reopening is explicit. The resolver verifies current participant, tenant, purpose, classification, consent, identity assurance, channel eligibility, and policy. It creates a new active session/execution context and records the historical relationship.

When continuity is not justified or permitted, a new conversation is created instead.

## Archival and Restoration

Archival removes a conversation from normal active processing while preserving protected history. Restoration is exceptional and checks legal hold, retention, tenant state, purpose, participant access, and data availability before an active or waiting transition.

## Deletion and Anonymization

Data and Security lifecycle processes implement deletion/anonymization. Conversation Platform records the controlled transition and stops normal access after completion; it does not retain duplicate content for convenience.

---

## Retention and Legal-Hold Precedence

Legal hold, investigation, regulatory retention, residency, and approved Data/Security policy take precedence over ordinary archive, deletion, anonymization, export, or restoration requests. A lifecycle request that conflicts with a higher-precedence restriction is blocked or transformed into the permitted restricted state with an audit reason.

Retention constraints do not broaden access. A record retained for legal or operational reasons remains tenant-scoped, classified, and accessible only through current authorization.

---

# Concurrency, Ordering, and Recovery

Every mutable conversation has a state version or equivalent concurrency token. A transition supplies the expected version; on conflict, the caller re-resolves current lifecycle, policy, and routing rather than overwriting newer state.

Global ordering is not assumed. Source sequence and occurrence time are retained when available, and delayed/out-of-order interactions are validated against canonical state.

After restart or failover, the platform recovers only durable lifecycle state, transition history, and authorized references. It does not use transient model context, provider session memory, or channel cache as source of truth.

---

## Lifecycle-to-Session and Work Matrix

| Conversation transition | Required session/work behavior |
|---|---|
| Active to Waiting | Complete or safely pause current session; persist approved follow-up/work references; block unapproved further delivery |
| Active/Waiting to Handed Off | Create governed human assignment; constrain agent execution according to handoff policy; preserve authorized context reference |
| Active/Waiting/Handed Off to Suspended | Cancel, defer, or quarantine active sessions and work; prevent new tool/workflow/delivery action except authorized safety/recovery work |
| Any active state to Closed | End or safely complete active sessions; preserve unresolved work for reconciliation; prevent ordinary new delivery/execution |
| Closed/Archived to Active | Create a new authorized session and execution context; do not revive stale runtime state or expired delegation |
| Any state to Deleted/Anonymized | Revoke ordinary access; stop pending work unless an authorized legal/security process retains it |

The detailed session and workflow behavior is defined by their owning models. This matrix establishes the required lifecycle boundary.

## Lifecycle Migration and Reconciliation

When lifecycle state definitions, transition guards, or policy versions change, the Conversation Platform maintains a migration plan for active and historical conversations. The plan identifies affected states, compatibility, owner, rollout, audit, rollback, and required revalidation.

Conflicting channel, agent, workflow, human, or scheduler requests are resolved using current lifecycle state, expected version, authority, policy precedence, participant/tenant conditions, and durable evidence. Suspension, legal/security restriction, and deletion/retention constraints take precedence over ordinary continuation. Ambiguous conflicts are preserved for authorized review rather than silently resolved by arrival order.

---

# Lifecycle Events and Audit

Conversation Lifecycle publishes governed facts after durable transitions:

- conversation.created
- conversation.activated
- conversation.waiting
- conversation.handoff_requested
- conversation.handed_off
- conversation.suspended
- conversation.closed
- conversation.reopened
- conversation.archived
- conversation.deleted_or_anonymized

Each event includes tenant, conversation reference, transition, reason, actor/source, correlation, causation, trace, classification, and schema version. An event does not grant permission to retrieve content, reopen a conversation, or deliver a message.

---

# Security, Privacy, and Tenant Controls

Transitions are tenant-scoped, purpose-bound, classified, authorized, and audited. Missing tenant context, conflicting participant identity, revoked consent, expired delegation, invalid channel mapping, or unauthorized operator request fails closed.

Closure, archival, deletion, and restoration apply current data, security, retention, legal, and residency policy. A historical reference does not grant content access or permission to restore it.

---

# Observability and Service Indicators

The platform emits transition rate, active/waiting/handed-off/suspended/closed inventory, transition latency, stale waiting state, handoff duration, reopen rate, suspension duration, archive/deletion completion, conflict, recovery outcome, and unauthorized transition attempt.

Conversation Platform owns the meaning of these signals; Operations and Observability Platforms own telemetry infrastructure and alerting.

---

# Testing Strategy

## Contract Tests

Validate states, transition schema, guards, idempotency, events, audit fields, state versioning, and error categories.

## Integration Tests

Validate channel creation, routing activation, agent execution association, workflow waiting/continuation, human handoff/return, delivery outcome, closure, reopening, archive, and authorized restoration.

## Security and Tenant Tests

Validate cross-tenant transitions, unauthorized reopen, stale delegation, revoked consent, invalid participant mapping, restricted archive access, deletion/anonymization, and operator recovery scope.

## Resilience Tests

Simulate duplicate interaction, out-of-order callback, concurrent transition, restart, waiting expiry, provider outage, ambiguous external outcome, security suspension, replay, and restore. Prove no duplicate conversation, silent reopen, state overwrite, or unauthorized context exposure.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation lifecycle state schema | Defines states, reasons, transitions, terminal behavior, and versioning | Conversation Platform |
| Transition guard and policy table | Defines tenant, identity, consent, classification, authorization, and dependency checks | Conversation Platform with Security owner |
| Transition-authority matrix | Defines requester, approver, executor, separation of duties, and audit for each transition class | Conversation Platform with Security and Operations owners |
| Inactivity and waiting policy | Defines reasons, owner, expiry, reminders, follow-up, and closure behavior | Conversation Platform and tenant owner |
| Lifecycle time and notification policy | Defines durations, expiry, participant notice, delivery evidence, fallback, and owner | Conversation Platform with Channel and tenant owners |
| Reopen, archive, and restoration procedure | Defines current-policy checks, access, retention, legal, and audit behavior | Conversation Platform with Data and Security owners |
| Retention and legal-hold precedence policy | Defines lifecycle restrictions, priority, audit, access, and permitted states | Conversation Platform with Data and Security owners |
| Lifecycle event registry | Defines schemas, producer, consumer, retention, and replay controls | Conversation Platform with Integration owner |
| Lifecycle-to-session/work matrix | Defines active-session, execution, workflow, tool, delivery, and reconciliation behavior by transition | Conversation Platform with Agent and Integration owners |
| Lifecycle migration and reconciliation procedure | Defines policy/state migration, conflict precedence, review, evidence, rollout, and rollback | Conversation Platform with Data, Security, and Operations owners |
| Lifecycle SLI/SLO catalog | Defines state, transition, handoff, suspension, recovery, and retention measures | Conversation, Operations, and Observability owners |
| Lifecycle test suite | Validates contracts, integration, security, tenant, resilience, and recovery behavior | Conversation Platform and Testing Platform |

---

# Anti-Patterns

## Call End Means Conversation Closed

A call, browser, or channel connection ending does not necessarily end the business conversation. Apply explicit lifecycle policy.

## Reopen by Identifier Alone

Knowing a conversation ID, phone number, email thread, or provider message ID does not authorize reopening or context access. Re-evaluate current identity, tenant, purpose, and policy.

## Last Write Wins

Overwriting state on concurrent or delayed updates can erase handoff, closure, suspension, or security conditions. Use expected-version transitions and reconciliation.

## Waiting Forever

An unbounded waiting conversation obscures ownership and creates stale context. Every waiting state needs reason, owner, expiry, and continuation/closure behavior.

## Archive as Broad Access Store

Archived conversations remain classified, tenant-scoped, and authorized. They are not broad support, analytics, or agent-context storage.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform ownership and components. |
| 03_CONVERSATION_MODEL.md | Defines canonical conversation, participant, and interaction records. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines active-session coordination and execution association. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines authorized context snapshots and context lifecycle. |
| 06_CONVERSATION_ROUTING.md | Defines routing eligibility across lifecycle states. |
| 07_CONVERSATION_EVENTS.md | Defines event contracts and subscriptions. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines handoff and collaboration transitions. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines state concurrency, recovery, and reconciliation. |
| 10_CONVERSATION_SECURITY.md | Defines identity, consent, classification, access, and privacy. |
| 11_CONVERSATION_OBSERVABILITY.md | Defines lifecycle telemetry and service objectives. |
| 12_CONVERSATION_TESTING.md | Defines Conversation Platform testing strategy. |
| 02_AGENT_PLATFORM/32_AGENT_FAILURE_HANDLING.md | Defines agent-side failure and reconciliation behavior. |
| 08_DATA_PLATFORM | Owns storage, retention, backup, restoration, and deletion implementation. |
| 09_SECURITY_PLATFORM | Owns enterprise identity, authorization, privacy, and compliance policy. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Lifecycle document. |
| 2.1 | 2026-08-05 | Added transition authority, timing, notifications, session/work behavior, retention precedence, migration, reconciliation, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

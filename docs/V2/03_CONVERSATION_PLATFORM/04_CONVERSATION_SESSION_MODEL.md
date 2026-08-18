# 04_CONVERSATION_SESSION_MODEL

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform coordinates active interaction sessions within canonical conversations.

A conversation is durable business continuity. A session is a bounded coordination window for a live or asynchronous interaction, such as a voice call, chat visit, messaging exchange, email response cycle, API stream, human handoff, or agent execution association. A conversation may have many sessions over time.

---

# Purpose

The purpose of the Conversation Session Model is to safely connect channel activity, participant presence, routing, context, agent execution, workflow continuation, and human handoff to a canonical conversation without making transient runtime or provider state authoritative.

It prevents session fixation, stale continuation, cross-channel confusion, duplicate execution, unsafe resumption, and loss of continuity during failure or handoff.

---

# Objectives

The Conversation Session Model must:

- Separate durable conversation lifecycle from bounded active-session coordination.
- Define session identity, ownership, channel association, participant presence, execution links, expiry, and recovery.
- Support voice, chat, messaging, email, API, event-triggered, and human-assisted interaction patterns.
- Bind every session to one tenant and one canonical conversation when a conversation applies.
- Require current identity, consent, policy, purpose, classification, and authorization before resumption or sensitive continuation.
- Prevent duplicate, concurrent, stale, or cross-tenant session action.
- Provide controlled session handoff, channel switching, expiry, cancellation, and audit evidence.
- Remain independent of provider session IDs, agent runtime worker processes, and workflow-engine state.

---

# Scope

This document defines session concepts, states, associations, lifecycle, continuity, concurrency, recovery, security, observability, and testing. It defines how sessions reference agent execution and workflow/handoff work; it does not own agent or workflow state.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Canonical conversation entities and lifecycle | 02_CONVERSATION_LIFECYCLE.md and 03_CONVERSATION_MODEL.md |
| Agent runtime execution state, model context, or reasoning | 02_AGENT_PLATFORM |
| Channel media, provider call/session, delivery, or transport state | Voice and relevant Channel Platforms |
| Workflow state, scheduled work, compensation, or external action | 07_INTEGRATION_PLATFORM |
| Context content composition and snapshot rules | 05_CONVERSATION_CONTEXT_MODEL.md |
| Routing/handoff policy and queue behavior | 06_CONVERSATION_ROUTING.md and 08_CONVERSATION_HANDOFF_MODEL.md |
| Identity, authorization, consent, security policy, and storage implementation | Security and Data Platforms |

---

# Session Principles

## Session Is Not Conversation

A session is a time-bounded coordination record. Ending a session does not automatically close a conversation; closing a conversation safely ends or detaches its active sessions.

## One Tenant and One Parent Conversation

A session has one immutable tenant owner and, where participant interaction applies, one parent canonical conversation. Event-only work may have no conversation only when policy permits and its purpose is explicit.

## Provider ID Is a Mapping

A call SID, web socket, browser tab, channel thread, or API stream is external evidence mapped to a session after validation. It is not a bearer credential or authoritative session identity.

## Session Does Not Grant Authority

A valid session reference does not authorize context retrieval, tool use, external action, delivery, or participant association. Every material action uses current permission, tenant, consent, classification, and policy checks.

## Resume Is Reauthorization

Resuming after inactivity, reconnect, handoff, workflow wait, agent retry, or channel switch revalidates current conversation state, participant evidence, tenant, identity, consent, purpose, classification, and policy.

---

# Session Model

~~~text
Conversation
    |
    +-- Session
         +-- Channel/Provider Mapping
         +-- Participant Presence Reference
         +-- Agent Execution Reference
         +-- Workflow/Handoff Reference
         +-- Authorized Context Snapshot Reference
         +-- State, Expiry, and Correlation
~~~

## Required Session Attributes

A session has session ID, tenant, parent conversation reference when applicable, session type, channel/provider mapping reference, participant association, purpose, classification, state, expected version, created/updated/expiry time, context/authorization references, correlation/trace fields, and lifecycle/audit references.

Session records use references to raw channel data, runtime state, prompts, recordings, attachments, and external work. They do not duplicate restricted content or credentials.

## Session Types

| Type | Examples |
|---|---|
| Interactive | Voice call, web chat, authenticated app chat, live API stream |
| Asynchronous | Email response window, messaging exchange, deferred follow-up |
| Agent execution | Bounded coordination for an authorized agent invocation |
| Human handoff | Operator assignment or collaborative review window |
| Workflow continuation | Controlled wait/resume relationship to a business process |
| Event-triggered | Approved event response associated with a conversation or independent purpose |

---

# Session States and Lifecycle

~~~text
Created
    -> Authorized
    -> Active
    -> Waiting
    -> Handed Off
    -> Completed / Cancelled / Expired
    -> Retained for Audit
~~~

| State | Meaning |
|---|---|
| Created | Session record exists but no active processing is permitted |
| Authorized | Required identity, tenant, purpose, policy, and context references are valid |
| Active | An approved channel, agent, human, or workflow interaction is in progress |
| Waiting | Session waits for participant, workflow, handoff, approved external outcome, or reconnect |
| Handed Off | An authorized human/queue or collaboration mode owns the next step |
| Completed | Controlled session purpose reached terminal outcome |
| Cancelled | Session ended by participant, policy, conversation transition, or authorized operator |
| Expired | Time or inactivity bound passed; resume requires new authorization |
| Retained | Historical session metadata remains subject to retention and access policy |

Session transition authority follows the Conversation Lifecycle and Routing/Handoff policies. A session cannot become Active unless its parent conversation is eligible and current authorization succeeds.

---

# Creation, Resolution, and Continuity

## Session Creation

A validated interaction, approved routing decision, human handoff, workflow continuation, or authorized event creates a session. Creation uses idempotency keys and tenant/channel/participant evidence to prevent duplicate active sessions.

## Channel Switching

Channel switching creates or associates a target session with the same conversation only after target channel eligibility, participant evidence, consent, classification, and policy pass. The source session is completed, waiting, or handed off according to the continuity policy.

The platform transfers only an authorized context reference. It does not copy restricted content, assume that contact details prove identity, or carry expired authority to the target session.

## Reconnect and Resume

A reconnect or delayed interaction does not revive an expired or completed session automatically. The resolver evaluates whether to continue an eligible session, create a new session under the same conversation, or create a new conversation.

## Multi-Participant Sessions

A session may include multiple participant associations only under an explicit visibility and role policy. Participant presence, join/leave, speaking/interaction role, and authorized context are recorded separately from canonical participant identity.

## Device and Browser Transfer

Web/app session transfer, reconnect from another device, logout, device loss, or shared-device use follows a verified transfer and revocation policy. The target session must establish its own trusted identity and tenant/channel binding; it does not inherit browser state, context, or authority merely from a copied URL, identifier, or client storage value.

The source session is revoked, completed, or placed in a controlled handoff state according to policy. Sensitive conversation access may require step-up verification before transfer or resume.

---

# Agent, Workflow, and Handoff Association

## Agent Execution Association

Conversation Platform requests an agent execution through an authorized bounded context reference. The Agent Platform resolves version, reasoning, tools, and controlled actions. The session records only execution references, outcome, and allowed lifecycle effect.

An in-flight agent execution is pinned to its session/conversation context. A new session or resumed session creates a new execution authorization rather than reusing stale runtime state.

## Workflow Association

A session may wait on or correlate with workflow work. Workflow state remains owned by its implementation platform. When workflow work resumes, the Conversation Platform creates or authorizes the appropriate session and rechecks current policy before delivering any outcome.

## Handoff Association

Human handoff creates a governed session/assignment relationship with queue, role, visibility, ownership, and return conditions. Human completion, escalation, or return is recorded as a session outcome and may trigger controlled routing.

---

# Concurrency, Expiry, and Recovery

## Concurrency

A session uses an expected version and active-ownership token or equivalent coordination control. Concurrent channel input, agent result, human action, workflow callback, or provider reconnect validates current session and conversation state before it changes ownership or outcome.

The platform avoids last-write-wins behavior. Conflicting inputs are ordered/reconciled using source evidence, lifecycle, authority, policy, and durable state.

## Session Concurrency and Turn Ownership

Tenant policy defines maximum active, waiting, reconnecting, and handed-off sessions by conversation, participant, channel, agent, queue, and tenant capacity. Limit breaches create an explicit routing, deferment, handoff, or safe refusal outcome; they do not silently replace another active session.

The turn-ownership matrix defines whether an agent, human, workflow, participant, or collaboration mode may produce the next response. Human-exclusive handoff, approval wait, safety hold, and active agent response are mutually governed states. A concurrent result that loses turn ownership is recorded, reconciled, or discarded safely rather than delivered twice.

## Expiry and Inactivity

Expiry is set by session type, channel, risk, classification, tenant policy, and business purpose. Waiting and handoff sessions record owner, expiry, reminder/follow-up behavior, and safe terminal disposition.

Expiry revokes ordinary active use; it does not delete the conversation or historical audit record.

## Session Outcome Taxonomy

Every terminal session records an approved outcome category: completed, participant-ended, participant-abandoned, channel-disconnected, agent-completed, agent-failed, handed-off, policy-blocked, security-suspended, delivery-failed, workflow-pending, cancelled, or expired.

Outcome category is distinct from business outcome and delivery confirmation. It is used for routing, observability, analytics, recovery, and participant communication under current policy.

## Recovery

After restart, failover, or provider interruption, the platform restores only durable session references and state. It revalidates parent conversation eligibility, tenant, policy, identity, consent, authorization, dependency health, and idempotency before resuming.

## Session Migration

When session state, schema, identifier, expiry, or policy behavior changes, the Conversation Platform maintains a migration plan for active and retained sessions. The plan identifies compatibility, affected session types, rollout, revalidation, fallback, audit, rollback, and expiry behavior.

An active session is not silently reinterpreted under a materially different policy. Where compatibility is not safe, the session is completed, cancelled, or reauthorized through a new session.

---

# Security, Privacy, and Tenant Controls

Session IDs are unguessable, scoped, and protected against fixation, replay, substitution, and disclosure. Provider/browser identifiers are mappings, not access tokens. A session cannot cross tenant boundaries or be reassigned through user-controlled input.

Session context, participant presence, handoff, and external references are classified and access-controlled. Operators, agents, channels, and workflows receive only the minimum authorized data. Ending, expiring, or suspending a session revokes or expires derived context references as policy requires.

## Session Token Boundary

Conversation session IDs are coordination identifiers, not browser cookies, OAuth tokens, API keys, provider credentials, or bearer authorization tokens. Channel/browser authentication tokens and provider credentials are owned by Security and Channel Platforms and are validated before any mapping to a Conversation Platform session.

The session model records only approved identity/authorization references and expiry. It never stores reusable secrets or treats a client-held session identifier as sufficient proof of identity or permission.

---

# Observability and Audit

The platform records session creation, authorization, activation, channel association, participant join/leave, context reference, agent/workflow/handoff correlation, waiting, expiry, cancellation, completion, recovery, and conflict outcome.

Metrics include active-session count, creation/authorization latency, reconnect/resume success, expiry, duplicate prevention, channel-switch completion, handoff duration, agent-execution association, conflict, recovery, and unauthorized session attempt.

---

# Testing Strategy

## Contract Tests

Validate session schema, identifier, type, state, parent/tenant relationship, authorization/context reference, expiry, transition, and audit fields.

## Integration Tests

Validate channel creation, reconnect, switching, agent execution, workflow continuation, human handoff, participant join/leave, closure, cancellation, and recovery.

## Security and Tenant Tests

Validate fixation, replay, guessing, cross-tenant mapping, expired session, revoked consent, unauthorized context, operator access, and provider identifier misuse.

## Resilience Tests

Simulate duplicate channel callbacks, concurrent agent/human actions, worker restart, provider reconnect, delayed workflow result, expiry, conversation suspension, handoff failure, and reconciliation. Prove no duplicate active session, stale authority, or context leak.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation session schema | Defines type, parent, state, mapping, expiry, authorization, and correlation | Conversation Platform |
| Session transition and expiry policy | Defines guards, authority, duration, inactivity, cancellation, and retention | Conversation Platform with Security and tenant owners |
| Session concurrency and turn-ownership matrix | Defines limits, active response owner, collision, queue, and safe outcome behavior | Conversation Platform with Agent, Channel, and Operations owners |
| Session continuity and channel-switch contract | Defines target validation, context transfer, source/target disposition, and audit | Conversation Platform with Channel and Agent owners |
| Device transfer and revocation policy | Defines verification, source/target handling, logout, shared-device, step-up, and audit behavior | Conversation Platform with Security and Channel owners |
| Session-token boundary standard | Defines session ID, authentication-token, credential, reference, and prohibited-storage rules | Conversation Platform with Security owner |
| Session concurrency and recovery procedure | Defines ownership token, conflict, restart, resume, and reconciliation behavior | Conversation Platform with Data and Operations owners |
| Session outcome taxonomy | Defines terminal categories, business/delivery distinction, routing, analytics, and communication use | Conversation Platform with Operations and Analytics owners |
| Session migration policy | Defines active/retained session compatibility, rollout, reauthorization, fallback, audit, and rollback | Conversation Platform with Data and Security owners |
| Session security test suite | Validates fixation, tenant, context, authorization, expiry, and recovery controls | Conversation Platform and Testing Platform |
| Session observability catalog | Defines signals, metrics, audit, SLOs, and diagnostic references | Conversation, Operations, and Observability owners |

---

# Anti-Patterns

## Provider Session Is Canonical

A call SID, browser tab, or provider thread cannot replace a tenant-safe canonical session and conversation model.

## Expired Session Resumes Automatically

Resuming stale context or authority after expiry can expose data or repeat action. Resolve and authorize a new eligible session.

## Session as Permission Token

A session reference proves coordination identity, not permission to read data, use a tool, deliver a message, or act for a participant.

## Runtime Worker Owns Continuity

Keeping session truth only in a worker or model context loses recoverability and causes inconsistent behavior on scaling or restart.

## Channel Switch Copies Everything

Only minimal authorized context transfers. Do not copy raw history, restricted content, or authority into another channel session.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation Platform components and boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines conversation state that gates session behavior. |
| 03_CONVERSATION_MODEL.md | Defines session parent, participant, interaction, and mapping entities. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines bounded context content and snapshots. |
| 06_CONVERSATION_ROUTING.md | Defines session destination and eligibility. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines human assignment and collaboration behavior. |
| 09_CONVERSATION_STATE_MANAGEMENT.md | Defines durable state, concurrency, and recovery patterns. |
| 10_CONVERSATION_SECURITY.md | Defines detailed identity, consent, access, and privacy controls. |
| 02_AGENT_PLATFORM/07_AGENT_RUNTIME_ARCHITECTURE.md | Owns runtime worker and agent execution lifecycle. |
| 02_AGENT_PLATFORM/23_AGENT_SESSION_MANAGEMENT.md | Defines Agent Platform integration boundary; canonical session ownership belongs here. |
| 04_VOICE_PLATFORM | Owns voice/provider session and media behavior. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Session Model document. |
| 2.1 | 2026-08-05 | Added concurrency/turn ownership, device transfer, token boundary, outcomes, migration, capacity, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

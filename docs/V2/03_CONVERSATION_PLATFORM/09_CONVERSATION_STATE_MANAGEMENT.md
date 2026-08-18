# 09_CONVERSATION_STATE_MANAGEMENT

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform maintains authoritative, tenant-scoped conversation state while many channels, participants, agents, workflows, human operators, and asynchronous events interact with the same conversation.

Conversation state is the durable current representation of a canonical conversation and its controlled transition history. It prevents a provider thread, browser session, agent runtime, event consumer, cache, transcript, or human workspace from becoming an independent source of truth.

---

# Purpose

The Conversation State Management Model provides correctness rules for reading, changing, reconstructing, and reconciling canonical conversation state.

It ensures that state changes are intentional, authorized, versioned, auditable, tenant-safe, resilient to concurrency and failure, and understandable long after the original request or channel session has ended.

---

# Objectives

The Conversation State Management Model must:

- Establish the Conversation Platform as the sole canonical owner of conversation state.
- Define the state aggregate, state categories, invariants, transition controls, versions, and history.
- Support safe concurrent activity from multiple channels, participants, services, and operational actors.
- Prevent duplicate, stale, out-of-order, cross-tenant, and unauthorized updates from changing canonical state.
- Preserve causal evidence and reconstruction capability without treating events or projections as mutable truth.
- Provide controlled conflict detection, recovery, repair, and reconciliation.
- Protect classification, consent, participant visibility, retention, residency, and authorization boundaries.
- Publish durable facts only after the corresponding state change is recorded.

---

# Scope

This document defines canonical state ownership, aggregate boundaries, state categories, mutation, concurrency, history, reads/projections, integrity, recovery, reconciliation, security, observability, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Conversation lifecycle states and business transition eligibility | 02_CONVERSATION_LIFECYCLE.md |
| Session state, execution runtime state, or agent execution lifecycle | 04_CONVERSATION_SESSION_MODEL.md and 02_AGENT_PLATFORM |
| Routing decision policy, destination ranking, or capacity selection | 06_CONVERSATION_ROUTING.md |
| Handoff collaboration, acceptance, or transfer rules | 08_CONVERSATION_HANDOFF_MODEL.md |
| Context composition, snapshot contents, or context authorization | 05_CONVERSATION_CONTEXT_MODEL.md |
| Interaction content storage, transcript, recording, attachment, or vector-storage implementation | 08_DATA_PLATFORM and relevant Channel Platforms |
| Broker, database engine, cache, queue, replication, backup, or deployment implementation | 07_INTEGRATION_PLATFORM, 08_DATA_PLATFORM, and 12_DEPLOYMENT_PLATFORM |
| Enterprise identity, authorization, key management, retention policy, and compliance infrastructure | 09_SECURITY_PLATFORM |
| Analytics warehouse, dashboard, logging, tracing, alerting, or incident-process implementation | Data, Observability, and Operations Platforms |

---

# State Ownership Principles

## One Canonical Owner

Conversation Platform owns canonical conversation state and durable transition history. Adjacent platforms may own their own state and submit controlled requests or facts, but they do not directly mutate Conversation state.

## State Is Not Content

State records the minimum durable facts required to coordinate a conversation: lifecycle, participant associations, channel mappings, current work and response ownership, routing/handoff references, authorized context references, policy/consent/classification references, and integrity metadata.

A raw transcript, recording, attachment, agent prompt, model reasoning trace, memory item, external ticket, provider payload, or cache entry is not canonical conversation state. State holds governed references where needed.

## Current State and History Work Together

The current state supports safe decisions now. Immutable transition history explains how it reached that state. Neither a mutable projection nor an event stream alone replaces the other without controlled reconstruction and validation.

## Controlled Mutation

Every state mutation is requested through a Conversation Platform command or governed internal transition. The request identifies actor/service, purpose, tenant/environment, target aggregate, expected version, authorized operation, correlation/causation, idempotency, and supporting evidence.

---

# Canonical State Aggregate

~~~text
Conversation State Aggregate
    +-- identity and tenant/environment scope
    +-- lifecycle and effective-status references
    +-- aggregate version and integrity metadata
    +-- participant associations and visibility references
    +-- interaction and approved channel-thread mappings
    +-- current response/work owner and waiting-state reference
    +-- routing and handoff references
    +-- session and authorized context references
    +-- classification, consent, retention, residency, and policy references
    +-- transition history and reconciliation status references
~~~

The aggregate is scoped to one canonical conversation. A participant, channel identifier, agent execution, workflow instance, ticket, or provider thread can relate to it, but cannot become its parent aggregate or independently decide its version.

## State Categories

| Category | Examples | Rule |
|---|---|---|
| Identity and scope | conversation ID, tenant, environment, organization reference | Immutable after creation except controlled migration with explicit audit. |
| Lifecycle | created, active, waiting, handed off, suspended, closed, archived | Governed by the Lifecycle Model. |
| Participants and visibility | participant association, role, verification/visibility reference | Changes require participant and policy checks. |
| Interaction continuity | normalized interaction references, channel-thread mapping | Provider identifiers are mapped; they are not canonical IDs. |
| Ownership and work | current owner, work segment, turn authority, waiting reference | Exactly one active owner or an approved safe waiting state per work segment. |
| Routing and handoff | decision, queue, offer, active handoff, return reference | Changes use Routing and Handoff contracts. |
| Context and session | authorized snapshot and execution-session references | References never grant continuing access by themselves. |
| Governance | classification, consent, retention, residency, policy references | Current policy is evaluated for every protected operation. |
| Integrity and recovery | version, transition digest, conflict, reconciliation, repair references | Managed only through controlled state operations. |

---

# State Invariants

- A state record belongs to exactly one authoritative tenant and environment.
- Conversation ID, creation authority, and tenant/environment scope are immutable under ordinary operation.
- Every state-changing operation has an authenticated actor/service, purpose, authorization decision, correlation, causation where applicable, and idempotency reference.
- Every accepted mutation advances the aggregate version exactly once and records immutable transition evidence.
- A work segment has one active response owner or one explicitly recorded safe waiting state.
- A handoff, routing decision, session, context snapshot, channel mapping, or external reference does not expand access or override current policy by itself.
- Closed, archived, suspended, retention-restricted, or legally held conversations accept only transitions allowed by the Lifecycle, Security, and Data policies.
- A projection, cache, event, channel/provider signal, or consumer database cannot overwrite canonical state directly.
- A repair is a new audited state operation; historical evidence is not silently rewritten.

---

# Aggregate Compatibility

The Conversation state aggregate is a versioned contract. Additive optional fields and references are preferred. Removing a field, changing its meaning or type, changing an invariant, or making an optional field required requires a new aggregate-contract version and documented migration, projection-rebuild, and consumer-compatibility plan.

A state transition records the aggregate-contract version used to evaluate it where the version is material to reconstruction, recovery, or audit. A derived view must declare which aggregate-contract versions it supports and must fail safely or be rebuilt when it cannot interpret an authoritative version.

---

# State Mutation Model

## Mutation Flow

~~~text
Controlled Request or Validated External Fact
    |
    v
Identity, Tenant, Purpose, and Authorization Checks
    |
    v
Current Aggregate Read and Expected-Version Check
    |
    v
Lifecycle, Ownership, Policy, and Domain Guard Evaluation
    |
    v
Durable State Transition and History Record
    |
    v
Outbox / Governed Conversation Event Publication
    |
    v
Projection, Cache, and Authorized Consumer Update
~~~

## Commands and Facts

A command asks Conversation Platform to evaluate and perform a state operation. A validated external fact supplies evidence that may allow a command or transition; it is never assumed to be authoritative state merely because it arrived from a channel, provider, agent, or event consumer.

Each accepted transition stores operation type, before/after version, effective and recorded times, actor/service identity, authorization/policy references, reason, evidence references, correlation, causation, idempotency, and resulting event reference.

## Idempotency

The same logical request must use a stable idempotency reference. Repeated delivery returns the original accepted outcome or a safe current-status result; it must not create a duplicate interaction mapping, route, handoff, owner change, notification, or external side effect.

---

# Concurrency and Ordering

## Optimistic Concurrency

State mutations provide the aggregate version they were evaluated against. If the version is stale, the platform rejects, re-evaluates, or serializes the request according to the operation's policy. It must not silently apply a stale update over a newer transition.

## Work-Segment and Turn Authority

Concurrent conversation activity is allowed only when it does not create conflicting participant-facing work. The state records the work-segment or response-turn reference and active owner. A second agent, workflow, human, or channel action must be rejected, deferred, coordinated, or explicitly authorized as collaboration.

## Event and Channel Ordering

Global ordering is not assumed. A delayed or duplicate provider/event input is evaluated using canonical aggregate version, normalized occurrence/recorded time, source provenance, idempotency, lifecycle state, and operation-specific ordering rules.

A late interaction may be recorded as evidence where policy permits, but it cannot silently reopen, change ownership, undo a handoff, or override a later canonical decision.

## Multi-Participant Changes

Participant joins, removals, visibility changes, identity verification, and shared-channel activity are independent controlled transitions. A participant-level change is not permission to alter another participant's visibility, content access, or active ownership.

---

# Read Model, Projections, and Caches

## Authoritative Read

A decision that changes conversation state, accesses protected conversation data, or sends participant-facing communication obtains the current authoritative state or a validated versioned view. It rechecks current authorization and policy.

## Read-Consistency Levels

| Level | Suitable use | Requirement |
|---|---|---|
| Authoritative | State mutation, protected-data access, participant-facing delivery, ownership change, handoff, routing, or recovery decision. | Read the current canonical state or a validated versioned view and re-evaluate current policy. |
| Version-validated | Coordinated internal work that can proceed only if the aggregate has not advanced beyond a known version. | Supply or compare aggregate version; re-read or stop if stale. |
| Derived | Queue display, dashboard, search, non-binding notification preview, or analytics. | Display source version and freshness; never use as the sole authority for a protected or participant-impacting action. |

## Derived Views

Channel views, operator workspaces, agent inputs, queues, search indexes, dashboards, analytics records, and caches are derived views. They carry source aggregate version and freshness metadata, have a defined rebuild path, and cannot directly write back to canonical state.

## Staleness and Invalidation

A consumer must tolerate delayed projection updates. Where freshness is material, it requests the authoritative version or waits for controlled refresh. State change events and policy/consent changes invalidate affected derived views according to their registered scope.

---

# History, Evidence, and Reconstruction

## Transition History

Each transition records enough metadata to establish who changed what, why, under which policy, from which version, and with what outcome. History references protected content rather than embedding broad payloads.

History is append-only from the domain perspective. Corrections, redactions, access changes, retention effects, and repairs are later governed facts that preserve the original audit narrative only to the extent policy permits.

## Reconstruction

The platform can reconstruct a state from an approved durable state record and transition history, then validate aggregate version, invariants, tenant scope, policy references, and reconciliation status. Rebuilding a projection does not create a new state transition.

Reconstruction does not restore deleted, redacted, unavailable, or currently unauthorized content. Historical references resolve according to current consent, retention, legal-hold, residency, and authorization controls.

---

# Conflict, Recovery, and Reconciliation

## Conflict Categories

| Category | Example | Required response |
|---|---|---|
| Stale mutation | A human accepts an offer after it was reassigned. | Reject or re-evaluate against current state. |
| Duplicate input | A provider retries the same inbound interaction. | Return prior outcome or safely ignore after idempotency check. |
| Out-of-order fact | Delivery confirmation arrives after closure. | Record/reconcile only if policy permits; do not reverse later state. |
| Competing ownership | Agent and human both attempt the next response. | Preserve turn authority; defer, reject, or require supervisor coordination. |
| External uncertainty | Provider outcome cannot be confirmed. | Mark uncertain/reconciliation-required; avoid blind retry. |
| Integrity mismatch | Projection differs from aggregate or history. | Quarantine derived view, rebuild, and audit the discrepancy. |
| Tenant or policy mismatch | Input references a different tenant or no longer permitted data. | Reject/quarantine, alert where required, and preserve restricted evidence. |

## Reconciliation Procedure

A reconciliation case identifies the affected conversation, version range, suspected source, tenant/classification, external effect risk, owner, evidence, and required deadline.

The Conversation Platform compares authoritative state and transition history with controlled channel, provider, agent, workflow, or operational evidence. Resolution is one of: confirm state, issue a compensating transition, repair a derived view, safely retry a pending operation, preserve unresolved uncertainty, or escalate for authorized review.

A reconciliation never directly edits away history, bypasses current authorization, or repeats an external action without idempotency and side-effect checks.

## Reconciliation Authority and Escalation

Automated reconciliation may rebuild a derived view, suppress a duplicate, verify an idempotent outcome, or safely retry a registered non-external operation. It may not alter canonical ownership, lifecycle, participant visibility, consent, classification, or an uncertain external side effect without the applicable controlled transition.

Conversation operations review handles ordinary state conflicts and assigns the reconciliation case owner. Security review is required for suspected tenant, authorization, privacy, consent, classification, or integrity breach. A designated authorized human approver is required for exceptional repair, aggregate merge/split, tenant/environment migration, or a compensating transition with material participant or external-business impact. The registry records escalation criteria, accountable role, target response time, and closure evidence.

## Repair and Migration

A repair is an explicit, authorized, versioned operation with reason, approver where required, before/after evidence, correlation, and audit record. Tenant/environment migration or aggregate merge/split is exceptional and requires a dedicated approved migration procedure; it cannot be performed as an ordinary update.

---

# Security, Privacy, and Tenant Isolation

All reads, mutations, reconstruction, replay, repair, and operational inspection are scoped by current tenant, environment, identity, role, purpose, classification, consent, residency, retention, legal hold, and authorization decision.

State carries references to governance decisions rather than secrets or unrestricted personal content. Logging, metrics, traces, and reconciliation queues use minimum identifiers and protected references. Cross-tenant lookup, derived-view sharing, and repair are denied by default.

## Data-Lifecycle Effects

Deletion, anonymization, consent withdrawal, retention expiry, legal hold, residency restriction, and approved tenant migration are governed by the Data and Security Platforms. Conversation State Management records their authorized lifecycle effect and applies it to state references, read eligibility, projections, caches, event replay, reconstruction, and reconciliation.

A derived view must be invalidated, rebuilt, restricted, redacted, or removed as the governing lifecycle decision requires. Legal hold prevents destruction or alteration only within its approved scope; it does not restore ordinary access. A migration preserves source/destination evidence, authorization, version mapping, and audit correlation, and is never performed as a routine state update.

---

# Events and External Integration

Conversation events are published only after durable canonical state and history recording. 07_CONVERSATION_EVENTS.md owns the event taxonomy, envelope, schema, and consumer safeguards.

An external system, agent, channel, workflow, or event consumer requests a controlled state operation through the Conversation Platform. It may not use receipt of an event, a provider callback, or its local projection as authority to update conversation state directly.

---

# Observability and Audit

Telemetry records aggregate ID/version, operation type, actor/service category, state/guard result, idempotency result, conflict category, stale-version rate, transition latency, projection freshness, reconciliation status, repair, tenant/classification, and correlation/trace references.

Operational measures include mutation success/failure, version conflicts, duplicate suppression, out-of-order input, contention, owner ambiguity prevention, projection lag, cache invalidation, reconstruction success, reconciliation backlog/age, repair count, and unresolved external outcomes. Raw transcripts, recordings, attachments, secrets, and private reasoning are excluded from routine telemetry.

---

# Testing Strategy

## Contract Tests

Validate state aggregate fields, invariant enforcement, command/fact distinctions, expected-version behavior, transition history, idempotency, event ordering, policy references, and compatibility.

## Concurrency and Integration Tests

Simulate parallel channel input, agent execution, workflow completion, human handoff, participant changes, routing expiry, queue acceptance, projection lag, cache rebuild, event retry, restart, and late provider callbacks.

## Security and Recovery Tests

Simulate cross-tenant request, stale authorization, consent withdrawal, restricted state read, forged provider fact, duplicate mutation, out-of-order transition, uncertain external outcome, corrupted projection, history/state mismatch, failed publication, replay, repair, and legal hold. Prove canonical state remains coherent and no test leaks protected data or creates duplicate participant-facing work.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Conversation state aggregate contract | Defines canonical fields, references, state categories, versions, and invariants | Conversation Platform |
| Transition and command registry | Defines allowed operations, guards, actors, evidence, idempotency, and event mapping | Conversation Platform with Lifecycle owner |
| Concurrency and turn-ownership policy | Defines expected-version, work-segment, collaboration, stale-update, and ordering behavior | Conversation Platform with Routing and Handoff owners |
| Projection and cache contract | Defines derived-view provenance, freshness, invalidation, rebuild, and write-prohibition rules | Conversation Platform with Data and Observability owners |
| Reconciliation and repair procedure | Defines conflict classification, ownership, evidence, escalation, safe retry, repair, and audit | Conversation Platform with Operations and Security owners |
| State integrity test suite | Validates contract, concurrency, security, recovery, reconstruction, and migration scenarios | Conversation Platform with Testing Platform |

---

# Anti-Patterns

## Channel Thread as the Conversation Record

A provider thread, call ID, or browser session may map to a conversation but cannot replace canonical state or decide its lifecycle.

## Consumer Updates the Aggregate

A queue, CRM, agent runtime, dashboard, cache, or event consumer must request a controlled transition rather than writing state directly.

## Last Writer Wins

Silently accepting a stale update can undo ownership, consent, lifecycle, or handoff decisions. Use expected version and operation-specific reconciliation.

## Cache Is Treated as Current Authorization

A cached view is not proof of present consent, identity, classification, ownership, or permission. Material actions revalidate current state and policy.

## History Is Rewritten to Hide a Mistake

Corrections and redactions are governed later facts. Silent rewrite destroys auditability and recovery evidence.

## Replay Repeats External Action

Reconstruction and replay must not resend a message, repeat a tool action, or alter a later decision without side-effect and current-state controls.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Conversation State Service and platform ownership. |
| 02_CONVERSATION_LIFECYCLE.md | Defines business lifecycle states and transition eligibility. |
| 03_CONVERSATION_MODEL.md | Defines canonical entities and references represented in state. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines bounded session continuity and runtime links. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines authorized context snapshots and lifecycle. |
| 06_CONVERSATION_ROUTING.md | Defines destination selection and turn-routing policy. |
| 07_CONVERSATION_EVENTS.md | Defines event publication and consumption contracts. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines transfer, acceptance, collaboration, and return behavior. |
| 02_AGENT_PLATFORM | Defines agent execution and controlled requests to Conversation state. |
| 08_DATA_PLATFORM | Defines storage, lifecycle, backup, and data implementation. |
| 09_SECURITY_PLATFORM | Defines enterprise authorization, compliance, and governance controls. |
| 13_OBSERVABILITY_PLATFORM | Defines shared telemetry infrastructure and operations integration. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-06 | Initial Conversation State Management document. |
| 2.1 | 2026-08-06 | Added aggregate compatibility, read-consistency levels, reconciliation authority, and data-lifecycle effects. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

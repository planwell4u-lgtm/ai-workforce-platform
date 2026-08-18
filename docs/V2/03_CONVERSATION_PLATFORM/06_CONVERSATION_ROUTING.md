# 06_CONVERSATION_ROUTING

**Version:** 2.4  
**Status:** Approved  
**Owner:** Conversation Platform Owner  
**Phase:** Conversation Platform

---

# Overview

This document defines how the Conversation Platform routes a validated interaction to an eligible agent, human queue, workflow boundary, verification path, safe fallback, or deferment outcome.

Routing coordinates who handles the next conversation turn. It does not perform agent reasoning, authorize tools, execute workflows, deliver messages, or override tenant/security controls.

---

# Purpose

The purpose of Conversation Routing is to make assignment decisions deterministic, explainable, tenant-safe, and resilient across channels, participants, agents, human operators, and operational conditions.

It ensures that the right eligible destination receives the minimum authorized context while preventing ambiguous, unavailable, unauthorized, or overloaded destinations from silently handling an interaction.

---

# Objectives

The Conversation Routing Model must:

- Route only validated, tenant-scoped, policy-eligible interactions.
- Apply deterministic precedence for security, consent, lifecycle, identity, channel, capability, queue, capacity, and fallback conditions.
- Support agent, human, workflow, verification, deferment, and safe-refusal destinations.
- Preserve One Brain, Multi-Channel by selecting a centrally governed agent assignment rather than channel-specific intelligence.
- Bind routing decisions to conversation/session, purpose, classification, policy, expiry, and audit references.
- Avoid duplicate routing, split ownership, stale assignment, and unbounded queueing.
- Re-evaluate eligibility when conversation state, policy, tenant, consent, dependency, or capacity changes.
- Remain independent of a specific queue, workflow engine, model, provider, or scheduling implementation.

---

# Scope

This document defines routing inputs, destinations, precedence, decision records, eligibility, assignment, fallback, capacity, re-routing, security, observability, testing, and required artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent purpose, reasoning, version resolution, capabilities, tool use, and model behavior | 02_AGENT_PLATFORM |
| Human handoff collaboration, queue work details, transfer, and return behavior | 08_CONVERSATION_HANDOFF_MODEL.md |
| Conversation lifecycle, session, context, and canonical data entities | 02–05 Conversation Platform documents |
| Workflow implementation, business process state, tools, connectors, and external actions | 07_INTEGRATION_PLATFORM |
| Channel transport, provider routing, phone routing, media routing, and delivery implementation | Voice and relevant Channel Platforms |
| Identity, permission, consent, tenant, compliance, and security policy implementation | 09_SECURITY_PLATFORM |
| Queue infrastructure, autoscaling, job scheduling, and incident operations | Operations, Deployment, and Engineering Platforms |

---

# Routing Principles

## Route Eligibility, Not Intelligence

Routing selects an eligible destination category and assignment. The Agent Platform resolves the approved agent version and reasons within its own permission and safety boundaries.

## Policy Before Preference

Tenant, legal, classification, security, consent, identity assurance, lifecycle, and required approval restrictions take precedence over convenience, user preference, load balancing, or channel affinity.

## One Active Response Owner

For each response turn, routing establishes one active owner: eligible agent, human/queue, workflow boundary, or controlled deferment. Shared collaboration is explicit; competing destinations cannot independently deliver conflicting responses.

## Explainable and Expiring

Every decision records inputs, policy, destination, reason, alternative disposition, owner, time, expiry, and correlation. A decision expires when relevant state, policy, capacity, session, or participant conditions change.

## Safe Fallback

No eligible destination results in an approved safe fallback, verification path, deferment, or human escalation. It does not result in unapproved channel delivery, arbitrary agent selection, or silent message loss.

---

# Routing Model

~~~text
Validated Interaction
    |
    v
Tenant, Lifecycle, Identity, Consent, Classification Check
    |
    v
Channel, Session, Context, and Policy Eligibility
    |
    v
Destination Selection
    +--> Eligible Agent Assignment
    +--> Human Queue / Handoff
    +--> Workflow Boundary
    +--> Verification / Approval
    +--> Defer / Safe Fallback / Refusal
    |
    v
Routing Decision and Turn Ownership
    |
    v
Authorized Destination Request
~~~

---

# Routing Inputs

A routing request includes tenant, conversation/session, interaction, participant, channel, purpose, classification, lifecycle, identity assurance, consent, current handoff/turn state, agent assignment eligibility, queue/workflow availability, dependency health, capacity/quota, policy/approval references, and correlation.

Missing, conflicting, stale, or unauthorized inputs produce a controlled deny, verification, deferment, or human-review outcome.

---

# Destination Types

| Destination | Use |
|---|---|
| Agent assignment | An eligible governed agent can process the interaction |
| Human queue | A qualified human role/queue is required or preferred by policy |
| Workflow boundary | An approved business-process continuation or request is required |
| Verification/approval | Identity, consent, permission, information, or human approval is required first |
| Deferred work | Work is durable but cannot safely complete now |
| Safe fallback/refusal | No eligible action; provide permitted limited response or notice |

A destination type does not imply permission to access all conversation data, execute a tool, alter workflow state, or deliver a message. The receiving platform performs its own authorization.

---

# Decision Precedence

1. Tenant/environment, legal, regulatory, security, classification, and suspension restrictions.
2. Conversation lifecycle, participant visibility, identity assurance, consent, and purpose checks.
3. Mandatory safety, approval, verification, or human-review conditions.
4. Active handoff, response-turn ownership, workflow wait, or unresolved-action constraints.
5. Channel capability, language/accessibility, delivery eligibility, and provider/operational health.
6. Eligible agent assignment, human role/queue, or workflow boundary matching purpose and risk.
7. Capacity, quota, fairness, priority, affinity, and preference within the eligible set.
8. Approved fallback, deferment, or safe refusal when no destination remains.

A lower level cannot override an earlier restriction. The decision records applicable policy and the final disposition.

---

# Agent Assignment

Agent assignment is based on tenant-approved agent purpose, deployment eligibility, channel scope, risk/autonomy, capability profile, availability, current conversation/handoff state, and policy.

Routing does not select a version, provide broad context, or assume an agent can execute an external action. It issues a bounded assignment request; Agent Platform resolves version, context use, permissions, tools, and outcome.

A channel never receives a special agent brain solely because of its provider. Any channel adaptation occurs after the shared Agent Brain produces an approved outcome.

## Routing Policy Lifecycle and Simulation

Routing policies are versioned and progress through draft, validation, approval, activation, migration, rollback, deprecation, and retirement. A policy change that affects tenant scope, destination eligibility, priority, fairness, fallback, queue behavior, channel, data classification, or human/agent assignment requires the applicable review and controlled rollout.

Before activation, an approved simulation or dry-run evaluates the candidate policy against representative synthetic or authorized scenarios. Simulation records candidate destinations, precedence, capacity/health assumptions, fallback, fairness indicators, and expected user impact; it does not send work, mutate conversations, or authorize delivery.

---

# Human Queue and Handoff Routing

Human routing considers required role, tenant, language, skills, classification access, queue availability, priority, SLA, participant preference where allowed, and existing handoff ownership.

Queue assignment is a governed work reference. It does not disclose full history until the handoff model grants authorized context. If no qualified human destination is available, the routing policy specifies wait, safe notice, escalation, or fallback behavior.

---

# Workflow and Verification Routing

A workflow boundary is selected only when policy permits the relevant business process. Workflow implementation, state, tools, and compensation remain owned by Integration Platform.

Verification/approval routing creates an explicit controlled step when identity, consent, permission, missing information, high-risk action, or human review is required. It cannot be bypassed by a later channel message or agent retry.

---

# Capacity, Priority, and Fairness

Routing applies tenant quota, destination capacity, queue limits, channel SLA, risk priority, user impact, and fairness policy after required eligibility checks. It prevents one tenant, conversation, retry, or low-value workload from starving critical or safety-sensitive work.

Capacity exhaustion produces a bounded waiting, deferment, fallback, or escalation outcome with observable reason and owner. It does not silently discard accepted interactions or reroute them to an unqualified destination.

## Destination Health Contract

Every destination publishes approved availability, capacity, eligibility, health, freshness, failure, maintenance, and withdrawal state. Routing accepts health only within its defined freshness window; stale or unknown health is treated as unavailable or constrained according to risk policy.

Destination health does not expose private operational data to a tenant or user. It provides only the information necessary to route safely and explain an approved disposition.

## Routing Fallback and No-Route Policy

The fallback matrix defines permitted outcomes by tenant, channel, risk, classification, consent, participant preference, queue/destination condition, and failure type. It specifies whether to wait, defer, verify, hand off, offer an approved alternative channel, provide limited safe information, or refuse.

No-route policy defines queue-wait thresholds, participant notification timing, escalation owner, abandonment handling, durable work creation, review interval, and closure/deferment conditions. It never defaults restricted content to a less secure channel or unqualified destination.

## Routing Fairness

Routing policy is tested for materially different access, wait, fallback, handoff, or failure outcomes across approved dimensions such as tenant tier, language, channel, accessibility requirement, workload type, region, and time. Differences that are required by policy or capability are documented; unexplained harmful disparity triggers review and remediation.

---

# Re-Routing and Turn Ownership

A routing decision is re-evaluated on session expiry, conversation lifecycle transition, participant/identity/consent change, handoff outcome, policy update, agent deployment withdrawal, queue state, dependency failure, capacity change, or explicit authorized reassignment.

Re-routing cancels, supersedes, or safely completes the prior turn ownership before assigning a new owner. In-flight work is reconciled according to session/lifecycle/failure policy; the platform avoids duplicate delivery or external action.

---

# Security, Privacy, and Tenant Controls

Routing is tenant-scoped, purpose-bound, classified, authorized, and audited. A route cannot cross tenant boundaries, use a mismatched channel/integration account, or reveal context beyond the destination’s role and current authorization.

Destination lookup uses approved metadata and references. Routing logs and queue labels avoid secrets, raw restricted content, hidden instructions, or private reasoning. Operator and support access to routing evidence is time-limited and tenant-scoped.

---

# Observability and Audit

Routing records request, inputs, eligibility result, destination category/assignment, policy/authority, priority, queue/capacity outcome, turn owner, expiry, fallback, reroute, and correlation references.

Metrics include routing latency, assignment rate, fallback/verification/deferment, queue wait, capacity rejection, reroute, handoff escalation, agent eligibility failure, workflow availability, channel mismatch, turn conflict, and destination outcome.

## Routing Explainability

The routing record identifies the policy version, applicable restrictions, eligible/rejected destination categories, priority/health/capacity factors, selected disposition, fallback reason, expiry, and correlation evidence. It provides authorized operators and tenant users with an appropriate explanation without exposing another tenant’s queue state, security policy internals, or protected configuration.

---

# Testing Strategy

## Contract Tests

Validate routing request, input, destination, decision, owner, expiry, fallback, and audit schemas.

## Policy and Integration Tests

Validate precedence, tenant/consent/identity/lifecycle restrictions, agent/human/workflow selection, handoff, verification, capacity, channel scope, fallback, and reroute.

## Security and Resilience Tests

Simulate cross-tenant route, stale assignment, withdrawn agent, unavailable queue, duplicate interaction, active handoff, dependency outage, capacity exhaustion, policy update, and concurrent routing. Prove no unqualified or duplicate response owner.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Routing request and decision schema | Defines inputs, destination, reason, policy, owner, expiry, and audit | Conversation Platform |
| Routing precedence and eligibility policy | Defines restriction order, agent/queue/workflow match, verification, fallback, and re-routing | Conversation Platform with Agent, Security, and tenant owners |
| Routing policy registry and lifecycle | Defines policy version, review, simulation, activation, migration, rollback, deprecation, and retirement | Conversation Platform with Security and tenant owners |
| Destination registry | Defines approved agent assignments, human roles/queues, workflow boundaries, channel scope, risk, and capacity metadata | Conversation Platform with dependent owners |
| Destination-health contract | Defines health, capacity, eligibility, freshness, maintenance, failure, and withdrawal signals | Conversation Platform with Agent, Integration, Channel, and Operations owners |
| Turn-ownership and reroute policy | Defines active owner, collaboration, cancellation, supersession, conflict, and delivery safeguards | Conversation Platform with Agent and Operations owners |
| Capacity, priority, and fairness policy | Defines quotas, limits, SLA, priority, queue behavior, exhaustion, and tenant fairness | Conversation Platform with Operations and tenant owners |
| Routing fallback and no-route matrix | Defines permitted fallback, waiting, notification, escalation, abandonment, and closure behavior | Conversation Platform with Channel, Operations, and tenant owners |
| Routing simulation and fairness suite | Defines dry-run scenarios, expected disposition, scorecard, disparity indicators, and remediation | Conversation Platform with Testing and tenant owners |
| Routing explainability record | Defines policy, evaluated/rejected destinations, factors, fallback, visibility, and audit | Conversation Platform with Security and Operations owners |
| Routing observability catalog | Defines signals, metrics, SLOs, audit, and diagnostic fields | Conversation, Operations, and Observability owners |
| Routing test suite | Validates contract, policy, tenant, integration, resilience, and security behavior | Conversation Platform and Testing Platform |

---

# Anti-Patterns

## Channel Chooses Intelligence

Provider-specific agent logic duplicates the Agent Brain and violates One Brain, Multi-Channel. Channels affect eligibility and presentation, not intelligence ownership.

## Route Equals Permission

Selecting an agent, queue, or workflow does not authorize context access, tool use, external action, or delivery.

## Last Write Wins Routing

Concurrent routes can produce conflicting human/agent responses. Use turn ownership, expected state, and controlled supersession.

## Capacity Bypass

Routing to an unqualified or unauthorized destination because the preferred queue is full creates safety and privacy risk. Use explicit fallback or deferment.

## Silent Fallback

Changing from agent to human, secure channel to less-secure channel, or action to deferment without recording reason and user impact destroys trust and auditability.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_CONVERSATION_ARCHITECTURE.md | Defines Routing Service responsibility and boundaries. |
| 02_CONVERSATION_LIFECYCLE.md | Defines state/transition conditions that gate routing. |
| 03_CONVERSATION_MODEL.md | Defines routing decision and conversation references. |
| 04_CONVERSATION_SESSION_MODEL.md | Defines turn/session ownership and expiry relationship. |
| 05_CONVERSATION_CONTEXT_MODEL.md | Defines bounded context available to a selected destination. |
| 07_CONVERSATION_EVENTS.md | Defines routing and assignment events. |
| 08_CONVERSATION_HANDOFF_MODEL.md | Defines human queue, collaboration, transfer, and return behavior. |
| 02_AGENT_PLATFORM/07_AGENT_RUNTIME_ARCHITECTURE.md | Receives authorized agent execution requests. |
| 02_AGENT_PLATFORM/28_AGENT_DEPLOYMENT_MODEL.md | Defines eligible deployment/assignment state. |
| 07_INTEGRATION_PLATFORM | Owns workflow and connector implementation. |
| 09_SECURITY_PLATFORM | Owns authorization, identity, consent, and security policy. |
| 11_OPERATIONS_PLATFORM | Owns operational queue, incident, and support procedures. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Conversation Routing document. |
| 2.1 | 2026-08-05 | Added policy lifecycle, simulation, destination health, fallback/no-route, fairness, explainability, and final artifacts. |
| 2.2 | 2026-08-06 | Added required document-owner metadata for governance and approval review. |
| 2.3 | 2026-08-06 | Moved to Review after internal consistency and Agent-boundary audit. |
| 2.4 | 2026-08-06 | Approved as the current Conversation Platform architecture source of truth. |

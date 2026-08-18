# 25_AGENT_PERMISSION_MODEL

**Version:** 2.1  
**Status:** Deprecated  
**Phase:** Agent Platform

**Replacement:** `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md` (Approved)  
**Deprecation Date:** 2026-08-07  
**Deprecation Note:** Retained for historical reference. Its previous authorization-ownership model is superseded by the approved Agent-to-Authorization boundary.

---

# Purpose

This document defines how the Agent Platform grants, evaluates, delegates, approves, revokes, and audits permission to access data, use capabilities, execute tools and workflows, administer configuration, and communicate through channels.

It turns the security principles in `24_AGENT_SECURITY_MODEL.md` into deterministic decisions: a user, agent, service, workflow, operator, or integration may act only on an explicitly permitted, tenant-scoped resource for an approved purpose and duration.

---

# Objectives

The Permission Model must:

- Provide one consistent authorization model across all platform components.
- Express permissions through subjects, actions, resources, scope, purpose, and conditions.
- Support human, service, agent, workflow, and delegated-user authority without identity confusion.
- Enforce least privilege, deny-by-default, approval, separation of duties, and rapid revocation.
- Keep decisions deterministic, auditable, explainable, and independent of any model or vendor.
- Combine role-based baseline access with dynamic policy constraints.
- Prevent agents, tools, workflows, channels, and events from bypassing permission checks.

---

# Scope

This document defines:

- Subjects, resources, actions, scopes, roles, grants, policies, decisions, and obligations.
- Policy evaluation, caching, revocation, denial, delegation, and approval behavior.
- Authorization for agent capabilities, context, knowledge, memory, tools, workflows, events, channels, and operations.
- Permission governance, audit, testing, and implementation artifacts.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Authentication, data protection, threat models, and security operations | `24_AGENT_SECURITY_MODEL.md` |
| Tenant partitioning and cross-tenant prevention mechanisms | `26_AGENT_TENANT_ISOLATION.md` |
| Channel protocol mapping and delivery mechanics | `22_AGENT_MULTI_CHANNEL_MODEL.md` |
| Conversation and session lifecycle | `23_AGENT_SESSION_MANAGEMENT.md` |
| Agent reasoning or model behavior | `08_AGENT_EXECUTION_ENGINE.md` |
| Tool interfaces and execution mechanics | `15_AGENT_TOOL_SYSTEM.md` and `16_AGENT_TOOL_EXECUTION_MODEL.md` |
| Workflow state-machine design | `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` |
| Enterprise directory groups and identity-provider configuration | Security Platform |

---

# Core Concepts

## Subject

A **subject** is the authenticated principal requesting or performing an action: human user, service workload, governed agent, workflow instance, operator, provider, or external integration. An agent is distinct from its initiating user; acting for that user requires bounded delegation.

## Resource and Action

A **resource** is a protected entity or data set, such as a conversation, knowledge document, memory record, agent configuration, workflow, tool, event subscription, credential, or delivery target. An **action** is an explicit operation such as `read`, `create`, `update`, `delete`, `execute`, `approve`, `publish`, `subscribe`, `deliver`, `replay`, or `administer`.

## Scope, Grant, Policy, and Obligation

A **scope** restricts a permission by tenant, organization, environment, region, resource, relationship, channel, capability, parameter, time, rate, or purpose. A **grant** is a versioned statement that authorizes a subject or role within a scope. A **policy** evaluates grants with current dynamic conditions. An **obligation** is a required condition on an allow, such as step-up authentication, approval, redaction, logging, rate limit, or a delivery restriction.

---

# Resource Hierarchy and Ownership

Permissions are evaluated against an explicit resource hierarchy. A typical hierarchy is:

```text
Platform
    -> Tenant
        -> Organization / Workspace
            -> Agent or Integration
                -> Conversation / Workflow / Knowledge Source
                    -> Session / Document / Memory Record / Tool Action
```

Parent scope can constrain a child resource but cannot silently broaden access. For example, a tenant-level role may permit access to approved resource families within that tenant, but classification, participant relationship, resource ownership, purpose, and child-level explicit deny may still prohibit a specific conversation, document, or tool action.

Every protected resource records its tenant, owner or owning service, parent relationship where applicable, classification, lifecycle, and policy-relevant attributes. A resource with missing or contradictory ownership is treated as inaccessible until corrected or reviewed.

---

# Permission Principles

## Deny by Default

An action is denied unless an applicable policy produces explicit allow. Missing context, ambiguous ownership, expired grant, unavailable policy evidence, or failed evaluation never creates implied access.

## Explicit Resource and Action

Permissions identify both resource type and action. Broad labels such as "agent access" or "admin" are insufficient without constrained scope. Wildcards are governed and cannot cross tenant, environment, or classification boundaries.

## Dynamic Policy Overrides Static Role

Roles provide baseline grants. Tenant, purpose, identity assurance, classification, consent, lifecycle state, risk, approval, and separation-of-duties rules may further restrict or deny them.

## Explicit Deny Wins

An explicit deny, revoked consent, revoked grant, tenant mismatch, classification restriction, or unmet obligation overrides an allow. Precedence is deterministic and auditable.

## No Transitive Privilege

Permission to use an agent, workflow, or tool does not confer every permission held by that component. Each downstream action is evaluated under its own subject, delegation, scope, and policy.

## Policy Precedence

When several policies or grants apply, the platform uses the following deterministic precedence:

1. Tenant-boundary, legal, regulatory, and environment restrictions.
2. Resource existence, ownership integrity, classification, retention, and lifecycle restrictions.
3. Identity validity, explicit deny, revoked grant, revoked consent, and revoked delegation.
4. Required identity assurance, approval, separation of duties, and risk controls.
5. Narrowest applicable allow from direct grant, role, ownership relationship, or delegated authority.
6. Obligations, rate limits, and time constraints attached to the resulting allow.

If rules conflict at the same precedence level, deny wins. A lower-precedence allow cannot override a higher-precedence restriction. Every decision records the policy versions and precedence result that produced it.

---

# Permission Architecture

```text
Authenticated Subject
    |
    v
Permission Request
    |
    v
Policy Decision Point
    |
    +--> Grants and Roles
    +--> Tenant and Resource Scope
    +--> Purpose, Classification, Consent, Risk
    +--> Delegation, Approval, and Revocation
    |
    v
Allow / Deny / Step-Up / Approval / Review
    |
    v
Policy Enforcement Point
    |
    v
Protected Action and Audit Outcome
```

## Policy Decision and Enforcement

The Policy Decision Point (PDP) evaluates the request against current grants, roles, policies, resource attributes, consent, risk, delegation, approval, and revocation data. Every protected service acts as a Policy Enforcement Point (PEP), validating the decision’s tenant, action, resource scope, expiry, and obligations before it acts. A PEP cannot substitute a broader action or reuse a decision for another resource.

---

# Permission Taxonomy

| Resource family | Examples |
|---|---|
| Tenant and administration | Tenant configuration, organizations, users, roles, policy assignments |
| Agent control plane | Agent definitions, instructions, capabilities, models, versions |
| Conversation and context | Conversations, sessions, snapshots, transcripts, attachments, handoffs |
| Knowledge and memory | Sources, documents, retrieval indexes, memory records, retention requests |
| Work execution | Agent executions, workflows, work items, approvals, schedules |
| Tools and integrations | Tool definitions, parameter schemas, connections, external accounts, credentials |
| Events and channels | Event subscriptions, replays, channel configurations, delivery targets, templates |
| Operations and audit | Logs, traces, dead letters, incident records, recovery controls |

Standard actions are `read`, `list`, `search`, `create`, `update`, `delete`, `execute`, `invoke`, `approve`, `reject`, `publish`, `subscribe`, `deliver`, `transfer`, `replay`, `pause`, `resume`, `export`, `administer`, and `impersonate`.

Sensitive behavior uses narrow actions such as `conversation.link_channel`, `tool.execute.payment_refund`, or `event.subscription.inspect_dead_letter`. Every grant and decision carries tenant/organization, environment/region, resource, action, purpose, classification, participant relationship, time, rate, approval, and applicable parameter constraints.

---

# Roles and Grants

## Role Model

Roles group repeatable baseline grants. Typical categories include tenant administrator, agent designer, knowledge manager, support operator, approver, auditor, integration operator, and runtime workload. Roles are tenant-scoped unless they are explicitly approved platform roles; platform roles do not imply tenant-data access.

## Direct Grants and Lifecycle

Direct grants are narrow, exceptional, or resource-specific. They contain a justification, owner, scope, effective time, expiry, and audit trail.

```text
Requested -> Reviewed -> Approved -> Active
                               |
                               v
                   Suspended / Revoked / Expired -> Retained for Audit
```

Creating, broadening, delegating, or renewing a high-risk grant requires the applicable approval and separation of duties. A grant becomes unusable immediately when revoked, expired, or invalidated by tenant, identity, or policy change.

---

# Permission Evaluation

## Request Contract

```text
authorizationRequest
|
+-- requestId
+-- subject and workload identity
+-- tenantId / organizationId / environment
+-- action and resource reference
+-- requested scope and parameter constraints
+-- business purpose
+-- session / conversation / event / workflow references
+-- delegation and approval references
+-- classification, consent, identity assurance, risk, and requested duration
```

## Evaluation Order

1. Authenticate the subject and validate tenant/environment context.
2. Validate request schema, action, resource, and required policy inputs.
3. Apply explicit deny, revocation, legal hold, consent, classification, and tenant-boundary rules.
4. Resolve eligible roles, grants, ownership, and delegation.
5. Evaluate purpose, risk, approval, separation of duties, rate, and time constraints.
6. Return scoped allow with obligations, or deny, step-up, approval, or review.

## Decision and Caching

The decision includes a unique decision reference, result, policy version, tenant, subject, action, resource scope, expiry, obligations, approvals, and audit reference. It is not a bearer token and cannot be reused for a different resource, parameter set, subject, tenant, purpose, or action.

Caching is permitted only within a decision’s explicit scope and expiry, with tenant partitioning, policy-version awareness, and revocation propagation. Changes to grants, roles, consent, identity, classification, ownership, or policy invalidate related cached decisions. Sensitive actions fail closed when the PDP or a required policy input is unavailable.

## Performance and Availability Standard

The platform defines authorization latency, availability, cache lifetime, and revocation-propagation targets by action risk level. High and critical actions require current or near-current evaluation and the shortest cache lifetime; low-risk reads may use a longer approved cache.

Each PEP has a documented degraded-mode behavior. It must fail closed for high or critical actions when a decision, revocation signal, or required policy input is unavailable. A degraded allow is permitted only for explicitly classified low-risk operations, within a bounded duration, and with enhanced logging and operational alerting.

---

# Agent, Workflow, Tool, and Delivery Authorization

## Agent Capability and Delegation

An agent may select only capabilities enabled for its approved configuration, tenant, and current execution. Capability selection is not permission to access every associated data source or execute every possible action.

When an agent acts for a user, the platform records the initiating user, agent identity, explicit delegation, purpose, scope, expiry, and decision. The agent cannot create, broaden, or extend its own delegation.

## Workflow and Tool Actions

Workflow initiation and every material transition are independently authorized. Tool execution requires a separate decision for the exact tool action, target resource, constrained parameters, tenant, user delegation where applicable, approval state, and intended output or delivery context.

## Context, Knowledge, Memory, Events, and Delivery

A reference to a conversation, document, memory record, transcript, attachment, or event is not permission to retrieve it; retrieval is separately authorized. Publishing, consuming, replaying, pausing, inspecting, or changing event subscriptions also requires its own scoped permission.

Outbound communication is a distinct `deliver` action. It verifies recipient, identity assurance, consent, communication preference, channel capability, content classification, quiet hours, template rules, and approval obligations.

---

# Delegation, Approval, and Emergency Access

## Delegation

Delegation is explicit, non-transitive, purpose-bound, and time-bound. It identifies delegator, delegate, actions, resources, tenant, constraints, expiry, and revocation status. It cannot grant privileges the delegator does not have and cannot be created from model output alone.

## Approval and Separation of Duties

An approval is an auditable decision by an eligible approver for a defined action, resource, parameter set, purpose, and time window. Material changes invalidate it. Policies may require different subjects for request, approval, execution, and audit; an agent or workflow cannot satisfy its own human-approval requirement.

## Approval Contract

Every approval request records the requesting subject, tenant, action, resource, parameter hash or constrained parameter set, purpose, risk level, required approver role, expiry, and decision context. The approval result records the approver, assurance level, timestamp, outcome, rationale where required, and immutable audit reference.

The policy defines whether one approver, multiple approvers, or dual control is required for each risk level. It also defines approval expiry, rejection handling, escalation, and the conditions that invalidate an approval: material change to target, parameters, scope, purpose, classification, risk, delegation, or applicable policy version.

## Emergency Access

Emergency access is limited to predefined critical recovery scenarios. It requires strong identity, explicit reason, narrow duration, enhanced monitoring, immutable audit, and post-event review. It is not a routine bypass of normal authorization.

---

# Permission Governance and Operations

Every role, grant template, action taxonomy entry, policy, and high-risk permission has a business and technical owner, version, approval history, review cycle, and retirement process. Permission changes are versioned, tested, reviewed by risk, auditable, reversible control-plane changes.

Tenant and platform roles, direct grants, service permissions, agent capabilities, delegations, and emergency access are periodically reviewed. Unused, stale, orphaned, or overbroad access is removed or narrowed. Operational recovery actions such as replay or override require explicit recovery permission and do not grant broad customer-data access.

## Entitlement Lifecycle

Entitlements follow a controlled joiner/mover/leaver lifecycle for human users, workload services, agents, integrations, and operators.

| Lifecycle event | Required permission behavior |
|---|---|
| New subject or service | Assign only approved baseline role(s) after identity and tenant binding are verified |
| Role, team, tenant, or responsibility change | Recalculate grants, revoke no-longer-valid access, and require approval for newly elevated access |
| Agent configuration or capability change | Re-evaluate the agent’s allowed capabilities, tools, data, and delegations before activation |
| Integration credential or provider change | Revalidate workload identity, scope, secret ownership, and allowed tenant/resource access |
| Departure, disablement, compromise, or tenant termination | Revoke active sessions, grants, delegations, credentials, cached decisions, and pending approvals within the applicable target |

Lifecycle automation must produce audit evidence and alert on incomplete or delayed revocation.

---

# Observability and Audit

Every material authorization request and enforcement outcome is traceable with privacy-preserving metadata:

- Request, decision, grant, policy, delegation, approval, and obligation references.
- Subject, workload, agent, tenant, environment, role, resource scope, and action.
- Purpose, classification, identity assurance, consent, risk, outcome, time, expiry, and policy version.
- Session, conversation, event, workflow, tool, channel, correlation, and trace references.

Metrics include allow/deny rate, decision latency, expired-decision use, step-up and approval frequency, policy errors, stale-grant findings, privilege-escalation attempts, and tenant-boundary denials.

---

# Testing Strategy

## Contract and Policy Tests

Tests validate action/resource schemas, role/grant formats, request/response contracts, obligations, compatibility, and audit references. Policies are tested for allow, deny, explicit-deny precedence, tenant scope, classification, consent, purpose, time, rate, delegation, approval, separation of duties, and revocation.

## Integration and Resilience Tests

Integration tests confirm that channel adapters, session services, runtime workers, context retrieval, workflows, tools, event consumers, and operational interfaces act as PEPs. Tests simulate forged decisions, expired delegation, unavailable policy, cache invalidation, role changes, cross-tenant requests, concurrent revocation, and emergency-access review. Sensitive actions must fail closed when checks cannot be performed.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Action and resource registry | Canonical vocabulary, risk level, owner, and schema for protected actions | Agent Platform |
| Role and grant catalog | Versioned role definitions, grant templates, scope, and review requirements | Agent Platform and tenant policy owner |
| Policy-as-code repository | Reviewed, testable, versioned policy logic and deployment record | Security and engineering owners |
| Authorization decision schema | Machine-readable request, response, obligation, expiry, and audit contract | Agent Platform and Security Platform |
| Delegation and approval register | Tracks scope, expiry, revocation, approvers, and outcomes | Agent Platform |
| Resource hierarchy and ownership registry | Defines parent/child relationships and policy-relevant ownership attributes | Agent Platform |
| Policy precedence specification | Defines the executable ordering, deny rules, and conflict-test cases | Security and engineering owners |
| Entitlement lifecycle runbook | Defines joiner/mover/leaver automation, revocation targets, exceptions, and evidence | Security and Operations owners |
| Approval workflow contract | Defines approver eligibility, quorum, expiry, invalidation, escalation, and audit | Agent Platform and tenant policy owner |
| Authorization performance standard | Defines latency, availability, caching, revocation, and degraded-mode targets | Platform engineering and Security owners |
| Policy test-fixture catalog | Provides stable representative subject/resource/tenant scenarios for regression tests | Engineering owners |
| Access-review report | Evidence of periodic role, grant, service, and capability review | Tenant and platform owners |
| Permission test suite | Regression, integration, security, and resilience tests | Feature owner with Security approval |

---

# Anti-Patterns

## Role Means Unlimited Access

Treating a role label as blanket authority ignores tenant, resource, classification, purpose, and risk. Roles are baselines; each material action remains policy-scoped.

## Agent Inherits User Privileges Permanently

An agent must not retain user authority beyond explicit, bounded delegation. Conversation history or preference does not create durable impersonation rights.

## Tool Permission from Prompt Text

Natural-language instructions, model plans, or tool names do not authorize parameterized external actions. The exact tool action and target are evaluated under current policy.

## Cached Allow After Revocation

Using stale authorization after revocation, consent change, or policy update creates a bypass. Cache only under controlled expiry and invalidation rules.

## Generic Admin Role Across Tenants

A broad platform role must not implicitly provide every tenant’s data access. Separate platform administration from tenant data and require scoped, audited elevation.

---

# Architecture Boundaries

| Document | Relationship |
|---|---|
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Enforces decisions before runtime execution and protects workload scope. |
| `08_AGENT_EXECUTION_ENGINE.md` | Treats reasoning and plans as inputs to, not substitutes for, authorization. |
| `11_AGENT_CONTEXT_MODEL.md` | Uses authorization to select minimal context and retrieve referenced data. |
| `14_AGENT_CAPABILITY_MODEL.md` | Defines capabilities; this model governs whether they may be selected or used. |
| `15_AGENT_TOOL_SYSTEM.md` | Evaluates permission for tool discovery, invocation, and parameterized actions. |
| `16_AGENT_TOOL_EXECUTION_MODEL.md` | Enforces scoped decisions, approval, and audit at execution. |
| `18_AGENT_MEMORY_INTEGRATION.md` | Governs access to memory records and retention actions. |
| `19_AGENT_KNOWLEDGE_INTEGRATION.md` | Governs source, document, and retrieval authorization. |
| `20_AGENT_WORKFLOW_INTEGRATION.md` | Requires permission for workflow initiation and material transitions. |
| `21_AGENT_EVENT_INTEGRATION.md` | Requires permission for event publication, subscription, replay, and recovery. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Requires permission for delivery, handoff, and channel association. |
| `23_AGENT_SESSION_MANAGEMENT.md` | Requires permission for context access, linking, lifecycle changes, and recovery. |
| `24_AGENT_SECURITY_MODEL.md` | Defines the governing security principles and decision boundary. |
| `26_AGENT_TENANT_ISOLATION.md` | Enforces tenant scope as a non-negotiable constraint. |

---

# Final Summary

The Permission Model is the deterministic authorization layer of the Agent Platform. It evaluates who may do what, to which resource, in which tenant, for what purpose, under which conditions, for how long, and with which approval or audit obligations.

By separating identity from authorization, roles from dynamic policy, agent identity from user delegation, and decisions from enforcement, the platform can provide useful AI capabilities without hidden or permanent privilege paths.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Permission Model architecture document. |
| 2.1 | 2026-08-05 | Added resource hierarchy, policy precedence, decision-service performance rules, approval contract, entitlement lifecycle, and final implementation artifacts. |

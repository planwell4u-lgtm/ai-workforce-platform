# 24_AGENT_SECURITY_MODEL

**Version:** 2.1  
**Status:** Deprecated  
**Phase:** Agent Platform

**Replacement:** `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` (Approved)  
**Deprecation Date:** 2026-08-07  
**Deprecation Note:** Retained for historical reference. Its previous security-ownership model is superseded by the approved Agent-to-Security boundary.

---

# Purpose

This document defines the security model for the Agent Platform. It establishes how users, agents, services, channels, events, tools, knowledge sources, memory, and operational staff are authenticated, authorized, isolated, monitored, and recovered in a multi-tenant AI Employee environment.

The model applies a zero-trust principle: agent-generated content, inbound messages, external events, provider callbacks, tool results, retrieved knowledge, and internal service requests are treated as untrusted until their identity, context, authorization, and policy conditions are verified.

---

# Objectives

The Agent Security Model must:

- Protect tenant data, credentials, identity, privacy, and business operations.
- Ensure an agent can act only through explicitly authorized capabilities, workflows, and tools.
- Prevent untrusted content from changing instructions, permissions, policy, or execution boundaries.
- Enforce least privilege, separation of duties, traceability, and revocable access.
- Secure interactions across channels, events, sessions, integrations, and runtime workers.
- Support data classification, minimization, encryption, retention, and lawful privacy controls.
- Detect, contain, investigate, and recover from security-relevant failures.
- Remain vendor- and transport-independent while supporting evolving models and integrations.

---

# Scope

This document defines:

- Agent Platform security principles and trust boundaries.
- Authentication, authorization, service identity, and delegated access requirements.
- Security controls for instructions, prompts, context, memory, knowledge, tools, workflows, events, sessions, and channels.
- Data protection, secrets management, audit, monitoring, incident response, and security testing requirements.
- The security decision model used by platform components.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise identity provider, directory, MFA, and corporate access policy | Security Platform |
| Network perimeter, host hardening, cloud account baseline, and physical security | Infrastructure and Security Platform |
| Detailed permission grants and role definitions | `25_AGENT_PERMISSION_MODEL.md` |
| Tenant data partitioning implementation | `26_AGENT_TENANT_ISOLATION.md` |
| Channel protocol and provider mapping | `22_AGENT_MULTI_CHANNEL_MODEL.md` |
| Session lifecycle and conversation continuity | `23_AGENT_SESSION_MANAGEMENT.md` |
| Tool contract and execution mechanics | `15_AGENT_TOOL_SYSTEM.md` and `16_AGENT_TOOL_EXECUTION_MODEL.md` |
| Enterprise incident-management process and compliance obligations | Security and Operations Platforms |

---

# Security Principles

## Zero Trust

No request, content item, service, channel, event, identity claim, network location, or prior conversation is inherently trusted. Each material action is evaluated against current identity, tenant, purpose, classification, authorization, and policy.

## Explicit Authorization

An agent, workflow, service, or human operator must have an explicit authorization for each protected action. Possession of an identifier, previous access, channel membership, or a model-generated plan does not confer permission.

## Least Privilege and Just-in-Time Access

Components receive only the narrowest permissions, data, duration, and scope required for the current task. Elevated or sensitive access is time-bound, purpose-bound, auditable, and revocable.

## Defense in Depth

Security controls are layered across ingress, identity, policy, runtime, context, tool execution, storage, events, delivery, and operations. Failure of one control must not create an unrestricted execution path.

## Secure by Default, Fail Closed for Sensitive Actions

When identity, authorization, tenant context, classification, integrity, or policy cannot be established, the platform denies or quarantines the request. It may offer a controlled verification, safe fallback, or human-review path.

## Data Minimization

The platform processes and retains only the data necessary for the authorized purpose. It uses references, redaction, scoped retrieval, and short-lived context rather than broad replication of sensitive data.

## Accountability

Every material automated action is attributable to an initiating actor or event, authorizing policy, execution identity, relevant context references, tool or workflow decision, and final outcome.

---

# Trust Boundaries

```text
External Users / Providers / Systems
    |
    v
Ingress Security Boundary
    |
    v
Channel and Event Normalization Boundary
    |
    v
Identity, Tenant, Consent, and Policy Boundary
    |
    v
Agent Runtime and Context Boundary
    |
    v
Workflow / Tool Authorization Boundary
    |
    v
Protected Data and External Action Boundary
```

Each boundary validates the inputs it receives and emits only the minimum approved output needed by the next component. A validated input at one boundary is not automatically trusted for a different purpose or a later action.

---

# Security Decision Model

Every protected operation uses a consistent decision process.

```text
Request or Trigger
    |
    v
Authenticate Subject and Service
    |
    v
Resolve Tenant, Purpose, and Resource Classification
    |
    v
Evaluate Permission, Policy, Consent, and Risk
    |
    +--> Deny / Quarantine / Require Step-Up / Human Review
    |
    v
Issue Scoped Authorization Decision
    |
    v
Execute and Record Outcome
```

## Decision Inputs

An authorization decision evaluates, as applicable:

- Subject identity: user, service, agent, workflow, operator, or external provider.
- Tenant, organization, environment, and region.
- Requested action, resource, scope, and business purpose.
- Role, permission, delegated authority, and approval state.
- Identity assurance, consent, classification, retention, and legal restrictions.
- Channel, device, source integrity, risk signals, rate limits, and time constraints.
- Current session, conversation, workflow, tool, and event context.

## Decision Output

The decision output is an immutable, auditable reference that records allow, deny, step-up, review, or constrained allow; its scope, expiry, policy basis, and obligations. It is not a reusable bearer credential and cannot be broadened by an agent.

## Security Decision Contract

The security decision model is implemented through a versioned, machine-readable contract. A request identifies the authenticated subject and workload, tenant, action, resource reference, purpose, classification, delegation, session or event reference, requested duration, and relevant risk signals.

The response includes the decision, policy and decision references, permitted scope, expiry, required obligations, approval or step-up requirement, audit reference, and denial reason category where safe to disclose. It must not expose policy internals or sensitive resource details to an unauthorized caller.

Authorization decisions are short-lived and purpose-bound. They may be cached only within their explicit scope and expiry, with tenant isolation and revocation support. If a decision cannot be obtained or validated, sensitive actions fail closed; low-risk operations may use only an explicitly approved degraded-mode policy.

---

# Control Plane and Data Plane Security

The **control plane** manages agent definitions, instructions, capabilities, policies, tenant configuration, tool registration, provider configuration, model selection, permission grants, and deployment settings. The **data plane** processes interactions, events, context, agent execution, workflow work, tool invocation, and delivery.

Control-plane changes have elevated security impact. They require authenticated administration, tenant and environment scope, versioning, approval appropriate to risk, audit records, rollback capability, and separation of duties where required. A data-plane agent or runtime worker cannot modify its own instructions, permissions, enabled tools, security policy, model-provider configuration, or tenant boundaries.

Control-plane credentials, services, and operator roles are distinct from data-plane workload identities. A compromise in one plane must not silently grant unrestricted access to the other.

---

# Identity and Authentication

## Human Identity

Human users authenticate through enterprise-approved identity mechanisms. Channel identifiers such as email addresses, phone numbers, browser sessions, and messaging-provider accounts are evidence, not automatic proof of account identity.

The required authentication assurance is proportional to the requested action and data classification. High-impact actions require the applicable step-up verification even if a user has an active conversation.

## Service and Workload Identity

Every platform service, adapter, worker, event producer, consumer, workflow, and tool connector has a verifiable workload identity. Services authenticate to one another using short-lived credentials or equivalent approved mechanisms; shared static credentials are prohibited.

## Agent Identity

An agent is a governed software identity, distinct from the user who initiated work and distinct from the runtime worker executing it. The agent identity identifies its approved configuration, tenant scope, capabilities, policy version, and permitted delegation boundary.

An agent must never impersonate a human user without explicit delegated authorization, clear audit attribution, and applicable consent.

## External Provider Identity

Channel providers, webhooks, integration partners, and external event sources require verified identity, signature or token validation, freshness checks, replay protection, and tenant/provider binding before their data is accepted.

---

# Authorization and Delegation

## Authorization Layers

The platform evaluates authorization at multiple layers:

| Layer | Decision |
|---|---|
| Ingress | May this source submit this interaction or event? |
| Context | May this execution access this data for this purpose? |
| Agent capability | May this agent select this capability? |
| Workflow | May this process start, continue, or transition? |
| Tool | May this exact action run against this resource with these parameters? |
| Delivery | May this result be sent to this recipient through this channel? |
| Operations | May this operator inspect, replay, alter, or recover this scoped data? |

Passing one layer never implies passing another.

## Delegated User Authority

When an agent or workflow acts on behalf of a user, it receives only an explicit, scoped delegation. The delegation identifies the user, action, resource scope, purpose, expiry, and any required approval. It cannot be transferred, extended, or used for unrelated actions.

## Approval and Separation of Duties

High-impact, irreversible, financial, regulated, privileged, or external actions may require human approval or dual control. The requesting agent, approver, executor, and auditor must be logically separable where policy requires it.

---

# Instruction, Prompt, and Context Security

## Instruction Hierarchy

Approved system instructions, tenant policy, capability constraints, and runtime safety rules remain authoritative over user input, retrieved content, event payloads, tool results, and external documents. Untrusted content cannot alter the instruction hierarchy or request disclosure of protected context.

## Prompt and Content Injection

All untrusted content is labeled by source, classification, and provenance before it enters an authorized context snapshot. The platform applies input validation, retrieval filtering, content isolation, structured tool interfaces, and policy checks to reduce prompt injection and data-exfiltration risk.

The platform must not rely solely on model behavior to enforce security. A model may propose an action, but deterministic policy and authorization controls decide whether it can occur.

## Context Boundaries

Context snapshots are immutable, minimal, expiry-bound, tenant-scoped, and purpose-bound. They include references to restricted resources only when the current execution is authorized to retrieve them. Hidden instructions, credentials, private reasoning, and unrelated tenant data are never exposed as context.

## Output Safety

Before user-facing delivery or external action, outputs are evaluated for authorization, classification, destination, content policy, required disclosures, and action-specific constraints. Output filtering does not replace the earlier access-control layers.

---

# Data Protection and Privacy

## Classification

All data is assigned or inherited a classification appropriate to its sensitivity, such as public, internal, tenant-confidential, restricted, or regulated. Classification determines access, storage, logging, encryption, retention, delivery channel, and human-review requirements.

## Encryption and Key Management

Sensitive data is encrypted in transit and at rest using Security Platform-approved mechanisms. Key management, rotation, separation, recovery, and access are centrally governed. The Agent Platform must not embed keys in code, prompts, session state, event payloads, or logs.

## Data Minimization and Redaction

Services request the smallest field set and shortest retention necessary. Logs, traces, analytics, model prompts, and support tools use redaction or references by default. Raw transcripts, attachments, and regulated data require explicit justification and controlled access.

## Retention, Deletion, and Residency

Data retention, deletion, legal hold, anonymization, and residency follow tenant agreement, classification, regulation, and approved policy. The platform records deletion and retention actions without retaining unnecessary sensitive content.

---

# Secrets and Configuration Security

Secrets include provider credentials, API keys, signing material, tokens, encryption keys, connection strings, and privileged configuration. They are stored, issued, rotated, and revoked through approved secret-management controls.

Secrets must never appear in source control, model context, conversation records, event payloads, prompts, telemetry, error messages, or human-handoff notes. Services receive short-lived, scoped secret access where possible and fail closed when secrets cannot be obtained safely.

Agent and tenant configuration changes require authenticated, authorized, audited control-plane operations with versioning, review, rollback, and separation of duties where appropriate.

---

# Channel and Session Security

Channel adapters validate provider identity, signatures, timestamps, message uniqueness, replay protection, tenant binding, content limits, malware-scanning requirements, and consent context before normalizing an interaction.

Session Management protects session identifiers from fixation, guessing, substitution, replay, and leakage. A channel thread or phone number is not a bearer authorization token. Cross-channel linking requires current participant evidence, purpose, tenant policy, classification controls, and, when required, verified identity.

Outbound delivery requires recipient validation, current consent, channel eligibility, classification review, and any necessary approval. A completed agent execution never automatically authorizes a communication.

---

# Event, Workflow, and Tool Security

## Event Security

Event producers and consumers use authenticated service identities and authorization scoped by event type, tenant, classification, and action. External events are validated and normalized before becoming trusted platform events. Replay, dead-letter inspection, and subscription changes are restricted, audited operational actions.

## Workflow Security

Workflow initiation, transitions, compensation, approval, and cancellation are authorized independently from the triggering interaction. A workflow carries correlation and authorization references but must re-evaluate policy for material steps and side effects.

## Tool Security

Tools execute only through the Tool System. Each invocation validates the requester, agent capability, user delegation where applicable, action parameters, resource scope, tenant, approval requirements, rate limit, and intended destination.

Tool results are untrusted data until validated. They cannot grant new privileges, alter agent instructions, or cause a follow-on action without a separate authorization decision.

---

# Runtime and Model Security

Runtime workers are isolated by tenant, environment, workload identity, and least-privilege service permissions. They receive only short-lived authorized context and do not persist durable secrets or unrestricted conversation state locally.

Model-provider access is governed by approved provider configuration, data-processing rules, region, classification, and observability controls. The platform must record the model and policy version used for material executions while avoiding the storage of unnecessary prompt or response content.

Model selection, fallback, and retry must not weaken classification, residency, consent, tool authorization, or output-safety requirements.

## Model Provider Assurance

Each approved model provider and model configuration has a documented assurance record covering provider identity, contract and data-use terms, supported deployment region, classification eligibility, data residency, encryption, retention and training-use expectations, available audit evidence, incident-notification obligations, and approved use cases.

A provider, region, model, or fallback change is a controlled configuration change. It requires compatibility and security review before production use, and the Runtime must select only a configuration eligible for the current tenant, classification, and purpose. If no eligible provider is available, the platform fails safely or follows an approved non-model fallback; it does not silently route restricted data to a less suitable provider.

---

# Risk Classification and Escalation

Every protected action is assigned a risk level based on impact, reversibility, identity assurance, data classification, external reach, financial or legal consequence, and potential for abuse.

| Risk level | Examples | Minimum control posture |
|---|---|---|
| Low | Public information, non-sensitive drafting, internal status lookup | Authenticated access, tenant scope, logging, rate limits |
| Moderate | Tenant-confidential lookup, customer support response, reversible update | Current authorization, classified context, delivery controls, audit trail |
| High | Account change, external communication to a verified user, sensitive-data retrieval, workflow side effect | Strong identity assurance, explicit scope, policy obligations, enhanced logging, approval where policy requires |
| Critical | Payments, privileged administration, bulk communication, regulated-data export, irreversible external action | Step-up verification, explicit approval or dual control, constrained execution, real-time monitoring, recovery plan |

The detailed mapping of actions to risk level belongs in the Permission Model and tenant policy. An agent may not lower an action's risk classification or bypass an escalation requirement.

---

# Security Observability and Audit

Security-relevant events are centrally collected, protected from unauthorized alteration, and retained according to policy. Logs and traces must avoid secrets and unnecessary sensitive content.

Required audit information includes:

- Actor, service, agent, tenant, environment, and workload identity.
- Authentication, authorization, delegation, approval, consent, and identity-assurance decisions.
- Accessed resource references, classification, action scope, and outcome.
- Agent configuration, instruction, capability, policy, model, tool, workflow, and channel references.
- Event, conversation, session, correlation, causation, and trace identifiers.
- Security control failures, denials, step-up requests, quarantines, exceptions, and operator actions.

Security monitoring detects anomalous access, repeated denials, unexpected privilege use, prompt-injection indicators, abnormal tool activity, tenant-boundary violations, suspicious event patterns, credential misuse, data-exfiltration signals, and delivery anomalies.

---

# Incident Response and Recovery

## Containment

The platform can revoke service credentials, disable an agent or capability, pause a tool, quarantine a channel or event source, suspend a tenant integration, block delivery, and invalidate active authorization decisions according to approved incident procedures.

## Investigation

Investigations use immutable audit references, bounded access to protected records, tenant-scoped search, and separation of duties. Operators must not obtain broad transcript, prompt, or customer-data access merely to investigate a platform signal.

## Recovery

Recovery verifies configuration integrity, credential rotation, policy correctness, tenant scope, data consistency, and idempotency before re-enabling work or replaying events. Replay or retry cannot bypass current security controls.

---

# Security Testing and Assurance

## Required Testing

Security validation includes:

- Authentication, service identity, token expiry, and credential-rotation tests.
- Authorization, delegation, approval, separation-of-duties, and revocation tests.
- Tenant-isolation, cross-channel linking, session-fixation, and replay-resistance tests.
- Prompt-injection, data-exfiltration, malicious attachment, and untrusted tool-result tests.
- Event authenticity, schema validation, dead-letter, replay, and subscription-authorization tests.
- Tool parameter validation, privilege escalation, external-action, and idempotency tests.
- Logging/redaction, encryption, retention, deletion, and incident-recovery tests.

## Threat Modeling

Every new agent capability, tool, channel, workflow, external integration, sensitive data class, and model-provider change requires proportionate threat modeling before production enablement. The threat model records assets, trust boundaries, abuse cases, mitigations, residual risk, owner, and approval.

## Security Exceptions

Any exception to a security requirement must be time-bound, scoped, risk-assessed, approved by the designated authority, monitored, and reviewable. An exception does not silently become a permanent platform behavior.

---

# Software Supply-Chain and Deployment Security

Builds, dependencies, infrastructure definitions, container images, deployment packages, and runtime configurations are treated as security-sensitive inputs. The delivery pipeline must use approved source repositories, dependency and vulnerability scanning, secret scanning, software-bill-of-materials generation, artifact provenance or signing, environment separation, and controlled deployment admission.

Production deployment verifies that the artifact, configuration, policy version, and approved dependency posture match the release record. Critical vulnerabilities, compromised credentials, unapproved artifacts, or materially unsafe configuration block deployment or trigger the approved exception process.

Runtime images and dependencies are regularly patched according to risk, exposed surface, and service criticality. Emergency changes remain audited and are reconciled into the normal change record after containment.

---

# Security Control Matrix

The platform maintains a versioned control matrix that converts this architecture into testable release criteria.

| Control area | Required control | Evidence | Primary owner |
|---|---|---|---|
| Identity | Verified human, service, agent, and provider identities | Authentication and token-expiry tests; identity audit records | Security Platform |
| Authorization | Scoped, current decision for every material action | Decision contract tests; policy and audit references | Agent Platform and Security Platform |
| Tenant protection | Tenant scope enforced in storage, routing, events, and operations | Isolation tests and access logs | Agent Platform |
| Untrusted content | Provenance, isolation, validation, and deterministic action gates | Injection and exfiltration tests | Agent Platform |
| Data protection | Classification, encryption, minimization, redaction, and retention | Data-handling tests and configuration evidence | Security Platform |
| Tools and workflows | Parameter validation, approval, idempotency, and audit | Tool/workflow security tests | Agent Platform |
| Channels and sessions | Provider validation, consent, identity assurance, replay controls | Adapter and session security tests | Channel owner |
| Supply chain | Approved dependencies, provenance, scanning, and admission controls | Build and release attestations | Engineering and Operations |
| Detection and recovery | Monitoring, containment, investigation, and replay controls | Alerts, runbooks, incident exercises | Security and Operations |

Each production feature identifies the controls it depends on, the evidence generated, the responsible owner, and any approved exception. Missing evidence blocks release when the required control is applicable.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Security decision contract | Machine-readable input, output, obligations, and audit reference for authorization decisions | Agent Platform and Security Platform |
| Data-classification and handling matrix | Defines access, logging, encryption, retention, and delivery controls by classification | Security Platform |
| Agent capability and tool permission map | Maps agents and capabilities to allowed actions and approval requirements | Agent Platform |
| Threat-model register | Records approved threats, controls, residual risks, and reviews | Security owner and feature owner |
| Secret and credential inventory | Tracks owner, scope, rotation, revocation, and provider association | Security and Operations owners |
| Model-provider assurance register | Records provider, region, classification eligibility, data-use controls, and approved configurations | Security and Agent Platform owners |
| Risk and escalation register | Maps actions to risk level, approval, step-up, monitoring, and recovery requirements | Agent Platform and tenant policy owner |
| Supply-chain assurance record | Records dependency posture, SBOM, provenance, scans, and deployment admission evidence | Engineering and Operations owners |
| Security test suite and release checklist | Demonstrates required controls before production enablement | Feature owner with Security approval |
| Incident and recovery runbooks | Defines containment, investigation, recovery, and communication procedures | Operations and Security owners |

---

# Anti-Patterns

## Model Output as Authorization

Treating an agent's plan, confidence, or natural-language response as proof that an action is permitted allows prompt injection and privilege escalation. Authorization must be deterministic and external to the model.

## Channel Identity as Account Verification

Assuming a sender address, phone number, call, or chat account proves a user's identity can expose protected data. Apply the required assurance for the action and context.

## Broad Tool Credentials

Giving a general-purpose agent broad API credentials creates uncontrolled blast radius. Tools must use scoped, policy-checked, auditable access for a specific action and resource.

## Secrets in Context or Logs

Passing credentials through prompts, events, transcripts, error messages, or support notes makes them difficult to control and rotate. Use approved secret-management and redaction controls.

## Security by Prompt Alone

Instructions that tell a model to "be secure" are useful behavior guidance, not a security boundary. Enforce access, parameter, data, and delivery controls in deterministic platform services.

## Permanent Exception

An undocumented temporary bypass becomes an invisible long-term vulnerability. Every exception requires scope, owner, expiry, monitoring, and review.

---

# Architecture Boundaries

| Document | Relationship |
|---|---|
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Applies workload identity, isolation, context, and execution security boundaries. |
| `08_AGENT_EXECUTION_ENGINE.md` | Keeps reasoning and output generation subordinate to security policy and authorization. |
| `11_AGENT_CONTEXT_MODEL.md` | Applies minimal, classified, authorized context snapshots. |
| `12_AGENT_INSTRUCTION_SYSTEM.md` | Defines instruction authority preserved against untrusted content. |
| `15_AGENT_TOOL_SYSTEM.md` | Executes scoped, authorized tool actions only. |
| `16_AGENT_TOOL_EXECUTION_MODEL.md` | Applies runtime validation, approval, and audit to tool execution. |
| `18_AGENT_MEMORY_INTEGRATION.md` | Governs secure access to memory under classification and purpose controls. |
| `19_AGENT_KNOWLEDGE_INTEGRATION.md` | Governs provenance, retrieval, and protection of knowledge content. |
| `20_AGENT_WORKFLOW_INTEGRATION.md` | Requires authorized workflow transitions and side effects. |
| `21_AGENT_EVENT_INTEGRATION.md` | Secures event publication, subscription, replay, and event-triggered execution. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Applies secure channel ingress, identity, consent, and delivery controls. |
| `23_AGENT_SESSION_MANAGEMENT.md` | Applies session identity, context, continuity, and state-access controls. |
| `25_AGENT_PERMISSION_MODEL.md` | Defines detailed grants, roles, policies, and authorization evaluation. |
| `26_AGENT_TENANT_ISOLATION.md` | Defines tenant-boundary enforcement across data, services, and operations. |

---

# Final Summary

The Agent Security Model makes security a platform property rather than a model behavior. It requires explicit, current authorization at every material boundary; treats all content and integrations as untrusted until verified; protects tenant data through minimization and controlled context; and keeps agent, workflow, and tool actions accountable.

By combining zero trust, least privilege, deterministic policy enforcement, defense in depth, and auditable recovery controls, the platform can safely deliver AI Employee capabilities across channels and integrations without granting uncontrolled autonomy.

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Security Model architecture document. |
| 2.1 | 2026-08-05 | Added security-decision contract, control/data-plane boundary, model-provider assurance, risk classification, supply-chain security, control matrix, and final implementation artifacts. |

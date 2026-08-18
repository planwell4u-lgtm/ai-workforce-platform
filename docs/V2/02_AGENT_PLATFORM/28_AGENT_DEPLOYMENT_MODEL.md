# 28_AGENT_DEPLOYMENT_MODEL

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document defines how approved Agent Platform configurations are promoted, activated, assigned, verified, suspended, and withdrawn across environments and tenant scopes.

Agent deployment is the controlled act of making an immutable agent version eligible to receive work. It is distinct from deploying software infrastructure: the Agent Platform deploys governed agent behavior, while the Deployment Platform deploys the services and infrastructure that run it.

---

# Purpose

The purpose of the Agent Deployment Model is to make the transition from a validated agent version to a live, user-facing Agent Brain safe, repeatable, observable, tenant-scoped, and reversible.

It ensures that deployment does not bypass versioning, security, permission, tenant isolation, channel constraints, evaluation evidence, or operational readiness.

---

# Objectives

The Agent Deployment Model must:

- Promote only approved immutable agent versions through controlled environments.
- Separate agent configuration deployment from software and infrastructure deployment.
- Bind deployments to tenant, environment, assignment scope, channel eligibility, and release policy.
- Verify dependencies, authorization, evaluation, capacity, and operational readiness before activation.
- Support preview, staged rollout, suspension, rollback, and withdrawal without altering history.
- Ensure all channels resolve the same approved Agent Brain unless policy explicitly assigns an eligible experiment.
- Preserve execution continuity and prevent new work from reaching an invalid, revoked, or withdrawn version.
- Produce complete deployment, activation, health, and audit evidence.

---

# Scope

This document defines:

- Agent deployment units, targets, assignments, environments, and deployment states.
- Promotion, activation, readiness verification, staged rollout, suspension, rollback, and withdrawal.
- Agent-specific dependency, security, tenant, channel, observability, and operational requirements.
- The boundaries between agent deployment and infrastructure deployment.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Containers, Kubernetes, Helm, Terraform, CI/CD pipelines, network, and runtime infrastructure | Deployment Platform |
| Software artifact build, image provenance, dependency scans, and deployment admission controls | Engineering, Deployment, and Security Platforms |
| Agent-version semantics, manifest immutability, and version compatibility | `27_AGENT_VERSIONING_MODEL.md` |
| Runtime worker scheduling, autoscaling, and process lifecycle | `07_AGENT_RUNTIME_ARCHITECTURE.md` and Operations Platform |
| Tenant authorization, role grants, approval, and security policy | `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md`, `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md`, and Security Platform |
| Channel-provider deployment, phone-number provisioning, and protocol configuration | `22_AGENT_MULTI_CHANNEL_MODEL.md` and Channel Platforms |
| Enterprise incident-management and release-management processes | Operations Platform |

---

# Core Concepts

## Deployment Unit

A **deployment unit** is a released immutable agent version plus its approved manifest, dependency eligibility, validation evidence, and deployment policy. It does not contain secrets, mutable “latest” references, raw customer data, or infrastructure artifacts.

## Deployment Target

A **deployment target** identifies the tenant, environment, region/residency scope, agent identity, allowed channels, and traffic or assignment scope in which a deployment unit may be activated.

## Assignment

An **assignment** maps an eligible deployment unit to an authorized execution population. It may be a default assignment, named preview cohort, channel-eligible cohort, experiment cohort, or a bounded traffic percentage. Assignments are versioned, tenant-scoped, auditable, and reversible.

## Environment

An **environment** is an approved logical stage such as development, test, staging, preview, or production. Environment eligibility is policy-controlled; a production deployment cannot source a draft or unapproved test configuration.

## Deployment Record

A **deployment record** is the immutable audit record of a promotion, readiness result, activation, assignment change, suspension, rollback, or withdrawal.

---

# Deployment Principles

## Configuration Deployment Is Separate From Software Deployment

Deploying a new agent version changes governed agent behavior. Deploying a runtime service changes the software that may execute it. Both require controls, but each has separate ownership, approvals, observability, and rollback paths.

## Promote, Do Not Rebuild

The same immutable released version is promoted across environments when eligible. A deployment process must not rebuild, rewrite, or substitute the version manifest. Environment-specific operational configuration is referenced through approved deployment policy and cannot broaden agent permissions.

## Readiness Before Activation

An agent version is activated only after validation evidence, authorization, dependency eligibility, tenant state, model/provider eligibility, channel readiness, capacity policy, observability, and rollback target are confirmed.

## Tenant and Channel Scope Are Explicit

Every deployment and assignment names its tenant and permitted channels. A deployment cannot be treated as global because a field is missing, and channel availability never overrides tenant consent, classification, delivery policy, or version eligibility.

## Fail Safe

If deployment readiness, dependency validation, authorization, policy, or tenant state cannot be verified, activation is blocked. Existing safe assignments remain unchanged unless an authorized safety withdrawal is required.

---

# Deployment Lifecycle

```text
Released Version
    -> Eligible for Target
    -> Readiness Verified
    -> Deployed
    -> Activated / Assigned
    -> Monitored
    -> Suspended / Rolled Back / Withdrawn
    -> Retained for Audit
```

## Eligibility

An agent version is eligible for a target only when it is released, tenant-owned or validly adopted, compatible with the target environment, compliant with current policy, and supported by every required dependency.

## Readiness Verification

Readiness verifies:

- Version manifest integrity and release status.
- Tenant, environment, region, and residency eligibility.
- Required authorization, approval, risk, and separation-of-duties evidence.
- Tool, workflow, capability, model, knowledge, memory, and channel-policy eligibility.
- Evaluation, regression, security, and operational evidence appropriate to risk.
- Runtime capacity and compatible service availability reported by owning platforms.
- Observability, alerting, support ownership, stop conditions, and rollback target.

## Activation and Assignment

Activation makes a deployment unit available for its approved assignment. New executions resolve the assignment according to tenant, agent, environment, channel, and experiment policy. In-flight executions remain pinned to their resolved version unless safety policy requires controlled termination.

## Suspension and Withdrawal

Suspension temporarily blocks new work for a deployment or assignment while preserving its record. Withdrawal removes eligibility for new work because of security, dependency, policy, tenant, operational, or business conditions. Both actions are auditable and may trigger safe fallback, handoff, or incident procedures.

## Deployment State Transitions

| Current state | Permitted transition | Authorized actor | Required condition |
|---|---|---|---|
| Eligible | Readiness Verified | Deployment service or authorized operator | Version, tenant, dependencies, evidence, and target are valid |
| Readiness Verified | Deployed | Deployment service | Deployment record and rollback target are created |
| Deployed | Activated / Assigned | Authorized deployer | Required approval, channel readiness, and assignment policy are satisfied |
| Activated / Assigned | Suspended | Authorized deployer, safety control, or incident process | Stop condition, policy, tenant, or operational reason is recorded |
| Activated / Assigned | Rolled Back | Authorized deployer or incident process | Eligible rollback target and approved scope are verified |
| Activated / Assigned or Suspended | Withdrawn | Security, tenant, or authorized operational process | Security, policy, dependency, or business withdrawal condition is present |
| Suspended | Activated / Assigned | Authorized deployer | Current readiness and authorization are revalidated |

Every transition emits an authorized deployment fact and records actor, tenant, environment, assignment scope, reason, prior/resulting state, expected version, and correlation identifiers.

## Deployment Concurrency

Only one material deployment operation may change the assignment for a given tenant, agent, and environment target at a time. The deployment service uses an expected deployment-record version or equivalent lock to prevent concurrent activation, rollback, suspension, or withdrawal from overwriting one another.

If a conflict occurs, the operation reloads the current target state and re-evaluates authorization, readiness, stop conditions, and rollback eligibility. It must not use last-write-wins behavior or assume that a previously valid approval remains valid after scope changes.

---

# Deployment Flow

```text
Released Agent Version
    |
    v
Target Eligibility and Readiness Check
    |
    +--> Block / Remediate
    |
    v
Authorized Deployment Record
    |
    v
Activation and Assignment
    |
    v
Runtime Resolution for New Executions
    |
    v
Monitoring and Stop-Condition Evaluation
```

The deployment service requests activation through controlled Agent Platform interfaces. It never directly alters runtime state, channel-provider configuration, tool credentials, tenant policy, or infrastructure resources.

---

# Promotion and Environment Controls

## Promotion Path

The standard path is:

```text
Draft -> Test / Evaluation -> Staging -> Approved Preview -> Production
```

Promotion may skip no mandatory validation stage. An emergency deployment uses a separately approved emergency process with enhanced audit, limited scope, monitoring, and post-deployment review.

## Environment Separation

Each environment has distinct tenant data rules, credentials, model eligibility, tools, integrations, channels, and observability settings. Production versions must not use test credentials, unrestricted test data, or unreviewed provider configurations.

## Configuration Overlays

Environment-specific overlays may configure non-behavioral operational settings such as endpoint routing, rate limits, or observability destinations where policy permits. An overlay cannot change the agent’s instructions, capabilities, permissions, dependency manifest, tenant scope, data classification, or approval requirements; those changes require a new agent version.

## Channel Readiness Matrix

Before activation, each permitted channel has an approved readiness entry for the tenant, environment, and agent assignment.

| Channel area | Required readiness evidence |
|---|---|
| Voice | Tenant-bound number/provider configuration, media route, call policy, capacity, consent, and fallback path |
| Web or app chat | Authorized client integration, tenant routing, identity/session behavior, rate limit, and delivery controls |
| Messaging and email | Provider binding, opt-in/template/window requirements, recipient policy, delivery status, and fallback path |
| API | Client identity, contract version, tenant scope, quota, idempotency, and error behavior |

An unavailable or unapproved channel is excluded from the assignment. Channel readiness does not change the Agent Brain version or grant permission to send a communication.

---

# Rollout and Assignment Controls

## Staged Rollout

Staged rollout uses approved assignments such as internal preview, named tenant cohort, defined participant cohort, permitted channel cohort, or bounded percentage. The rollout policy records entry criteria, scope, evaluation signals, owner, monitoring window, success criteria, stop conditions, and rollback target.

## Assignment Precedence

When multiple eligible assignments exist, the resolver applies deterministic precedence:

1. Safety or security withdrawal.
2. Tenant suspension, channel restriction, consent, or classification restriction.
3. Explicit approved experiment assignment for the current continuity window.
4. Named preview or cohort assignment.
5. Default active production assignment.

If no eligible assignment remains, the platform does not invoke the agent. It follows an approved safe fallback, queue, or human-handoff path.

## Deployment Continuity

Conversation and session continuity follows the version-pinning rules in the Versioning Model. A rollout change affects only new eligible executions unless controlled migration is explicitly approved.

## Success and Stop Conditions

Each rollout defines measurable baseline, success, warning, and stop thresholds for the affected scope. At minimum, it monitors version-specific execution success, latency, policy/security denials, tool and workflow failures, channel-delivery failure, dependency health, user-impact signals, and error-budget consumption.

A breach of a stop threshold automatically pauses expansion and creates an operational signal. The authorized owner decides whether to resume, narrow the scope, rollback, suspend, or withdraw according to the rollout and incident policy. Thresholds are tenant-, risk-, and channel-aware; they are not global defaults.

---

# Dependency and Change Management

## Dependency Health

The deployment service continuously monitors the eligibility of referenced capabilities, tools, workflows, policies, model providers, knowledge/memory access profiles, and channel policies. A dependency change does not mutate the version manifest; it can only change whether a deployment remains eligible.

## Breaking Change Response

When a dependency becomes revoked, insecure, retired, incompatible, unavailable, or non-compliant, the platform identifies affected deployments. It blocks new activation and, based on risk, suspends, withdraws, or routes affected work to an approved fallback. Replacement requires a new compatible agent version.

## Change Coordination

Material agent deployment change requires review of affected Agent, Conversation, Channel, Integration, Security, Data, Operations, and Deployment Platform boundaries as appropriate. Architecture changes follow the project decision and change-management process.

---

# Security and Tenant Controls

Deployment actions—promote, activate, assign, suspend, rollback, withdraw, and inspect protected records—require tenant-scoped authorization. High-risk production deployments require the approval and separation-of-duties controls defined by the Permission and Security Models.

Deployment records contain references and digests, not secrets, credentials, raw customer data, private model reasoning, or unrestricted operational configuration. A platform administrator does not gain tenant-content access merely by administering a deployment.

Tenant suspension, revoked consent, invalid policy, or security withdrawal takes precedence over an active assignment. No deployment action may use a default tenant or silently expand a tenant/cohort scope.

---

# Observability and Operational Readiness

Every deployment records version, manifest digest, tenant, environment, target, assignment, actor, approval, readiness evidence, dependencies, start/end time, result, rollback target, and correlation identifiers.

Deployment health is evaluated through version-specific execution success, latency, safety/policy denials, tool/workflow outcomes, channel-delivery outcomes, dependency health, quota/capacity signals, user-impact signals, and alert thresholds. Observability Platform owns telemetry infrastructure; this model defines the agent deployment information required by it.

Each production assignment has a named business owner and operational owner, a support path, alert routing, stop conditions, and an approved rollback or withdrawal plan.

## Post-Deployment Verification and Sign-Off

After activation, the deployment owner verifies that the resolved version, tenant scope, assignment, channel routing, policy enforcement, dependency health, telemetry, alerting, and rollback target match the approved deployment record. The verification uses representative safe interactions and does not expose customer data unnecessarily.

The business owner and operational owner record completion or an exception within the rollout’s defined verification window. A rollout remains in monitored state until the required sign-off and success criteria are met; it is not considered complete merely because activation succeeded.

---

# Deployment Management Contract

The Agent Platform exposes a versioned deployment-management contract for authorized control-plane operations. It supports:

- Create or evaluate a target eligibility request.
- Request readiness verification and retrieve evidence.
- Create, update, or remove a tenant-scoped assignment.
- Activate, suspend, rollback, withdraw, and inspect a deployment.
- Retrieve deployment provenance, health, transition history, and post-deployment verification state.

Every request identifies the immutable agent version, tenant, environment, target, assignment scope, expected deployment-record version, actor, authorization/approval references, reason, and correlation identifiers. Responses include the resulting state, evidence references, obligations, conflict or denial category where safe to disclose, and audit reference.

The contract does not expose infrastructure controls, credentials, raw customer data, or authority to alter a version manifest.

---

# Testing Strategy

## Deployment Contract Tests

Tests validate deployment-unit, target, assignment, readiness, activation, suspension, withdrawal, and audit contracts; they also verify that overlays cannot alter immutable agent behavior.

## Integration Tests

Integration tests verify promotion, target eligibility, authorization, dependency checks, runtime resolution, channel eligibility, experiment continuity, observability records, and safe fallback when no assignment is eligible.

## Resilience and Security Tests

Tests simulate dependency revocation, failed readiness checks, partial rollout failure, invalid rollback target, tenant suspension, revoked approval, provider outage, stale assignment, worker restart, and emergency withdrawal. They must prove that no invalid version receives new work and that tenant boundaries remain intact.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Agent deployment-unit schema | Defines immutable version, target, readiness, assignment, and audit references | Agent Platform |
| Deployment management API schema | Defines eligibility, readiness, assignment, activation, suspension, rollback, withdrawal, and provenance operations | Agent Platform |
| Target and environment registry | Defines eligible environments, regions, channels, constraints, and owners | Agent Platform with Deployment and Security owners |
| Channel readiness matrix | Defines tenant/environment/channel prerequisites, ownership, evidence, and fallback path | Channel owners with Agent Platform approval |
| Readiness checklist and policy | Defines required evidence, approvals, dependencies, capacity, observability, and rollback checks | Agent, Operations, and Security owners |
| Rollout and assignment policy | Defines cohort selection, precedence, monitoring, stop conditions, and continuity rules | Agent Platform and tenant policy owner |
| Deployment threshold and sign-off policy | Defines baselines, success/stop thresholds, verification window, owners, and completion criteria | Agent and Operations owners |
| Deployment runbook | Defines activation, suspension, rollback, withdrawal, incident, and communication actions | Operations and Agent Platform |
| Deployment test suite | Validates contracts, integration, resilience, security, and tenant isolation | Agent Platform and Testing Platform |

---

# Anti-Patterns

## Deploying a Draft

Allowing a draft agent configuration to serve production traffic bypasses validation, approval, reproducibility, and rollback controls. Production deployment requires a released immutable version.

## Infrastructure Release Equals Agent Activation

A successful runtime or cluster deployment does not authorize a new agent behavior. Agent activation remains a separate tenant-scoped, evidence-based decision.

## Environment Overlay Changes Behavior

Using a deployment overlay to change instructions, tools, permissions, or dependencies creates an unversioned behavior fork. Material behavior changes require a new agent version.

## Global Default Assignment

An assignment with no explicit tenant or scope can expose a version across organizational boundaries. Every assignment must be tenant-scoped and policy-eligible.

## Rollback Without Current Check

Reactivating an older version without checking current security, dependency, tenant, and policy eligibility can restore a known unsafe behavior.

---

# Related Documents

| Document | Relationship |
|---|---|
| `04_AGENT_LIFECYCLE.md` | Defines the logical agent lifecycle; this model controls deployment eligibility of versions. |
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Resolves active assignments and executes eligible versions. |
| `21_AGENT_EVENT_INTEGRATION.md` | Carries governed deployment and withdrawal facts to authorized consumers. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Applies channel eligibility and delivery controls without changing agent intelligence. |
| `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent application of control-plane security, release evidence, and supply-chain boundaries. |
| `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent enforcement for deployment, activation, suspension, rollback, and approval actions. |
| `26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md` | Requires tenant-scoped deployments, assignments, and operational access. |
| `27_AGENT_VERSIONING_MODEL.md` | Defines immutable versions, manifest, compatibility, experiments, and rollback eligibility. |
| `12_DEPLOYMENT_PLATFORM` | Owns infrastructure deployment, environment operations, CI/CD, and runtime platform controls. |
| `11_OPERATIONS_PLATFORM` | Owns incident, release, support, and operational response processes. |
| `13_OBSERVABILITY_PLATFORM` | Owns telemetry infrastructure, dashboards, alerting, and retention. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Deployment Model architecture document. |
| 2.1 | 2026-08-05 | Added deployment transitions, concurrency controls, channel readiness, success/stop thresholds, sign-off, and deployment-management contract. |

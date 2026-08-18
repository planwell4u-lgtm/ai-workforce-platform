# 27_AGENT_VERSIONING_MODEL

**Version:** 2.2  
**Status:** Approved  
**Phase:** Agent Platform

---

# Overview

This document defines how the Agent Platform versions, validates, publishes, activates, compares, rolls back, retires, and audits agent definitions.

An agent version is an immutable, tenant-scoped release of the configuration that determines how an Agent Brain behaves. Versioning makes agent change deliberate and recoverable across every supported channel while preserving the **One Brain, Multi-Channel** principle.

---

# Purpose

The purpose of the Agent Versioning Model is to prevent uncontrolled changes to agent behavior. It enables teams to evolve instructions, capabilities, policies, model eligibility, tool assignments, knowledge/memory access settings, and channel behavior through reviewable versions rather than editing a live agent in place.

It provides a stable contract between agent design, runtime execution, evaluation, deployment, observability, and governance.

---

# Objectives

The Agent Versioning Model must:

- Make every executable agent definition immutable, identifiable, and reproducible.
- Separate draft design work from published and active production versions.
- Ensure a version applies consistently across channels unless an approved channel policy requires otherwise.
- Validate compatibility with capabilities, tools, workflows, policies, models, knowledge, and memory before activation.
- Support controlled rollout, comparison, rollback, retirement, and audit.
- Preserve tenant isolation and prevent one tenant’s version from affecting another.
- Allow runtime executions to identify the exact agent version and dependencies used.
- Avoid coupling agent-version semantics to a deployment tool, model provider, or source-control system.

---

# Scope

This document defines:

- Agent definition, version, revision, release, and activation concepts.
- Version lifecycle, immutability, compatibility, validation, promotion, rollback, and retirement rules.
- The version manifest and references to versioned dependencies.
- Tenant scope, runtime resolution, experimentation, audit, and testing requirements.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Runtime worker release, infrastructure rollout, environments, and CI/CD | `28_AGENT_DEPLOYMENT_MODEL.md` and Deployment Platform |
| Event schema evolution and broker compatibility | `21_AGENT_EVENT_INTEGRATION.md` |
| Tool contract versioning and connector implementation | `15_AGENT_TOOL_SYSTEM.md`, `16_AGENT_TOOL_EXECUTION_MODEL.md`, and Integration Platform |
| Knowledge document or memory-record versioning | Knowledge Platform and Memory Platform |
| Tenant authorization, approval, and role policy | `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md`, `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md`, and Security Platform |
| Channel-provider configuration or protocol versions | `22_AGENT_MULTI_CHANNEL_MODEL.md` and relevant Channel Platform |
| Source-code branching, package versioning, or artifact build processes | Engineering and Deployment Platforms |

---

# Core Concepts

## Agent Definition

An **agent definition** is the tenant-scoped logical identity of an Agent Brain. It has a stable `agentId` and represents the business role an organization intends the agent to perform.

## Agent Version

An **agent version** is an immutable, executable snapshot of that agent definition. It has a unique `agentVersionId`, a human-readable version label, a manifest, lifecycle state, dependency references, and audit metadata.

## Draft Revision

A **draft revision** is mutable design work that has not been published. Drafts are never executable in a production runtime and do not alter an active version.

## Release and Activation

A **release** is a validated published version approved for an environment. **Activation** assigns one eligible released version as the default version for a tenant, agent, and environment. Release does not automatically mean activation.

## Version Manifest

The **version manifest** is the complete, immutable record of the agent configuration and the exact approved dependency references needed to reproduce behavior within the documented limits of external systems.

---

# Versioning Principles

## Immutable Executable Versions

Once published, an agent version cannot be edited. A change creates a new draft and, after validation and approval, a new version. Corrections to metadata may be recorded as auditable annotations but cannot change executable behavior.

## One Versioned Brain Across Channels

The active agent version is resolved centrally by the Agent Platform. Voice, chat, messaging, email, and API channels invoke the same approved Agent Brain. Channel-specific presentation rules may adapt delivery but cannot silently select different intelligence, instructions, or permissions.

## Explicit Dependency References

The manifest uses explicit approved references to dependent capabilities, tools, workflows, policies, model configurations, knowledge access profiles, memory access profiles, and channel policy profiles. Mutable “latest” references are prohibited for executable production versions.

## Safe Evolution

Additive, compatible changes are preferred. A change that can affect security, authorization, tenant scope, data classification, tool behavior, workflow side effects, model eligibility, channel delivery, or user-visible commitments requires elevated validation and approval.

## Reproducibility and Traceability

Every material execution records the resolved `agentId`, `agentVersionId`, manifest digest, relevant dependency references, environment, tenant, and policy decision references. Reproducibility means the platform can explain the approved configuration used; it does not promise deterministic model output.

---

# Version Manifest

```text
Agent Version Manifest
|
+-- agentId / agentVersionId / version label
+-- tenantId / environment / lifecycle state
+-- identity, role, and approved purpose
+-- instruction and persona references
+-- capability and policy references
+-- approved model-configuration eligibility reference
+-- tool and workflow assignment references
+-- knowledge and memory access-profile references
+-- channel behavior and delivery-policy references
+-- security classification and risk profile
+-- compatibility declarations
+-- manifest digest / createdBy / createdAt / approval references
```

The manifest stores references to sensitive material rather than duplicating secrets, raw documents, transcripts, credentials, private reasoning, or unbounded data. Every referenced dependency must be tenant-eligible, active, and authorized before a version can be released or executed.

---

# Version Lifecycle

```text
Draft
    -> Validated
    -> Reviewed
    -> Released
    -> Active
    -> Superseded
    -> Retired
    -> Archived
```

## Draft

Draft revisions may be edited by authorized designers within tenant scope. They are clearly separated from production versions and can use controlled preview environments only.

## Validation and Review

Validation checks manifest completeness, schema validity, tenant eligibility, dependency availability, permission boundaries, policy compatibility, channel applicability, testing evidence, and migration requirements. Review confirms business ownership, risk, approval, and release readiness.

## Release and Activation

A released version is immutable and eligible for controlled deployment. Activation assigns it to an environment and traffic scope after required approvals. Only one default active version is selected for an agent within a tenant/environment, though controlled experiment assignments may resolve alternative eligible versions.

## Supersession, Retirement, and Archive

A new active version supersedes the prior default but does not erase it. Superseded versions remain available for audit, execution correlation, and approved rollback until retirement policy permits removal. Retired versions cannot be newly activated; archived history remains subject to retention and access policy.

## Version Labels

Every version has an immutable system identifier and a human-readable semantic label in the form `major.minor.patch`.

- **Major**: changes agent purpose, security posture, authority, externally visible business contract, or other behavior requiring an explicit migration or reapproval.
- **Minor**: adds compatible approved capability or behavior without invalidating the documented agent purpose or supported integrations.
- **Patch**: corrects or clarifies behavior without intentionally changing the approved purpose, permissions, dependency contract, or user-facing commitment.

The version label communicates review intent; the manifest digest remains the authoritative identity of the exact executable configuration.

---

# Compatibility and Change Classification

## Compatible Change

A change is compatible when it does not invalidate approved dependency contracts, security boundaries, tenant eligibility, required evaluations, or user-facing behavior assumptions. Examples may include clarifying an internal instruction, adding an optional safe capability behind policy, or improving an inactive draft.

## Material Change

A material change requires a new version and increased review when it changes any of the following:

- Agent purpose, identity, persona, or instruction authority.
- Capability, tool, workflow, integration, or external-action eligibility.
- Permission, delegation, approval, data classification, or tenant boundary.
- Model provider eligibility, model configuration, or fallback policy.
- Knowledge or memory access profile, retention behavior, or source scope.
- Channel delivery behavior, consent requirement, or user-visible commitment.
- Evaluation criteria, safety control, or regulatory obligation.

## Breaking Dependency Change

When a referenced dependency is retired, incompatible, revoked, or no longer tenant-eligible, the affected version cannot be newly activated or executed without an approved replacement version or explicit controlled mitigation. The platform must identify affected active versions before accepting a breaking dependency change.

## Change-Impact Matrix

| Change type | New version | Required control before release |
|---|---|---|
| Draft wording or metadata correction with no executable effect | Not necessarily | Draft review and audit record |
| Instruction, persona, capability, knowledge, memory, or channel-policy change | Yes | Validation, evaluation, compatibility review |
| Tool, workflow, integration, model, or delivery behavior change | Yes | Security/permission review, regression tests, approval by risk |
| Tenant scope, classification, approval, delegation, or security-control change | Yes | Elevated security review and explicit authorization approval |
| Material purpose, high-risk action, or externally visible commitment change | Yes, normally major | Impact assessment, human approval, controlled rollout plan |
| Dependency retirement or incompatibility | Replacement version or controlled mitigation | Migration plan, affected-version inventory, rollback review |

The release policy may impose additional tenant or regulatory controls. No matrix entry permits a draft change to bypass the normal authorization, validation, or audit boundary.

## Dependency Migration

When a dependency is deprecated, the dependency owner publishes compatibility, replacement, support-end date, and migration guidance. The Agent Platform maintains an affected-version inventory and alerts the owning tenant or operator before support ends.

Migration creates a new agent version referencing the approved replacement. It is evaluated and released through the normal lifecycle; direct substitution inside a published manifest is prohibited. Emergency mitigation may suspend or block an unsafe version, but it must not silently alter its recorded configuration.

---

# Runtime Resolution and Execution

## Resolution

For each authorized execution, the Runtime resolves the active agent version using tenant, agent identity, environment, assignment policy, experiment policy, channel applicability, and current authorization. It validates that the resolved version is released, active or experiment-eligible, unexpired, compatible, and tenant-bound.

## Execution Pinning

An execution pins its resolved agent version and manifest digest for its lifetime. A later activation or rollback does not silently alter an in-flight execution. New executions resolve the then-current eligible version.

## Background and Event-Triggered Work

Scheduled, workflow, and event-triggered work records either a pinned version reference or a documented resolution policy. High-risk or delayed work should use an explicit pinned version to avoid unreviewed behavior drift. Resuming work always revalidates current authorization, tenant state, and dependency eligibility.

---

# Rollout, Experimentation, and Rollback

## Controlled Rollout

Activation supports controlled scopes such as internal preview, named tenant cohort, channel-eligible cohort, or bounded percentage assignment. A rollout policy records scope, entry criteria, monitoring signals, success criteria, stop conditions, owner, and rollback target.

Rollout assignment must not change tenant scope or bypass consent, permission, classification, or channel constraints. An experiment is not permission to expose unapproved behavior to users.

## Comparison and Evaluation

Version comparison uses approved evaluation criteria, test suites, safety signals, business outcomes, and observability data. Comparisons must protect tenant data and avoid using raw sensitive conversation content outside authorized evaluation processes.

## Experiment Continuity

An experiment assignment is recorded for a defined tenant, cohort, and continuity window. When a user interaction is part of an active conversation or session, the platform pins that interaction to its assigned eligible version for the approved window unless a safety, security, withdrawal, or explicit migration policy requires reassignment.

The assignment contains the version, policy, start and expiry, cohort basis, and correlation references. It must not override tenant scope, permission, consent, classification, or a version’s retirement or revocation.

## Rollback

Rollback changes the default assignment for future eligible executions to a prior released version. It is a controlled activation change with an audit reason, scope, authorization, dependency check, and communication/incident process where appropriate.

Rollback does not undo external actions already taken, mutate completed execution records, or reactivate a version that is retired, revoked, insecure, or incompatible.

---

# Security, Tenant, and Governance Controls

Every draft, manifest, version, release, activation, experiment, rollback, and retirement is tenant-scoped and authorization-controlled. Platform templates are immutable shared artifacts; a tenant adopts them into a tenant-owned version before execution.

Only authorized roles may create drafts, modify a draft, validate, approve, release, activate, rollback, retire, or inspect protected version history. High-risk changes require the approval and separation-of-duties controls defined by the Permission Model.

Version history and manifests do not contain secrets, credentials, hidden instructions, private model reasoning, or unrestricted customer data. Access to versioned references is evaluated separately at retrieval time.

## Retention and Provenance

Drafts, published manifests, validation evidence, approvals, rollout assignments, experiment results, activation history, rollback records, and execution-version provenance are retained according to tenant agreement, classification, audit, security, and operational-recovery policy.

Superseded versions remain retrievable only through controlled access for the approved retention period. Retiring or deleting a version record does not remove execution audit references that must be retained; those references are minimized or anonymized according to the owning retention policy.

---

# Observability and Audit

The platform records:

- Agent, version, manifest digest, tenant, environment, and lifecycle state.
- Creator, reviewer, approver, activator, rollback actor, timestamps, and reason.
- Dependency references, compatibility result, validation evidence, and policy versions.
- Rollout scope, experiment assignment, evaluation result, stop condition, and outcome.
- Resolved version for every material execution, workflow, tool action, event reaction, and user-facing delivery.

Metrics include draft-to-release lead time, validation failures, activation rate, rollback frequency, version adoption, execution/error rate by version, safety/policy denials by version, evaluation results, and stale or incompatible dependency findings.

---

# Testing Strategy

## Contract Tests

Contract tests validate manifest schema, immutable identifiers, lifecycle transitions, dependency references, compatibility declarations, and runtime-resolution responses.

## Integration Tests

Integration tests verify tenant-scoped version selection, channel-consistent resolution, execution pinning, dependency validation, controlled rollout, rollback, event-triggered work, and audit correlation.

## Security and Resilience Tests

Tests verify unauthorized draft changes, cross-tenant version access, mutable dependency substitution, stale activation, revoked dependency handling, rollback under incident conditions, partial rollout failure, and worker restart during resolution.

## Evaluation Tests

Every candidate release is evaluated against the approved functional, safety, security, tool, workflow, channel, and regression criteria appropriate to its risk. Failed or incomplete required evaluation blocks release or activation.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Agent-version manifest schema | Machine-readable immutable version contract and compatibility fields | Agent Platform |
| Version-management API contract | Defines draft, validate, release, activate, compare, rollback, retire, and provenance operations | Agent Platform |
| Dependency compatibility registry | Tracks versioned capability, tool, workflow, policy, model, and profile eligibility | Agent Platform with dependent owners |
| Change-impact matrix | Maps configuration changes to version labels, evidence, approval, and rollout requirements | Agent Platform and Security owner |
| Dependency migration register | Tracks deprecation, affected versions, replacement, support end, and migration status | Agent Platform with dependent owners |
| Release and activation policy | Defines validation, approvals, rollout scopes, stop conditions, and rollback authority | Agent Platform and tenant policy owner |
| Version retention policy | Defines lifecycle-history, evidence, provenance, archival, and deletion requirements | Agent Platform with Data and Security owners |
| Version evaluation suite | Validates functional, safety, security, channel, and regression expectations | Agent Platform and Testing Platform |
| Rollback runbook | Defines authorization, scope, dependency checks, monitoring, and incident actions | Operations and Agent Platform |
| Version audit report | Provides release, activation, experiment, execution, and retirement traceability | Agent Platform |

---

# Anti-Patterns

## Editing the Active Agent In Place

Live edits destroy reproducibility and make rollback uncertain. All executable behavior changes require a new immutable version.

## Latest Dependency Reference

Binding a production agent to an unpinned “latest” tool, policy, model, or workflow allows behavior to change without review. Use explicit approved dependency references.

## Channel-Specific Brain Fork

Creating separate agent versions per channel duplicates intelligence and violates One Brain, Multi-Channel. Channel adaptation belongs to channel policy and delivery layers unless a new agent purpose is intentionally created.

## Rollback Without Eligibility Check

Reactivating a historical version without checking revoked credentials, retired tools, current permissions, security findings, or dependency compatibility can reintroduce risk.

## Version Number as Authorization

Knowing or selecting a version identifier does not authorize its use. Runtime resolution and activation remain tenant- and policy-scoped.

---

# Related Documents

| Document | Relationship |
|---|---|
| `01_AGENT_PLATFORM_OVERVIEW.md` | Defines the Agent Platform’s overall responsibility and logical agent identity. |
| `04_AGENT_LIFECYCLE.md` | Defines agent lifecycle; this model versions its executable definitions. |
| `06_AGENT_CONFIGURATION_MODEL.md` | Defines configurable agent elements captured by the version manifest. |
| `07_AGENT_RUNTIME_ARCHITECTURE.md` | Resolves and pins an eligible version for execution. |
| `08_AGENT_EXECUTION_ENGINE.md` | Executes with the resolved version and records version correlation. |
| `12_AGENT_INSTRUCTION_SYSTEM.md` | Governs versioned instruction references and authority. |
| `14_AGENT_CAPABILITY_MODEL.md` | Defines capabilities referenced and validated by a version. |
| `15_AGENT_TOOL_SYSTEM.md` | Defines tools whose eligible assignments are versioned. |
| `20A_AGENT_WORKFLOW_INTEGRATION_REWRITE_DRAFT.md` | Defines workflows referenced by a versioned agent configuration. |
| `22_AGENT_MULTI_CHANNEL_MODEL.md` | Adapts output by channel without duplicating agent intelligence. |
| `24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent application of control-plane security and provider-assurance requirements. |
| `25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT.md` | Defines Agent enforcement of authorization for draft, release, activation, and rollback actions. |
| `26A_AGENT_TENANT_BOUNDARY_REWRITE_DRAFT.md` | Requires tenant-scoped version ownership, activation, and execution. |
| `28_AGENT_DEPLOYMENT_MODEL.md` | Deploys versioned agent configurations through controlled environments. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-05 | Initial Agent Versioning Model architecture document. |
| 2.1 | 2026-08-05 | Added semantic version labels, change-impact rules, dependency migration, experiment continuity, retention, and version-management contract requirements. |

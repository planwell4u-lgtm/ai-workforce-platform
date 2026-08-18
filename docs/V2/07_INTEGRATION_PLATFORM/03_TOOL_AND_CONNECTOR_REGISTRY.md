# 03_TOOL_AND_CONNECTOR_REGISTRY

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the Integration registry for connectors, tools, capabilities, contracts, profiles, availability, lifecycle, and adoption evidence.

The registry describes what an approved Integration adapter can do. It does not grant access, hold broad secrets, select an action for an Agent, or permit an external effect.

---

# Purpose

The registry gives the platform one provider-neutral source for discovering and validating Integration capabilities before an action is requested. It prevents provider SDK methods, ad-hoc tools, unversioned schemas, or configuration flags from becoming hidden public contracts.

---

# Objectives

The registry must:

- Define stable Connector, Tool, Capability, contract, profile, and lifecycle metadata.
- Publish only bounded, reviewed, versioned capabilities with explicit inputs, outputs, effects, constraints, and ownership.
- Keep capability discovery separate from action authorization, approval, credential delegation, and execution.
- Support tenant/environment-scoped availability without exposing provider accounts, credentials, or other tenants.
- Make compatibility, deprecation, migration, rollback, and removal explicit.
- Provide evidence for conformance, security, privacy, tenant isolation, observability, and test readiness.

---

# Scope

This document defines the logical registry model, lifecycle, discovery rules, contract/version policy, availability representation, onboarding, retirement, and audit requirements.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Agent reasoning, tool selection, or business intent | 02_AGENT_PLATFORM |
| Canonical Conversation work, routing, handoff, or participant communication | 03_CONVERSATION_PLATFORM |
| Tenant/membership/entitlement/configuration source of truth | 16_PLATFORM_FOUNDATION |
| Enterprise authorization, credential vault, secrets, cryptography, or compliance policy | 09_SECURITY_PLATFORM |
| Connector credential delegation | 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md |
| Current action authorization or approval | 05_ACTION_AUTHORIZATION_AND_APPROVAL.md |
| Dispatch, idempotency, retries, workflow execution, callbacks, or reconciliation | 06–09 and 13 Integration documents |
| Physical registry storage, search infrastructure, or deployment tooling | 08_DATA_PLATFORM and 12_DEPLOYMENT_PLATFORM |

---

# Registry Principles

## Discovery Is Not Permission

Registry visibility means a capability exists for a bounded evaluation scope. It does not grant a principal or Agent permission to invoke it, see its provider account, access a credential, or perform an effect.

## Capability Is Not Provider Method

A capability is a platform-defined, provider-neutral operation such as `crm.case.create` or `calendar.event.create`. Adapter methods, SDK types, provider IDs, headers, and raw response shapes remain internal.

## Contract Before Enablement

Every capability has an explicit request schema, output/outcome schema, effect class, error vocabulary, idempotency expectation, data-egress representation, and compatibility policy before it can be enabled.

## Availability Is Current and Scoped

Availability is evaluated using trusted tenant/environment, entitlement, connector/profile, configuration, provider health, policy, and lifecycle facts. A cached listing or prior success cannot make a capability available for a new action.

## Safe Retirement Beats Hidden Breakage

Deprecated or retired capabilities remain discoverable only through approved historical/audit representations. New selection stops before removal, and in-flight work follows an explicit migration, reconciliation, or safe-stop plan.

---

# Registry Entities

| Entity | Meaning | Required metadata |
|---|---|---|
| `ConnectorDefinition` | Provider-neutral adapter family for one external system. | Owner, adapter/version, supported provider profile classes, trust/data classification, lifecycle. |
| `ToolDefinition` | A named integration surface available to Agent selection through approved contracts. | Tool name, owner, allowed capabilities, selection constraints, contract compatibility. |
| `CapabilityDefinition` | One bounded external operation exposed by a connector. | Effect class, request/result schemas, parameter constraints, idempotency, authorization/approval class, egress, outcome vocabulary. |
| `CapabilityVersion` | Immutable published contract and behavior version. | Semantic version, compatibility, effective period, migration/rollback, conformance evidence. |
| `ConnectorProfile` | Approved configuration/profile class used to determine eligibility. | Tenant/environment applicability, provider role, region/residency, limits, feature flags, health, lifecycle. |
| `AvailabilityRecord` | Current evaluated eligibility result for a capability/profile scope. | Scope, reason category, policy/configuration version, expiry, correlation, no credential disclosure. |
| `DeprecationRecord` | Notice and controlled transition for a connector/capability version. | Replacement, effective date, affected profiles, in-flight treatment, owner, communication/audit reference. |

Provider accounts, OAuth grants, API keys, raw configuration, customer records, and secret references are never registry entries.

---

# Capability Contract

Each published capability declares:

| Contract area | Requirement |
|---|---|
| Identity | Stable tool/capability/version IDs and owning Integration team. |
| Intent boundary | Permitted business operation, effect class, prohibited use, and whether approval is required. |
| Input | Versioned minimal schema, validation rules, sensitive-field representation, target constraints, and defaults prohibited unless documented. |
| Output | Provider-neutral result, normalized outcome/error categories, protected evidence references, and uncertainty behavior. |
| Scope | Tenant/environment, subject/purpose, entitlement, connector/profile, region/residency, classification, and egress requirements. |
| Execution | Idempotency class, cancellation, rate/cost limits, timeout, retry, fallback, compensation, and reconciliation requirements. |
| Governance | Security/privacy/tenant review, test/conformance evidence, observability/audit requirements, owner, and lifecycle. |

A capability may expose a read, write, delete, external-notification, financial, administrative, or other effect class, but it cannot hide a materially different effect behind a generic name or optional parameter.

---

# Lifecycle

~~~text
Proposed -> Evaluating -> Registered -> Enabled -> Restricted -> Deprecated -> Retired
                         |                 |              |
                         +-> Rejected      +-> Suspended   +-> Removed from selection
~~~

| State | Meaning |
|---|---|
| `Proposed` | A potential connector or capability is recorded; not selectable. |
| `Evaluating` | Security, data, tenant, conformance, operational, and contract evidence is being assessed. |
| `Registered` | Contract is documented but unavailable for production selection. |
| `Enabled` | A current scoped profile may expose the capability, subject to action guard evaluation. |
| `Restricted` | Only specified tenant/environment/operation/profile use is eligible. |
| `Suspended` | New use is blocked because of incident, policy, health, or lifecycle condition. |
| `Deprecated` | New selection is being phased out with a documented replacement/exit path. |
| `Retired` | No new or resumed use; retained evidence follows policy. |
| `Rejected` | Not eligible; rationale is retained. |

Only an approved onboarding process can move a capability to `Enabled` or `Restricted`. Action authorization is still evaluated later for each requested effect.

---

# Discovery and Availability

Discovery responses show only the minimal capability metadata authorized for the caller's trusted tenant/environment, role, purpose, and representation. They exclude credentials, provider account details, other tenants, raw policy inputs, internal health diagnostics, and hidden capabilities.

Before an Agent receives a selectable capability, the registry confirms its contract version, owner, lifecycle, tenant/environment profile, entitlement/configuration, region/residency, feature state, and broad capability eligibility. A later action request re-evaluates all current authorization, approval, credential, target, and policy conditions.

An unavailable response uses normalized categories such as `NotEnabled`, `Restricted`, `Suspended`, `Deprecated`, `Incompatible`, or `Unavailable`; it never reveals whether another tenant owns a connector or why an external account exists.

---

# Versioning and Compatibility

Capability and schema versions use a documented compatibility policy. Additive changes are preferred. Any change to effect class, required approval, authorization semantics, sensitive data representation, target interpretation, idempotency behavior, outcome meaning, privacy classification, provider mapping, or lifecycle requires a new version and compatibility assessment.

An older version remains selectable only for its documented support window and profile scope. Migration records identify source/target versions, contract differences, tenant/profile impact, in-flight action treatment, rollback, conformance tests, and owner approval. A provider upgrade never silently changes a published platform capability.

---

# Onboarding, Enablement, and Exit

Before registration or enablement, the owner must provide:

1. bounded Connector and Capability definitions with provider-neutral contracts;
2. Security, privacy, data-egress, tenant, residency, and credential-delegation assessment;
3. action effect, approval, idempotency, cancellation, compensation, and uncertainty classification;
4. adapter conformance, contract compatibility, adversarial, reliability, observability, and test evidence;
5. profile/configuration, rate/cost, support, incident, rollout, rollback, and exit plan; and
6. Decision Log evidence when the connector or capability introduces a material long-lived decision.

Retirement first prevents new selection, then safely handles active actions/workflows, revokes or rotates applicable grants through Security controls, preserves required audit evidence, migrates eligible configuration, and reconciles uncertain provider effects. Removing a registry entry is never a substitute for retirement.

---

# Platform Foundation and Channel Boundaries

Platform Foundation owns tenant, membership, entitlement, configuration, and API-edge facts. The registry consumes those facts to evaluate a scoped listing; it does not create tenants, grants, entitlements, or configuration authority.

Voice and Digital Channel Platforms own participant transport and delivery. Registry capabilities may support approved business-system actions for a channel journey but cannot register themselves as a channel, choose a delivery route, or use availability as proof of participant contact.

---

# Security and Audit Requirements

Registry changes—including connector onboarding, capability enablement, profile change, contract version, restriction, suspension, deprecation, and retirement—record actor/service, scope, reason, evidence, effective time, approval, correlation, and resulting lifecycle state.

The registry stores only protected references to credentials, provider accounts, sensitive parameters, and external resources. Its audit and operational events use normalized categories and protected IDs, not raw secrets, tokens, payloads, or tenant-unscoped data.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Connector/capability registry schema | Defines entities, lifecycle, scope, visibility, versioning, and protected references. | Integration with Data and Security owners |
| Capability contract catalog | Defines input/output/effect/guard/egress/idempotency/compatibility requirements. | Integration with Agent, Conversation, and Testing owners |
| Availability evaluation policy | Defines trusted inputs, result categories, expiry, caching limits, and re-evaluation. | Integration with Platform Foundation and Security owners |
| Onboarding and retirement checklist | Defines review, conformance, rollout, suspension, migration, exit, and audit evidence. | Integration with Operations, Security, Data, and Testing owners |
| Registry conformance suite | Verifies schema, lifecycle, visibility, compatibility, isolation, privacy, and audit behavior. | Integration with Testing and Security owners |

---

# Anti-Patterns

## Registry Listing Grants Tool Access

Discovery is not authorization. Every action still needs current guard, approval, credential, target, and policy evaluation.

## Provider SDK Method Is a Public Tool

Provider methods are adapter details. A published capability has an independently versioned, bounded platform contract.

## Capability Version Changes In Place

Material behavior changes publish a new version with compatibility and migration evidence; they do not silently alter active consumers.

## Secret or Provider Account in Registry Metadata

Credentials and provider-account details stay in Security-governed references and protected adapters, never in discoverable registry content.

## Retirement Means Delete the Row

Retirement is a governed lifecycle and evidence process, not an untracked removal that strands actions, audits, or provider effects.

---

# Related Documents

| Document | Relationship |
|---|---|
| 01_INTEGRATION_PLATFORM_ARCHITECTURE.md | Defines the governed external-action boundary. |
| 02_INTEGRATION_DOMAIN_MODEL.md | Defines Connector, Capability, and action-domain records. |
| 04_CONNECTOR_AUTHENTICATION_AND_CREDENTIAL_DELEGATION.md | Defines credential scope and grants excluded from registry metadata. |
| 05_ACTION_AUTHORIZATION_AND_APPROVAL.md | Defines per-action permission and approval beyond discovery. |
| 08_EXTERNAL_API_AND_MCP_BOUNDARY.md | Defines public tool/API/MCP exposure contracts. |
| 10_INTEGRATION_ACCESS_AND_TENANT_ISOLATION.md | Defines tenant and subject isolation controls. |
| 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md | Defines governance and accountability controls. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created the Tool and Connector Registry model for capability contracts, lifecycle, availability, versioning, and onboarding. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

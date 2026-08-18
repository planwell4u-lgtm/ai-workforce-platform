# 09_WEBHOOK_AND_EXTERNAL_EVENT_MODEL

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines how Integration Platform receives, validates, normalizes, deduplicates, orders, correlates, retains, and reconciles external callbacks, webhooks, and provider events.

An inbound event is untrusted evidence. It is never an implicit command, authorization, tenant selector, credential grant, canonical Conversation event, or permission to execute another external effect.

---

# Purpose

The model prevents forged, stale, replayed, misrouted, cross-tenant, duplicate, out-of-order, schema-incompatible, or overbroad provider events from changing Integration action evidence or triggering unsafe work.

---

# Objectives

- Validate source authenticity, integrity, freshness, replay, schema/version, endpoint, tenant/resource, and operation correlation.
- Preserve raw provider payloads only in protected evidence paths; publish provider-neutral normalized facts.
- Deduplicate and order events without assuming provider timestamps or IDs are globally authoritative.
- Reconcile contradictory, late, missing, or uncertain external evidence safely.
- Apply data minimization, tenant isolation, rate/size limits, audit, observability, and incident handling.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Enterprise signature/key/secret standards, incident command, or compliance policy | 09_SECURITY_PLATFORM |
| Connector registration, credential delegation, action approval, execution, or workflow design | Integration documents 03–08 |
| Canonical Conversation event meaning, participant routing, or notification | 03_CONVERSATION_PLATFORM |
| API-edge infrastructure or tenant control plane | 16_PLATFORM_FOUNDATION |
| Provider-specific carrier/channel event behavior | Relevant Voice or Digital Channel document |
| Physical event storage, broker, or queue implementation | 08_DATA_PLATFORM and Operations Platform |

---

# Trust Principles

## Signed Is Not Sufficient

A valid signature or source assertion is necessary only where the provider supports it. The event must also match the current connector, tenant/environment, endpoint, account/resource, action/workflow correlation, schema, freshness, ordering, and lifecycle.

## Event Is Evidence, Not Authority

An event may update protected Integration evidence or open reconciliation. It cannot create an ActionRequest, grant approval, reactivate a credential, select a tenant, alter canonical Conversation state, or launch a new effect without its own current guarded action.

## Unknown Means Quarantine

An unknown, ambiguous, malformed, stale, replayed, over-limit, wrong-scope, or contradictory event is rejected, quarantined, or reconciled. The system never guesses a resource binding or exposes target details in the response.

---

# Event Envelope

Each accepted normalized event includes:

- Integration event ID and schema version;
- trusted tenant/environment, connector/profile, provider account/resource, endpoint, and event-type category;
- protected provider event/reference IDs and source-validation evidence;
- received/observed time, freshness window, sequence/ordering evidence, replay/deduplication result;
- action/attempt/workflow/callback correlation and causation references when applicable;
- normalized outcome/state category, classification/representation restriction, and protected raw-evidence reference; and
- audit, incident, reconciliation, and trace references where required.

Provider raw payload, signature, headers, URL, token, direct identifier, and unredacted content stay in protected adapter/security evidence. They are never routine event-bus payload fields.

---

# Intake and Validation Flow

1. Accept only registered connector/provider endpoint paths through the approved API edge.
2. Apply size, media type, rate, source/network, schema, and parsing limits before expensive processing.
3. Validate signature/certificate/shared-secret or equivalent source assertion through Security-managed material.
4. Validate timestamp/freshness, nonce or provider event ID, replay window, endpoint/account/resource mapping, schema/contract version, and tenant/environment binding.
5. Resolve expected action/attempt/workflow correlation from trusted server-side records; provider-supplied IDs are evidence only.
6. Deduplicate and evaluate ordering/terminal-state consistency.
7. Store protected evidence, emit normalized fact, and either update allowed Integration evidence, open reconciliation, or quarantine/reject.

An acknowledgement response is protocol-specific and does not imply the event changed platform state.

---

# Deduplication and Ordering

| Condition | Required posture |
|---|---|
| Exact replay | Return safe acknowledgement where required; do not repeat processing/effect. |
| Duplicate with same normalized evidence | Record deduplication and retain prior result. |
| Duplicate with conflict | Quarantine/open reconciliation; do not overwrite prior evidence. |
| Out-of-order non-terminal event | Apply only if allowed by the mapped action/workflow state; otherwise retain evidence. |
| Late event after terminal result | Preserve protected evidence and reconcile only if it materially contradicts result. |
| Missing expected event | Do not infer success; use bounded poll/reconciliation if eligible. |

Provider sequence/timestamp values are scoped evidence with known clock/order limits, never global truth or authorization.

---

# Normalization and Effect Boundary

Adapters map provider events to categories such as `ExternalAccepted`, `ExternalInProgress`, `ExternalSucceeded`, `ExternalFailed`, `ExternalCancelled`, `ExternalNoEffect`, `ExternalRestricted`, `ExternalUncertain`, and `ExternalEventRejected`.

A normalized event may advance a permitted Integration attempt/workflow evidence state only after current correlation and lifecycle checks. It cannot communicate with a participant, set a Conversation result, create a business record, or invoke a follow-on connector action unless an independently authorized workflow step runs its current guard.

---

# Reconciliation and Incident Handling

Conflicting, delayed, missing, rejected-after-acknowledgement, wrong-tenant, or suspected forged events create a protected reconciliation or incident reference. Reconciliation compares action/idempotency/workflow state with trusted provider evidence and current policy to establish confirmed effect, no-effect, continued uncertainty, restriction, or escalation.

On credential compromise, signature failure spike, callback flood, cross-tenant attempt, schema abuse, or integrity failure, Integration restricts the affected endpoint/profile/account scope, preserves minimum evidence, alerts the responsible owners, and follows Security incident controls. It does not disable unrelated tenants or resume automatically after recovery.

---

# Platform Foundation and Channel Boundaries

Platform Foundation supplies API-edge, tenant, environment, entitlement, and configuration facts. Integration validates them at intake but never derives them from a callback URL, header, provider account, or event payload.

Voice and Digital Channel event streams remain their respective channel-domain evidence. An Integration webhook may correlate to an approved action but cannot become a channel-delivery or participant-identity authority.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Provider webhook contract catalog | Defines endpoint, source assertion, schemas, limits, correlation, outcome mapping, and retirement. | Integration with Security and Testing owners |
| Event validation/deduplication standard | Defines freshness, replay, order, conflict, quarantine, and audit rules. | Integration with Data, Security, and Operations owners |
| Normalization and reconciliation matrix | Defines provider event to Integration evidence mapping and uncertain/conflict handling. | Integration with Execution, Workflow, and Conversation owners |
| Callback abuse and incident runbook | Defines rate/size control, containment, escalation, recovery, and evidence. | Integration with Security and Operations owners |
| Webhook conformance suite | Proves forged/replayed/stale/out-of-order/wrong-tenant/schema-abuse safety. | Integration with Testing and Security owners |

---

# Anti-Patterns

## Valid Webhook Is a Command

It is validated evidence only; follow-on effects require a registered, current guarded action.

## Provider ID Selects Tenant

Tenant scope comes from trusted server-side binding and must be validated against provider/account/resource evidence.

## Retry the Callback by Repeating the Action

Event replay and external-effect execution have separate idempotency boundaries; never dispatch just because callback delivery is uncertain.

## Raw Payload on the Event Bus

Publish normalized, minimized facts and protected references; raw payloads remain in approved evidence storage.

---

# Related Documents

| Document | Relationship |
|---|---|
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines effect and outcome correlation. |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Defines callback-driven technical progression. |
| 08_EXTERNAL_API_AND_MCP_BOUNDARY.md | Defines public API boundary distinct from provider intake. |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines external trust and privacy controls. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines reconciliation and recovery. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created webhook and external-event model covering validation, normalization, ordering, replay, reconciliation, and incident handling. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

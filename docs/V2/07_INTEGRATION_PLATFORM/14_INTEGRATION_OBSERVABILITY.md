# 14_INTEGRATION_OBSERVABILITY

**Version:** 1.1  
**Status:** Approved  
**Owner:** Integration Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines Integration-domain metrics, traces, structured logs, events, audit evidence, dashboards, alerts, service objectives, diagnostics, and data-quality controls.

Integration owns which connector/action/workflow/callback/outcome signals must be observable. Observability Platform owns shared telemetry collection, storage, query, alert, dashboard, and incident tooling.

---

# Purpose

Observability makes external-effect behavior visible without exposing raw provider payloads, credentials, sensitive parameters, unscoped external identifiers, or cross-tenant data.

---

# Objectives

- Measure safe action outcomes, not only provider uptime or API success.
- Observe registry, grants, authorization, approval, execution, workflows, callbacks, tenant scope, security, reconciliation, and recovery.
- Separate operational telemetry, audit evidence, protected provider data, and business analytics.
- Provide tenant-safe alerts, dashboards, SLOs, diagnostics, cost/capacity signals, and data-quality evidence.
- Preserve correlation across Integration, Agent, Conversation, Security, Data, and providers without granting cross-platform access.

---

# This Document Does Not Define

| Topic | Owner |
|---|---|
| Telemetry infrastructure, SIEM, alert delivery, dashboard hosting, or incident tooling | 13_OBSERVABILITY_PLATFORM and 11_OPERATIONS_PLATFORM |
| Canonical business/conversation outcomes, participant analytics, or Agent evaluation | Conversation, Agent, and business owners |
| Connector/action/workflow/security/tenant behavior itself | Integration documents 03–13 |
| Retention/deletion/privacy/compliance policy or audit infrastructure | Data and Security Platforms |

---

# Principles

## Observe Outcome, Not Component Health

Provider health or HTTP success does not prove a guarded external effect succeeded. Signals distinguish confirmed success/failure/no-effect from cancellation, restriction, degradation, deferral, and uncertainty.

## Correlation Is Scoped Evidence

Action, workflow, provider, callback, trace, and audit references connect work only inside trusted tenant/environment and current authorization. They are never read credentials or cross-tenant join keys.

## Telemetry Is Not Content or Audit Storage

Metrics/traces/logs support diagnosis; audit records accountable governance; provider payloads and sensitive artifacts remain protected evidence. Each follows its own access and lifecycle controls.

## Data Quality Is Observable

Missing, late, duplicate, mis-scoped, or incompatible signals create an explicit data-quality condition; dashboards/SLOs never present them as healthy zeroes.

---

# Signal Envelope and Telemetry Classes

Every signal includes schema/source/deployment version; trusted tenant/environment and tenant-safe partition; connector/capability/profile/adapter category; action/attempt/workflow/callback protected references; operation/outcome/failure category; correlation/causation/idempotency/trace; time/clock-quality; classification/representation; and audit/incident link where required.

| Class | Purpose | Control |
|---|---|---|
| Metrics | Aggregated availability, latency, volume, outcome, capacity, cost, and quality. | Tenant-safe dimensions; no raw content. |
| Traces | Bounded causal path across services/providers. | Opaque IDs and allowlisted attributes. |
| Structured logs | Diagnostic decisions/errors/state transitions. | Redaction and no secret/raw-payload logging. |
| Operational events | Versioned Integration facts for approved consumers. | Facts, not commands/access grants. |
| Audit evidence | Accountable action/governance/security lifecycle. | Durable, purpose-bound protected record. |
| Provider evidence | Raw response/callback details where needed. | Protected adapter/evidence path, not telemetry. |

---

# Metric and SLO Catalog

| Area | Required measures |
|---|---|
| Capability/connector | Availability, version adoption, enablement/restriction/suspension, configuration drift. |
| Credential/grant | Lease/grant validation, expiry/rotation/revocation, account/profile mismatch. |
| Authorization/approval | Guard success/denial/restriction/expiry, approval wait/decision, separation/limit enforcement. |
| Execution | Request-to-dispatch/outcome latency, confirmed result, idempotency suppression, retry/fallback/circuit. |
| Workflow/callback | Run/step/wait age, callback validation/replay/order, deadline, compensation, reconciliation age. |
| Security/tenant | Source/egress/injection/abuse category, scope denial/ambiguity/staleness, incident containment. |
| Provider/capacity/cost | Provider role latency/error/quota, tenant-safe rate/cost, bulkhead and backpressure. |
| Data quality | Missing/late/duplicate/schema/clock/correlation/redaction/sampling failure. |

Each metric/SLO defines source lineage, numerator/denominator, unit/window, dimensions, exclusions, data-quality condition, owner, target/alert, privacy classification, and version. SLOs do not justify relaxing action, tenant, approval, security, or egress controls.

---

# Dashboards, Alerts, and Diagnostics

Operations dashboards show authorized aggregate connector/action/workflow/callback/reconciliation/capacity health. Tenant views show only that tenant's permitted configuration, outcomes, usage, and restrictions. Security/governance views show authorized audit, source, egress, credential, and incident evidence. Provider views remain restricted to approved operations/security roles.

Alerts cover participant/business-impacting action degradation, uncertain-effect backlog, callback rejection/replay, credential/rotation failure, authorization/approval anomalies, tenant mismatch, egress/security anomaly, rate/cost/circuit pressure, workflow deadline, reconciliation age, and telemetry/audit data-quality loss. Alerts never contact participants or change canonical Conversation state automatically.

Diagnostics require current purpose, tenant, role, representation, expiry, and audit. Raw provider evidence or sensitive action data uses a separate protected evidence path.

---

# Privacy, Tenant, and Testing Controls

Telemetry excludes credentials, tokens, raw request/response/callback payloads, full sensitive parameters, direct participant identifiers, unrestricted provider IDs, and detailed policy data. Sampling, cardinality, aggregation, query, export, retention, and drill-down obey Security/Data/tenant controls.

Tests validate schema/version, scope, redaction, metric calculation, SLO/data quality, alert routing, dashboard audience, trace injection, provider payload leakage, cross-tenant query, cardinality abuse, pipeline outage, and audit completeness. Synthetic probes use dedicated tenant/accounts/endpoints and cannot create real external effects.

---

# Required Implementation Artifacts

| Artifact | Purpose | Owner |
|---|---|---|
| Integration signal/metric catalog | Defines outcomes, dimensions, lineage, SLOs, privacy, and ownership. | Integration with Observability and Operations owners |
| Trace/log/redaction/sampling standard | Defines correlation, allowed attributes, cardinality, privacy, quality, and diagnostics. | Integration with Security and Observability owners |
| Dashboard/alert/synthetic catalog | Defines audience, scope, thresholds, runbooks, probes, suppression, and audit. | Integration with Operations, Security, and Testing owners |
| Observability conformance suite | Proves signal quality, calculation, privacy, tenant isolation, alert, and outage behavior. | Integration with Testing and Observability owners |

---

# Anti-Patterns

## Provider Uptime Means Action Success

Only bounded Integration outcomes establish whether an external effect is confirmed, failed, restricted, or uncertain.

## Logs Store Provider Payloads

Raw payloads, secrets, and sensitive parameters remain in protected evidence paths, not routine logs/traces.

## Trace ID Grants Access

Correlation is scoped diagnostic evidence and requires current purpose/authorization for any lookup.

## Alert Sends a Participant Message

Alerts notify owners; Conversation controls any participant-facing communication.

---

# Related Documents

| Document | Relationship |
|---|---|
| 06_ACTION_EXECUTION_AND_IDEMPOTENCY.md | Defines outcome and idempotency signals. |
| 07_WORKFLOW_AND_ASYNCHRONOUS_EXECUTION.md | Defines workflow/callback/reconciliation signals. |
| 11_INTEGRATION_GOVERNANCE_AND_AUDIT.md | Defines audit evidence. |
| 12_INTEGRATION_SECURITY_AND_PRIVACY.md | Defines security/privacy controls. |
| 13_INTEGRATION_RELIABILITY_AND_FAILURE_HANDLING.md | Defines resilience outcomes and SLO context. |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-06 | Created Integration observability architecture covering outcomes, signals, SLOs, dashboards, alerts, privacy, and data quality. |
| 1.1 | 2026-08-06 | Approved after completeness, ownership, and long-term maintainability review. |

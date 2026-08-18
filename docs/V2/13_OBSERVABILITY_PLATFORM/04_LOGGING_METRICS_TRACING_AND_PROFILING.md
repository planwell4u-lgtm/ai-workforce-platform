# 04_LOGGING_METRICS_TRACING_AND_PROFILING

**Version:** 1.1  
**Status:** Approved  
**Owner:** Observability Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines how logs, metrics, traces, and profiles are selected, produced, operated, and reviewed across the platform. It provides consistent, privacy-aware diagnostic evidence without making telemetry a shadow domain database, a substitute for audit, or a generic store for participant content.

# Signal Selection Model

| Signal | Best use | Not a substitute for |
|---|---|---|
| Structured logs | Bounded diagnostic events, errors, state transitions, and safe context. | Canonical records, raw customer content, or authorization evidence. |
| Metrics | Aggregated rates, latency, resource/capacity, objectives, quality, and backlog trends. | Per-participant detail or a domain-specific success assertion without owner semantics. |
| Traces | Correlated technical execution across services, jobs, callbacks, and dependencies. | Identity/tenant authorization, a canonical conversation, or external-effect proof. |
| Profiles | Approved performance/resource investigation and optimization. | Routine request logging, code-level surveillance, or sensitive payload capture. |

Domain owners choose the outcomes and objectives that need visibility. Observability owns common libraries, collection/transport, storage, dashboards, access, and operational quality of the signal types.

# Structured Logging Rules

Logs are structured, versioned, and emitted at meaningful boundaries: request admission, job/event receipt, validation, dependency call, retry, state change, error, reconciliation, delivery attempt, and controlled recovery. A record includes safe time, service/module, environment, operation, outcome/error class, trace/correlation reference, version/configuration reference, and bounded owner-approved attributes.

Logs must not contain secret values, access tokens, private keys, raw prompts/messages/transcripts, attachments, full URLs/query strings, unredacted participant identifiers, or raw provider payloads. Error handling sanitizes stack traces and exception messages before capture. Debug logging is time-bounded, scope-limited, access-controlled, reviewed, and disabled/removed after the approved diagnostic window.

# Metrics Rules

Metrics use stable names, documented units, approved dimensions, bounded cardinality, and explicit owner/objective. They measure technical conditions such as request/error rate, latency, saturation, queue/backlog, retry/reconciliation state, dependency health, build/deployment status, and owner-approved domain indicators.

Metric labels exclude raw identities/content and unbounded identifiers. Histograms, counters, gauges, and summaries are chosen based on the question being answered and aggregation needs. A metric name or green threshold must not imply participant delivery, business-action completion, or policy compliance unless the owning platform has documented and validated that meaning.

# Distributed Tracing Rules

Tracing starts at trusted ingress or an approved execution boundary and propagates through service calls, events, jobs, retries, callbacks, adapters, and external dependency boundaries. Spans use safe operation names, start/end/error status, timing, dependency category, outcome classification, and approved references.

Trace sampling is documented by environment, risk, cost, and investigation need. Sampling never intentionally removes required Security audit evidence or the minimum correlation needed for an approved operational/recovery path. A missing trace is recorded as an observability limitation, not silently interpreted as a successful or failed domain outcome.

# Profiling Rules

Profiling is enabled only for approved performance, capacity, incident, or release-investigation purposes. It is restricted by environment, service/component, duration, access, data classification, and retention. Profiles exclude secrets and protected content and are reviewed for privacy/security impact before broad production use.

Profiling findings become a domain/Deployment/Operations improvement proposal when they indicate a performance, cost, reliability, or capacity issue. Observability supplies the evidence; the owner decides product behavior, resource policy, and remediation acceptance.

# Signal Quality and Cost Controls

Observability monitors coverage, ingestion delay, drop/sampling rate, malformed records, cardinality, storage/query cost, retention, and access anomalies. Excessive signal volume, leaking fields, or unbounded labels are treated as operational/security risks and are controlled through approved policy/configuration changes.

Instrument once at the owner boundary, then reuse the shared correlation/envelope. Duplicating equivalent logs/metrics/traces in channel, agent, client, or infrastructure layers merely to create a second success signal is prohibited. The producer that owns a fact publishes its safe evidence; consumers add only their own observed facts.

# Required Evidence

Before implementation approval, demonstrate structured log validation/redaction; metric unit/name/dimension review; bounded-cardinality checks; trace propagation and sampling behavior; safe profile enablement; missing/late/malformed signal handling; signal-cost controls; access negatives; and an investigation path that distinguishes observed telemetry from owner-verified outcome.

# Related Documents

- `01_SHARED_TELEMETRY_AND_ALERTING_CONTRACT.md`
- `02_OBSERVABILITY_PLATFORM_ARCHITECTURE.md`
- `03_TELEMETRY_DATA_MODEL_AND_CORRELATION.md`
- `../09_SECURITY_PLATFORM/13_SECURITY_OBSERVABILITY.md`
- `../08_DATA_PLATFORM/12_DATA_OBSERVABILITY_AND_AUDIT.md`
- `../11_OPERATIONS_PLATFORM/05_SERVICE_HEALTH_CAPACITY_AND_MAINTENANCE.md`
- `../12_DEPLOYMENT_PLATFORM/07_DEPLOYMENT_OBSERVABILITY_RELIABILITY_AND_DISASTER_RECOVERY.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-09 | Created logging, metrics, tracing, and profiling standards. |
| 1.1 | 2026-08-09 | Finalized after privacy, cardinality, signal-ownership, and maintainability review. |

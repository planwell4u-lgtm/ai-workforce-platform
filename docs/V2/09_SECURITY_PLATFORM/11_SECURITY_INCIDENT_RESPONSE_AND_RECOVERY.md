
**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines security incident classification, containment, evidence preservation, investigation, security recovery approval, communication inputs, and learning. Security coordinates security posture; Operations owns incident command and runtime restoration; domains execute safe repair of their own behavior and data.

# Incident Lifecycle

| Stage | Required outcome |
|---|---|
| Detect and triage | Validate signal, start correlation, classify urgency/scope, preserve volatile evidence. |
| Scope and contain | Identify affected identity, tenant, provider, workload, data/effect, and restrict minimum necessary surface. |
| Investigate | Preserve chain-of-custody evidence, determine entry/cause/impact, track uncertainty. |
| Eradicate | Revoke/rotate, patch/reconfigure, remove malicious dependency/access, and validate controls. |
| Recover | Reauthorize and restore only after current identity, policy, scope, lifecycle, residency, integrity, and observability checks. |
| Learn and close | Record outcome, notifications/obligations, remediation, tests, owner, and review. |

# Containment Controls

Containment may suspend principals, revoke sessions/tokens/delegation/credentials, restrict routes/features, quarantine workloads/providers/events, disable export/administration, or limit data access. Every action records authority, scope, reason, time, expected impact, evidence, expiry/review, and handoff. It must not create cross-tenant exposure, erase required evidence, or bypass legal/hold obligations.

# Evidence and Investigation

Evidence is acquired proportionately, access-controlled, time/correlation-preserving, minimally copied, integrity-protected as required, and retained under policy. Investigation access is least-privilege and auditable. Uncertainty is explicit: teams do not assert absence of impact merely because one log, provider response, or backup appears normal.

# Recovery Criteria

Before restoring a restricted capability, verify:

- Cause/entry path contained or an approved compensating control is active.
- Affected credentials, keys, tokens, sessions, workloads, policies, and provider links are revoked/rotated/revalidated.
- Tenant/environment scope, authorization, consent, lifecycle/deletion/hold, residency, and integrity remain current.
- Delayed work, queues, cache, backups, replicas, and external effects are reconciled; stale authority cannot replay.
- Required telemetry/audit evidence is healthy enough to observe recovery.
- An accountable owner accepts the restoration and rollback/restriction plan.

# Communication and Coordination

Security supplies verified impact, control, notification, and regulatory/contractual input through approved channels. It does not independently promise customer outcome or execute domain remediation. Handoffs identify owner, scope, evidence, current restriction, decision needed, deadline, and recovery criteria.

# Exercises and Tests

Practice credential compromise, identity takeover, authorization bypass, provider/webhook compromise, dependency compromise, data/export incident, workload lateral movement, audit failure, and regional/dependency outage. Test containment speed, revoke propagation, evidence access, recovery gate, communications, and lessons-to-regression conversion.

# Anti-Patterns

## Restart Is Recovery

Restart cannot restore trust; current authority, scope, integrity, lifecycle, and evidence must be revalidated.

## Containment Is an Unbounded Shutdown

Containment is minimum necessary, scoped, reviewed, observable, and safely reversible.

## Investigation Copies Everything

Evidence collection remains proportionate, protected, and compliant with data/lifecycle/residency requirements.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created security incident response and recovery model. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with lifecycle, containment, evidence, recovery, coordination, and exercise detail. |

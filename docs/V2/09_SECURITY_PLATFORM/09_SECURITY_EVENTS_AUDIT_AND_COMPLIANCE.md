
**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines security-event taxonomy, audit evidence, compliance-control mapping, evidence handling, and review expectations. Security owns what security evidence is required; Data and Observability own physical mechanisms; domain platforms own business-event meaning.

# Material Security Events

| Event family | Required examples |
|---|---|
| Identity | Enrollment, authentication result, challenge, account recovery/linking, suspension, deprovisioning. |
| Authorization | Policy/version change, allow/deny/restrict/challenge, delegation, approval, revocation, break-glass. |
| Trust and secrets | Workload/certificate/issuer trust change, secret/key issuance/rotation/revoke, provider credential event. |
| Protection | Sensitive access/export, tenant/residency/control violation, encryption/trust failure, privileged administration. |
| Assurance | Vulnerability/risk/exception, test/control evidence, detection/alert outcome, remediation. |
| Incident | Detection, classification, containment, evidence preservation, recovery approval, closure/lesson. |

# Event Contract

Each material record includes event type/version, trusted tenant/environment where applicable, time, actor/workload, resource/action reference, source, policy/control/configuration version, outcome/reason, severity, correlation, and protected evidence link. It excludes raw tokens, passwords, keys, provider credentials, unnecessary personal content, and unrestricted payload copies.

Events are immutable or tamper-evident as required, ordered/correlated sufficiently for investigation, access-controlled, purpose-bound, lifecycle/residency-aware, and themselves auditable. Delayed/failed delivery is marked uncertain and reconciled; absence of an event is not proof of a safe operation.

# Compliance Control Mapping

Security maintains a control catalog mapping each applicable security/privacy/compliance requirement to control objective, owner, implementation boundary, evidence source, test/assurance method, review cadence, exception process, and status. A policy statement alone is not implementation evidence; an audit event alone is not proof a control was effective.

Consuming platforms provide their domain/physical evidence through approved contracts. Security does not duplicate their records or retain unlimited raw customer content to demonstrate a control.

# Evidence Access and Retention

Audit/investigation access requires verified identity, policy-approved purpose, tenant/environment scope, least privilege, and access evidence. Retention, deletion/hold, export, legal request, residency, and redaction follow governing policy and Data mechanisms. Evidence export remains a protected data operation.

# Assurance and Reconciliation

Regularly reconcile required event sources, control versions, evidence completeness, event delivery, access reviews, exceptions, and remediation status. Material control/evidence gaps are classified, assigned, contained where necessary, remediated, retested, and recorded with accountable disposition.

# Anti-Patterns

## Audit Payload Contains Every Request Body

Evidence is minimal and referenced; raw protected content remains in its governed domain/Data representation.

## Compliance Is a Static Spreadsheet

Controls are live mappings to current owners, versions, tests, evidence, exceptions, and review dates.

## Provider Log Is Enterprise Audit

Provider evidence is validated, scoped, retained under policy, and correlated with internal controls before reliance.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created security event, audit, and compliance model. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with taxonomy, contract, control mapping, access, reconciliation, and evidence limits. |

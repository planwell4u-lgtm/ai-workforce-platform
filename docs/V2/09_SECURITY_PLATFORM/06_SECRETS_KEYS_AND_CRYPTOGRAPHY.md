# 06_SECRETS_KEYS_AND_CRYPTOGRAPHY

**Version:** 1.2  
**Status:** Approved  
**Owner:** Security Platform Owner  
**Phase:** Platform Architecture  

---

# Overview

This document defines the lifecycle, access, cryptographic, rotation, recovery, and evidence requirements for secrets, credentials, keys, certificates, and protected configuration. Security Platform owns the control standard; consuming platforms identify their legitimate need and use approved mechanisms without handling plaintext unnecessarily.

# Asset Classes

| Asset | Examples | Required boundary |
|---|---|---|
| Secret | API credential, provider token, database credential. | Store/reference in approved secret control; never source/client/log artifact. |
| Key | Encryption/signing/data-protection key. | Managed lifecycle, purpose/scope, authorized use, rotation/recovery/destruction. |
| Certificate | Workload TLS/mTLS certificate and trust chain. | Issuance, renewal, revocation, peer validation, inventory. |
| Derived credential | Short-lived token from workload/user identity. | Bounded audience/purpose/time; not a long-lived replacement secret. |
| Protected configuration | Sensitive connection/reference/parameter. | Classified, access-controlled, versioned, and redacted. |

# Lifecycle

Every asset has an owner, purpose, tenant/environment/provider scope, classification, system reference, creation/issuer, allowed consumer, expiry, rotation/revocation path, backup/recovery need, audit requirements, and retirement/disposal method.

1. Request and approve the minimum required asset and scope.
2. Generate/issue through the approved authority; record immutable reference and metadata.
3. Deliver only to authorized workload/administrator through protected runtime access.
4. Monitor validity/usage and rotate before expiry or on risk/change.
5. Revoke/disable on compromise, offboarding, provider disconnect, policy change, or retirement.
6. Reconcile consumers, retain required evidence, and destroy material when lifecycle permits.

# Access and Use Rules

Prefer workload identity and short-lived derived credentials over static secrets. A workload receives only the reference/material necessary for its specific provider, tenant/environment, audience, purpose, and lifetime. Human inspection/export of plaintext is exceptional, least-privilege, justified, time-bounded, observed, and audited.

Plaintext material must not appear in source control, repository history, diagrams, examples, tickets, build logs, application logs, traces, metrics, error messages, browser/mobile clients, analytics, or ordinary backups. Redaction is verified rather than assumed.

# Cryptographic Controls

Security specifies approved algorithms/profiles, key use separation, entropy/creation requirements, encryption-in-transit and encryption-at-rest expectations, signing/verification, certificate trust, rotation, and crypto-agility. Data Platform implements storage mechanisms; domain platforms classify data and invoke approved controls.

Key use is separated by purpose (for example, data encryption, signing, transport, and provider integration). Key metadata records purpose, scope, version, algorithm/profile, access policy, residency, backup/recovery, and destruction dependencies. Cryptographic controls do not replace authorization, lifecycle, tenant isolation, or audit.

# Rotation, Revocation, and Recovery

| Condition | Required safe action |
|---|---|
| Planned rotation | Create new version, validate consumer migration, use bounded overlap, retire old version, verify evidence. |
| Suspected compromise | Contain dependent access, revoke/rotate, assess scope, preserve evidence, reconcile and reauthorize recovery. |
| Certificate expiry/trust failure | Restrict connection, renew/replace through approved path, verify peer trust. |
| Provider credential disconnect | Stop external effect, revoke/remove credential, notify owner, require renewed delegation. |
| Backup/restore | Restore only approved encrypted references/material, revalidate policy/scope/version, and never revive revoked access. |

Emergency recovery is documented per asset class and requires accountable approval, minimum scope, enhanced monitoring, expiry, and post-use review. A backup cannot become an ungoverned repository of historical usable secrets.

# Evidence, Monitoring, and Tests

Record request/issuance/reference, access category, policy change, rotation, revocation, expiry, failed retrieval, certificate trust failure, emergency recovery, and destruction evidence without material disclosure. Monitor expiry, rotation health, access anomaly, failed/redacted log detection, provider dependency, and unresolved references.

Test denied access, least privilege, rotation without unintended outage, old-version retirement, compromise/revocation, certificate validation, backup/restore, provider failure, secret scanning, redaction, and tenant/environment separation.

# Anti-Patterns

## Environment Variable Is a Secret Strategy

Runtime injection may be a delivery mechanism, but it does not replace inventory, policy, rotation, access control, or redaction.

## One Key for Every Purpose

Separate key purpose and scope so compromise, rotation, access, and lifecycle remain bounded.

## Encryption Means Access Is Solved

Encryption protects material; current identity, authorization, tenant/purpose, lifecycle, and audit controls remain required.

# Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-07 | Created secrets, keys, and cryptography controls. |
| 1.1 | 2026-08-07 | Originally approved; reopened after completeness review. |
| 1.2 | 2026-08-07 | Rewritten with asset model, lifecycle, crypto, rotation, recovery, evidence, and assurance detail. |

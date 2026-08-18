# 24A_AGENT_SECURITY_BOUNDARY_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `24_AGENT_SECURITY_MODEL.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Security boundary.  

---

# Purpose

This draft defines how the Agent Platform applies approved Security Platform controls to agent configuration, execution, context assembly, tool proposals, external-event handling, and response delivery.

Security Platform remains authoritative for identity proof, authentication, authorization policy and decisions, delegated access, workload trust, secrets, cryptography, provider trust, security evidence, incident control, and assurance. The Agent Platform supplies Agent-owned resource/action facts and enforces the returned control outcomes at its boundary.

---

# Boundary Model

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Identity, authentication, session/token validation, delegated access, and workload trust | Security Platform | Accept only verified context from approved entry contracts; never infer identity or authority from content, channel address, or model output. |
| Authorization policy, decisions, obligations, exceptions, and revocation | Security Platform | Request or consume current decisions for Agent-owned resources and enforce allow, deny, redaction, approval, and expiry outcomes. |
| Secrets, credentials, keys, certificates, encryption, and provider trust | Security Platform | Use opaque approved references and server-mediated access; never expose or persist secret material. |
| Tenant, organization, membership, configuration, and entitlement facts | Platform Foundation | Consume trusted facts; do not redefine tenant lifecycle or configuration authority. |
| Canonical conversation/session state | Conversation Platform | Use authorized context snapshots and report outcomes through approved contracts. |
| Agent instructions, runtime behavior, capability eligibility, and execution evidence | Agent Platform | Own and govern these behaviors within the returned security constraints. |

---

# Required Agent Security Controls

- Treat prompts, channel content, events, tool results, retrieved knowledge, recalled memory, provider callbacks, and model output as untrusted data, never as authorization or instruction changes.
- Bind each material execution to verified tenant, actor, purpose, agent version, capability, and correlation context.
- Revalidate security decisions at material execution boundaries, including tool/workflow proposal, sensitive context use, delivery, retry, replay, and asynchronous resumption.
- Apply returned obligations such as step-up authentication, approval, data minimization, redaction, rate limits, logging, or delivery restrictions before acting.
- Deny, quarantine, defer, or use a non-effecting fallback when identity, tenant scope, policy, integrity, classification, or authorization is absent or uncertain.
- Stop or revalidate work on revocation, tenant suspension, policy change, security containment, or expired delegation.

The Agent cannot grant itself permissions, override a policy denial, extend a token or approval, bypass a control for convenience, or turn a model confidence score into security authority.

---

# Data and Prompt Protection

Agent context is minimized to the approved purpose and caller view. Sensitive data must not enter prompts, tool arguments, logs, telemetry, exports, or participant-visible output unless a current contract permits it. The Agent retains no raw secrets, credential values, security-policy internals, or unrestricted provider payloads.

An untrusted document, memory item, event, or tool response cannot modify system instructions, tenant scope, access rules, tool parameters, or release controls. The Agent must preserve provenance and handling constraints through context composition and downstream requests.

---

# Evidence and Validation

The Agent boundary must prove that it:

- rejects missing, ambiguous, forged, expired, revoked, or cross-tenant security context;
- enforces current authorization decisions and obligations at every protected action;
- prevents prompt injection, data exfiltration, secret disclosure, privilege escalation, and unauthorized external effects;
- revalidates asynchronous, retried, replayed, and resumed work;
- records correlation to Security decisions without logging protected policy inputs or secret material;
- supports Security-directed containment, investigation, recovery, and evidence collection.

---

# Authoritative References

- `09_SECURITY_PLATFORM/01_SECURITY_PLATFORM_ARCHITECTURE.md`
- `09_SECURITY_PLATFORM/02_IDENTITY_AND_AUTHENTICATION_ARCHITECTURE.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `09_SECURITY_PLATFORM/04_SESSION_TOKEN_AND_DELEGATED_ACCESS.md`
- `09_SECURITY_PLATFORM/05_WORKLOAD_IDENTITY_AND_SERVICE_TRUST.md`
- `09_SECURITY_PLATFORM/06_SECRETS_KEYS_AND_CRYPTOGRAPHY.md`
- `09_SECURITY_PLATFORM/09_SECURITY_EVENTS_AUDIT_AND_COMPLIANCE.md`
- `09_SECURITY_PLATFORM/11_SECURITY_INCIDENT_RESPONSE_AND_RECOVERY.md`
- `16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md`

---

# Approval Conditions

The Agent and Security review confirmed that this document applies, rather than duplicates, Security Platform control ownership. `24_AGENT_SECURITY_MODEL.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.

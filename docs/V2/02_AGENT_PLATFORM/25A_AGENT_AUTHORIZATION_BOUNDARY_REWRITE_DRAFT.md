# 25A_AGENT_AUTHORIZATION_BOUNDARY_REWRITE_DRAFT

**Version:** 1.1  
**Status:** Approved  
**Owner:** Agent Platform Owner  
**Phase:** Agent Platform approval review  
**Supersedes:** `25_AGENT_PERMISSION_MODEL.md`  

**File-name note:** The working filename is retained to preserve review traceability; this approved document is the authoritative Agent-to-Authorization boundary.  

---

# Purpose

This draft defines the Agent Platform's use of Security Platform authorization controls. Agent Platform identifies its own protected resources and proposed actions, supplies trusted execution facts to the approved authorization interface, and deterministically enforces returned decisions and obligations.

Security Platform owns enterprise authorization policy, policy decision and enforcement architecture, roles and grants, delegated access, approval requirements, exceptions, revocation, and audit requirements. Platform Foundation owns tenant, membership, configuration, and entitlement facts used as authorized policy inputs.

---

# Boundary Model

| Concern | Authoritative owner | Agent Platform responsibility |
|---|---|---|
| Identity, policies, grants, roles, decisions, delegation, step-up, approval, revocation, and exceptions | Security Platform | Submit Agent-owned resource/action facts; enforce the current returned decision and obligations. |
| Tenant, organization, membership, configuration, and entitlement facts | Platform Foundation | Consume trusted facts; do not create or alter control-plane authority. |
| Agent definitions, versions, capabilities, execution context, and behavior evidence | Agent Platform | Define protected Agent resources and validate that proposed work maps to an approved capability/version. |
| Tool, workflow, connector, and external-effect execution | Integration Platform | Request the approved contract only after Agent boundary checks; Integration independently authorizes and enforces effects. |
| Conversation and channel interaction state | Conversation and channel platforms | Use approved context without treating a channel identity or UI state as authority. |

---

# Agent Authorization Inputs

For a protected Agent action, the Agent Platform supplies only trusted, minimum inputs: verified subject and delegation references; tenant and purpose context; Agent resource/action/capability/version; target classification; requested parameters or risk signals; environment; correlation; and current lifecycle references.

Model intent, previous approval, a visible feature flag, a cached chat context, a channel address, or a user-supplied identifier is not authorization. The Agent must request a current decision whenever the policy requires it and must not turn an ambiguous result into an allow.

---

# Enforcement Rules

- Deny by default when a protected action has no current allow decision.
- Enforce obligations before action: confirmation, human approval, redaction, rate limit, secure delivery, audit, or additional verification.
- Revalidate after material changes to subject, delegation, tenant, purpose, policy, entitlement, configuration, resource lifecycle, or risk classification.
- Never permit an Agent to approve its own proposal, extend authority, impersonate an approver, or reuse a revoked/expired decision.
- Treat cached decisions as bounded performance aids only; invalidate or refresh them under Security-defined expiry and revocation rules.
- Pass authorization references to Integration or other owning platforms, which must independently enforce their own boundaries.

---

# Safe Outcomes

| Decision or condition | Agent behavior |
|---|---|
| Allow with obligations | Satisfy all obligations before continuing; report only the permitted outcome. |
| Deny | Do not retry to find a bypass; explain or escalate only as policy permits. |
| Approval or confirmation required | Request the approved evidence; do not imply action is complete. |
| Revoked, expired, or stale | Stop or revalidate work under current policy. |
| Unavailable or uncertain | Defer, restrict, or provide a non-effecting fallback; never assume allow. |

---

# Evidence and Validation

The boundary must prove that Agent actions are denied without a current decision; that tenant/purpose/delegation mismatches cannot cross scope; that obligation, revocation, approval, and expiration behavior is enforced; that model content cannot modify policy; and that protected actions record auditable correlation without exposing secret, policy-internal, or unnecessary personal data.

---

# Authoritative References

- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `09_SECURITY_PLATFORM/04_SESSION_TOKEN_AND_DELEGATED_ACCESS.md`
- `09_SECURITY_PLATFORM/08_TENANT_ISOLATION_AND_DATA_PROTECTION.md`
- `09_SECURITY_PLATFORM/09_SECURITY_EVENTS_AUDIT_AND_COMPLIANCE.md`
- `16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md`
- `16_PLATFORM_FOUNDATION/03_CONFIGURATION_AND_ENTITLEMENT_MODEL.md`
- `07_INTEGRATION_PLATFORM/05_ACTION_AUTHORIZATION_AND_APPROVAL.md`

---

# Approval Conditions

The Agent and Security review confirmed that this document consumes rather than duplicates enterprise authorization control ownership. `25_AGENT_PERMISSION_MODEL.md` remains available as a deprecated historical artifact; this document is the authoritative replacement.

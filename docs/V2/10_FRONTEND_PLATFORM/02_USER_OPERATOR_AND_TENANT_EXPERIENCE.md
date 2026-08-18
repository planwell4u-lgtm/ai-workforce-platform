# 02_USER_OPERATOR_AND_TENANT_EXPERIENCE

**Version:** 1.1  
**Status:** Approved  
**Owner:** Frontend Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines how the frontend presents tenant-aware customer and operator experiences. It makes current organization scope, available capabilities, authorization outcomes, and sensitive-context changes clear without creating a client-side authorization or tenancy system.

# Experience Roles

| Experience | Primary goal | Boundary |
|---|---|---|
| Customer/participant | Use an approved channel experience and receive truthful status/outcome information. | Channel, Conversation, and Agent platforms own communication behavior and canonical state. |
| Organization operator | Configure, review, observe, and intervene within granted scope. | Platform Foundation and Security determine membership, entitlement, and authorization. |
| Administrator | Manage approved organization/membership/configuration paths. | The UI requests changes; Platform Foundation/Security enforce them. |
| Support or incident responder | Investigate a purpose-limited, least-privilege view. | Security and Operations control elevation, evidence access, and incident procedure. |

# Tenant Context

The application shell always displays the active organization/tenant context and provides a server-authorized scope-change path when a person has more than one permitted scope. A selected tenant in local state, URL, cookie, or client cache is a request for scope—not proof that scope is permitted.

On scope change, session change, membership/entitlement update, revocation, or policy invalidation, the client clears or partitions tenant-bound views, revalidates server state, cancels unsafe in-flight work, and avoids showing stale protected information. It does not silently merge data or permissions across organizations.

# Navigation and Presentation Rules

- Navigation is organized around authorized tasks: agent management, governed knowledge, conversations/outcomes, approved actions, and organization administration.
- Visible navigation and controls may improve usability but are not an authorization boundary. Server responses for forbidden, unavailable, expired, or changed scope take precedence.
- The UI distinguishes a missing capability, an unavailable service, a pending approval, a denied request, and an empty result. It does not conceal a policy denial as a generic error.
- Deep links validate current identity, tenant, entitlement, resource access, and workflow/conversation state before rendering protected information.
- Handoff, approval, cancellation, and intervention controls show the owning platform’s authoritative disposition, required next step, and safe refresh path.

# Initial Operator Journey

For the first vertical slice, an authorized operator can select an allowed organization, view one governed agent, inspect its approved status and bounded configuration, observe one correlated conversation/channel outcome, and review one controlled business-action or approval result. The journey provides loading, empty, forbidden, expired, error, and recovery states.

The frontend does not expose raw provider records, unrestricted transcripts, tenant-wide search, direct tool execution, hidden admin routes, or a locally fabricated approval state.

# Required Evidence

Provide evidence for tenant-switch isolation, deep-link authorization, membership/entitlement revocation, stale-cache clearance, role-aware navigation, pending/denied/forbidden states, accessible keyboard/screen-reader flow, localization-safe labels, and end-to-end tenant-scoped journey behavior.

# Related Documents

- `01_FRONTEND_PLATFORM_ARCHITECTURE.md`
- `16_PLATFORM_FOUNDATION/02_TENANT_ORGANIZATION_AND_MEMBERSHIP_MODEL.md`
- `16_PLATFORM_FOUNDATION/03_CONFIGURATION_AND_ENTITLEMENT_MODEL.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`
- `03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md`
- `02_AGENT_PLATFORM/04_AGENT_LIFECYCLE.md`
- `07_INTEGRATION_PLATFORM/05_ACTION_AUTHORIZATION_AND_APPROVAL.md`

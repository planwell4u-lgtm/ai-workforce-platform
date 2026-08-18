# 04_FRONTEND_CONTRACT_AND_API_CONSUMPTION

**Version:** 1.1  
**Status:** Approved  
**Owner:** Frontend Platform Owner  
**Phase:** Platform Architecture

---

# Purpose

This document defines how frontend clients consume backend contracts. It preserves the authoritative ownership of Platform Foundation, Security, Conversation, Agent, Digital Channel, Integration, Data, and other platform services while giving users clear, truthful request and outcome states.

# Contract Boundary

The frontend calls only approved API-edge, backend-for-frontend, or service contracts. It never accesses databases, storage, queues, caches, vector stores, provider APIs, webhook endpoints, secrets, or internal service protocols directly.

Each client request uses the approved identity/session mechanism and carries only the server-approved scope implied by that mechanism. A tenant ID, role, authorization choice, feature entitlement, resource classification, action approval, or delivery state supplied by the client is untrusted until the owning backend validates it.

# Response and Outcome Model

Contracts expose typed outcomes rather than ambiguous success/failure flags:

| Outcome | Client presentation rule |
|---|---|
| Accepted / pending | Show the action is awaiting a later authoritative result; provide correlation and safe refresh. |
| Completed | Show only the verified outcome reported by the owning service. |
| Rejected / forbidden | Explain safe next steps without exposing policy internals or protected data. |
| Conflict / stale version | Refresh or guide controlled user resolution; never silently overwrite. |
| Unavailable / retryable | Offer bounded retry or recovery according to the contract. |
| Unknown / reconciliation pending | Do not submit again automatically; show the pending investigation state. |
| Expired / revoked | Clear protected state and guide re-authentication or scope re-selection. |

Provider acceptance, message delivery, agent execution, workflow completion, and external business-effect completion remain separate outcomes. The UI must preserve those distinctions.

# Versioning and Compatibility

- Contract clients are typed, version-aware, and generated or reviewed from the approved source contract where practical.
- Additive compatible fields may be ignored safely until adopted. Removed fields, changed semantics, new required inputs, changed error/outcome behavior, or changed authorization requirements require coordinated rollout and migration.
- The client supplies idempotency or concurrency fields only when the owning contract defines them; it does not implement the underlying correctness mechanism.
- Contract deprecation includes owner, consumer inventory, compatibility window, user-visible impact, fallback/rollback behavior, and removal approval.

# Error, Pagination, and Query Rules

Responses must preserve correlation and safe error categories while excluding secrets, raw provider payloads, unnecessary protected content, and authorization internals. Query/filter/sort inputs are validated by the backend; client filters never expand data scope. Pagination, search, export, attachment retrieval, and background polling use purpose-limited, tenant-scoped endpoints and respect data classification and retention policy.

# Mutations and Actions

The UI may initiate an authorized request, display required approval input, and render the returned lifecycle state. It cannot approve itself, execute a connector directly, bypass a workflow, or claim an effect before the owning contract confirms it. A retry after a timeout or unknown result must use the designated status/reconciliation path.

# Required Evidence

Provide contract compatibility tests, negative scope/authorization tests, typed outcome mapping tests, stale-version/conflict tests, pagination/export classification tests, no-direct-data-access checks, sensitive error/redaction tests, and end-to-end proof that UI labels preserve backend disposition.

# Related Documents

- `01_FRONTEND_PLATFORM_ARCHITECTURE.md`
- `03_FRONTEND_APPLICATION_AND_STATE_MODEL.md`
- `16_PLATFORM_FOUNDATION/04_API_EDGE_AND_SERVICE_DISCOVERY.md`
- `07_INTEGRATION_PLATFORM/04_ACTION_EXECUTION_AND_IDEMPOTENCY.md`
- `07_INTEGRATION_PLATFORM/05_ACTION_AUTHORIZATION_AND_APPROVAL.md`
- `17_DIGITAL_CHANNEL_PLATFORM/02_CHANNEL_ADAPTER_AND_MESSAGE_MODEL.md`
- `09_SECURITY_PLATFORM/03_AUTHORIZATION_POLICY_AND_ENFORCEMENT.md`

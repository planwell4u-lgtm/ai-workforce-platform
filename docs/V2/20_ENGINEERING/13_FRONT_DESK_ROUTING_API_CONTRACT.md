# Front Desk Routing API Contract

**Version:** 0.10  
**Status:** Partially implemented — test-only configuration, concurrency, health, eligibility, and route-request slices  
**Date:** 2026-08-27  
**Purpose:** Define the versioned API boundary for tenant-admin destination
configuration and Front Desk route requests.

---

## Scope

This is the planned HTTP API shape for Front Desk Worker V1. It separates two
different responsibilities:

1. **Tenant-admin configuration:** create and govern a tenant's eligible
   destination records.
2. **Conversation routing:** request a bounded route outcome for one active
   participant conversation.

The API returns recorded decisions and safe statuses. It does not transfer a
call, assign a human, send an external message, create a ticket, disclose a
private contact, or claim a handoff is complete.

The eventual machine-readable source of truth belongs in `protocols/contracts/v1/`
after Platform Foundation, Conversation, Security, and compatibility owners
approve this design.

## Implemented Test-only Slice

The backend now exposes only `POST /v1/conversation-routing-requests` for the
configured support tenant. It requires the existing `agent.context.read`
permission, an existing tenant-scoped conversation with no active turn, and an
exact request body of `conversation_ref`, `route_purpose`, and `event_ref`.

The registry is synthetic and fixed: `support` records `route_requested` for
that tenant; `human_support` returns `safe_unavailable`. Requests are stored
under a separate tenant-scoped `routing` record kind and are idempotent by
event reference. The route-request slice has no dynamic configuration health
integration, actual destination delivery, or external side effect.

The test-only control plane now also implements destination listing, draft
creation, validation, activation, and suspension. Before each routing request,
the server resolves exactly one tenant-scoped, active, purpose/type-compatible,
synthetic `web_chat` record. Missing, suspended, or incompatible records result
in `safe_unavailable`; routing cannot use another tenant's record or a fixed
fallback destination.

Validation creates a short-lived synthetic health signal. Activation and each
route lookup reject a record unless its health state is `healthy` and its
timezone-aware expiry remains in the future. This does not query a live worker,
human queue, carrier, or provider; those health sources remain deferred.

Implemented lifecycle calls carry only `expected_configuration_version`. The
server performs an atomic compare-and-swap mutation and rejects a stale version
with `409 state_conflict`; it never applies a last-write-wins configuration
update.

Activation also persists a unique tenant/purpose claim in the same database
transaction as the destination state transition. A competing activation cannot
create a second active destination for that purpose; suspension releases only
its matching claim in the same transaction.

The implemented request endpoint now supports a test-only two-step flow. An
`offer` records a `route_offered` or `handoff_offered` outcome with the selected
opaque destination reference. A later `request` supplies that offer reference;
the backend verifies the same conversation and purpose, then resolves that
same destination again. If it has been withdrawn, suspended, changed,
unhealthy, or expired, the request records `safe_unavailable` instead of using
another destination or claiming a handoff.

The original three-field request remains temporarily compatible as a direct
request. It has no offer reference and is still fully revalidated at request
time. The signed-in test web-chat now exposes this narrow Front Desk control
after it has received an opaque conversation reference. It displays only the
approved availability/request message and never treats a recorded request as a
completed transfer. The Client Workspace configuration UI remains deferred.

A separate test-only `/front-desk-admin` screen now invokes the administrator
configuration endpoints with the expected configuration version. It is gated by
`platform.front-desk.configure` and has no fallback to customer or operator
access. It cannot configure a real destination or complete a handoff.

## Common Rules

Every endpoint must:

- authenticate the caller and derive tenant, principal, role, permission, and
  environment on the server;
- use `/v1/` versioning and explicit request/response schemas;
- emit a server-generated `correlation_ref` and minimum-necessary audit event;
- reject unknown fields and never accept client-supplied authority fields;
- use opaque references only—never raw provider IDs, phone numbers, email
  addresses, credentials, queue details, or customer data; and
- return a stable safe error code without exposing cross-tenant or protected
  information.

Tenant, target, worker version, destination health, policy, approval, channel,
and conversation state are trusted server-derived values. The browser and model
cannot select or override them.

## Tenant-admin Configuration API

These planned endpoints are available only to an authorized tenant admin or
named platform policy owner. A tenant admin never supplies a tenant reference
in the path or body; tenancy comes from the authenticated workspace context.

| Method and path | Purpose | Result |
|---|---|---|
| `GET /v1/front-desk/destinations` | List authorized tenant-scoped destination summaries. | Paginated, minimum-necessary configuration records. |
| `POST /v1/front-desk/destinations` | Create a new draft configuration version. | `201` draft record. |
| `POST /v1/front-desk/destinations/{destination_ref}/validate` | Run trusted validation without activation. | `200` validation result and recorded status. |
| `POST /v1/front-desk/destinations/{destination_ref}/activate` | Activate an approved validated version. | `200` active record or safe conflict. |
| `POST /v1/front-desk/destinations/{destination_ref}/suspend` | Stop new offers and requests. | `200` suspended record. |
| `POST /v1/front-desk/destinations/{destination_ref}/withdraw` | Withdraw a record, subject to reconciliation. | `200` withdrawn record. |
| `POST /v1/front-desk/destinations/{destination_ref}/rollback` | Restore a prior approved configuration version. | `200` new active version or safe conflict. |

### Draft Create Request

```json
{
  "route_purpose": "support",
  "destination_type": "support_worker",
  "target_ref": "opaque-approved-worker-reference",
  "channel_scope": ["web_chat"],
  "public_display_ref": "opaque-approved-display-reference",
  "idempotency_key": "client-generated-unique-request-reference"
}
```

V1 accepts only these fixed pairs:

| `route_purpose` | `destination_type` |
|---|---|
| `support` | `support_worker` |
| `human_support` | `human_support_route` |

The backend confirms that `target_ref` is owned, approved, and eligible in the
current tenant. It must never resolve an arbitrary worker, external URL, or
contact supplied by the browser.

### Admin Response Shape

```json
{
  "destination_ref": "dst_opaque",
  "route_purpose": "support",
  "destination_type": "support_worker",
  "channel_scope": ["web_chat"],
  "public_display": "Support",
  "lifecycle_state": "validated",
  "configuration_version": 3,
  "health_state": "healthy",
  "updated_at": "2026-08-27T12:00:00Z",
  "correlation_ref": "cor_opaque"
}
```

The response deliberately omits raw `target_ref`, approval evidence, private
contact data, provider configuration, queue state, and internal health detail.

## Conversation Route-request API

`POST /v1/conversation-routing-requests` is the planned participant-facing
boundary. It is invoked only by the approved Front Desk web-chat surface or a
trusted channel adapter, after the Front Desk Worker determines a permitted
purpose.

### Request

```json
{
  "conversation_ref": "conv_opaque",
  "route_purpose": "human_support",
  "event_ref": "evt_unique_per_attempt"
}
```

`route_purpose` is limited to `support` and `human_support`. A request must not
include a destination reference, transcript, contact detail, free-form message,
worker identity, tenant reference, channel, or arbitrary metadata.

### Response

```json
{
  "routing_request_ref": "rr_opaque",
  "outcome": "handoff_requested",
  "public_message": "Your request for human support has been sent.",
  "expires_at": "2026-08-27T12:15:00Z",
  "correlation_ref": "cor_opaque"
}
```

The only V1 `outcome` values are `route_offered`, `route_requested`,
`handoff_offered`, `handoff_requested`, `safe_unavailable`, `forbidden`, and
`uncertain`. `route_requested` and `handoff_requested` mean the request was
recorded—not that the destination accepted it or that delivery occurred.

## State, Idempotency, and Errors

| Condition | HTTP status | Stable response code | Client behavior |
|---|---:|---|---|
| New valid configuration draft | `201` | `created` | Show draft status. |
| Valid route decision | `200` | `recorded` | Show only approved outcome. |
| Replayed idempotency key with same scope | `200` | `replayed` | Reuse the original outcome. |
| Invalid request shape | `400` | `invalid_request` | Correct and resubmit. |
| No authenticated/authorized access | `403` | `forbidden` | Show generic safe access message. |
| Referenced record absent or outside visibility | `404` | `not_found` | Do not reveal whether it exists elsewhere. |
| Current lifecycle/version conflict | `409` | `state_conflict` | Refresh/reconcile; do not retry blindly. |
| Dependency/state cannot be confirmed | `202` | `uncertain` | Present uncertain state and stop automatic retries. |

An idempotency key is bound to its authenticated tenant, principal/conversation,
operation, and normalized request contents. Reusing it with different content
is rejected. A state change after an earlier offer always requires a fresh
server validation before any request is recorded.

## Authorization and Visibility

- Public participants can create a route request only for an active,
  participant-visible conversation in their authenticated channel context.
- Tenant admins can see and manage only their tenant's configuration summaries.
- Activation, rollback, and policy override require explicit, separately
  authorized approval; client-side role checks are never sufficient.
- Platform support uses purpose-limited, auditable access and cannot silently
  mutate a tenant configuration.
- A Front Desk worker has no configuration-management authority and receives
  no private destination detail.

## Required Contract Tests

1. Schema validation rejects unknown fields, raw contacts, credentials, and
   client-supplied authority fields.
2. Tenant A cannot list, mutate, resolve, or request Tenant B's destination.
3. Only the two V1 purpose/type pairs can be saved or used.
4. A destination remains unavailable until it is validated, approved, active,
   channel-compatible, and health-fresh.
5. Replaying a route request returns its stored result; changed contents or
   stale conversation state cannot create a second effect.
6. Withdrawn, suspended, stale, unhealthy, or changed destinations are
   revalidated and produce a safe-unavailable or uncertain outcome.
7. Every privileged mutation and every route decision has tenant-scoped audit
   evidence without conversation content, private contacts, or credentials.
8. The frontend displays only the response fields above and never declares a
   transfer, assignment, or handoff complete.

## Implementation Sequence

1. Convert the approved design into versioned JSON Schema or OpenAPI contracts
   in `protocols/contracts/v1/`.
2. Review tenant ownership, authorization, audit, retention, compatibility,
   and rollback with the owning platform modules.
3. Implement a test-only backend registry and route-outcome service using
   synthetic destinations only.
4. Run schema, contract, tenant-isolation, idempotency, lifecycle, and failure
   tests.
5. Add the Client Workspace configuration screen and Front Desk route-offer UI
   only after the backend boundary is verified.

## Deferred Scope

This API does not authorize actual human assignment, queue selection,
skills-based routing, telephone transfer/forwarding, external notifications,
CRM/calendar actions, ticket creation, provider configuration, customer-data
routing, or cross-channel identity matching.

## Related Documents

- `09_SHARED_WORKER_BLUEPRINT.md`
- `10_FRONT_DESK_WORKER_V1.md`
- `11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `12_FRONT_DESK_DESTINATION_REGISTRY.md`
- `../03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `../16_PLATFORM_FOUNDATION/README.md`
- `../../protocols/README.md`

## Revision History

| Version | Date | Changes |
|---|---|---|
| 0.10 | 2026-08-27 | Added the permission-bound test-only Front Desk destination administrator screen. |
| 0.9 | 2026-08-27 | Added the test-only web-chat route-offer/request control with no transfer claim. |
| 0.8 | 2026-08-27 | Added test-only offer-to-request revalidation against the same active destination. |
| 0.7 | 2026-08-27 | Added atomic single-active destination claims per tenant and route purpose. |
| 0.6 | 2026-08-27 | Added atomic expected-version checks for test-only lifecycle mutations. |
| 0.5 | 2026-08-27 | Added test-only healthy-and-fresh eligibility checks at activation and route lookup. |
| 0.4 | 2026-08-27 | Connected route requests to freshly resolved active tenant destination records. |
| 0.3 | 2026-08-27 | Implemented the test-only tenant-admin destination configuration lifecycle; it remains separate from route eligibility. |
| 0.2 | 2026-08-27 | Implemented the test-only, tenant-scoped support route-request slice and recorded its deliberate limits. |
| 0.1 | 2026-08-27 | Created the planned versioned Front Desk routing API contract. |

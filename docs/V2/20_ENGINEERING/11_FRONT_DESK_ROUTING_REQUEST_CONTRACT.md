# Front Desk Routing Request Contract

**Version:** 0.1
**Status:** Planned
**Date:** 2026-08-27
**Purpose:** Define the first tenant-safe, non-transfer routing-request boundary for Front Desk Worker V1.

---

## Scope

This contract lets Front Desk Worker V1 request an eligible next destination for an active conversation. In V1, the only destination types are the configured tenant Support Worker and the configured tenant human-support route.

It creates a governed routing request and an explainable outcome. It does not perform a telephony transfer, assign a human operator, create a ticket, disclose context, invoke an integration, or claim that a handoff has completed.

Conversation Platform remains the authoritative owner of conversation lifecycle, routing decisions, turn ownership, and human-handoff coordination. Agent Platform requests the routing purpose; Frontend presents the approved outcome.

## V1 Flow

```text
Front Desk Worker identifies a permitted routing purpose
        ↓
Backend receives a bounded routing request
        ↓
Conversation Routing validates tenant, conversation, lifecycle,
worker version, configured destination, policy, and active-turn state
        ↓
Eligible destination exists
        ├── Support Worker → record route offered or requested
        └── Human support → record handoff offered or requested
        ↓
No eligible destination → record safe-unavailable outcome
        ↓
Frontend presents the approved outcome; it never claims a transfer completed
```

## Request Inputs

The public client request contains only opaque references and a bounded purpose. Trusted backend services resolve all authority-bearing values.

| Input | Source | Rule |
|---|---|---|
| `conversation_ref` | Client request | Must identify an active tenant-scoped conversation visible to the participant. |
| `route_purpose` | Front Desk Worker outcome | V1 enum: `support` or `human_support`. |
| `event_ref` | Client or channel idempotency input | Unique per routing attempt and validated for duplicate handling. |
| `correlation_ref` | Backend | Generated or validated by the trusted request path; never selected by the model. |
| Tenant, participant, permissions, worker/version, channel, lifecycle, turn owner | Backend contracts | Derived server-side; never accepted as client authority. |

The request must not carry a destination URL, phone number, email address, queue identifier, provider credential, account data, transcript, raw model instruction, or arbitrary metadata.

## Destination Registry

Each tenant may publish at most one active V1 destination for each route purpose.

| Route purpose | Allowed destination | Required registry fields |
|---|---|---|
| `support` | Tenant-approved active Support Worker | Tenant, worker reference/version, lifecycle eligibility, channel scope, policy version, and health state. |
| `human_support` | Tenant-approved human-support route | Tenant, route reference, channel-safe display method, lifecycle eligibility, policy version, and health state. |

The registry stores references and eligibility metadata, not raw destination credentials or unrestricted contact data. A destination that is inactive, stale, mismatched, withdrawn, or unhealthy is ineligible.

## Decision Outcomes

| Outcome | Meaning | Permitted frontend message |
|---|---|---|
| `route_offered` | An eligible destination exists; the participant may choose to continue there. | “I can connect you with Support.” |
| `route_requested` | A participant or authorized policy requested the eligible next destination. | “Your request has been sent to Support.” |
| `handoff_offered` | An eligible human-support path exists. | “I can help you reach human support.” |
| `handoff_requested` | A human-support request was recorded. | “Your request for human support has been sent.” |
| `safe_unavailable` | No eligible destination can safely be offered or requested. | “Human support is not available through this channel right now.” |
| `forbidden` | The requester, conversation, or policy is ineligible. | Generic safe access/fallback message only. |
| `uncertain` | Dependency or state reconciliation prevents a confirmed outcome. | “We could not confirm the request. Please try again or use the approved contact path.” |

`route_requested` and `handoff_requested` indicate a recorded request only. They never imply human acceptance, channel transfer, delivery, ticket creation, or resolution.

## Precedence and Validation

Before selecting a destination, the backend checks:

1. Tenant/environment, suspension, classification, and policy restrictions.
2. Conversation visibility, lifecycle, participant assurance, and consent.
3. Active handoff, turn ownership, duplicate event, and pending-action state.
4. Front Desk Worker version, lifecycle, and route-purpose eligibility.
5. Registry tenant match, destination lifecycle, channel scope, health, and policy version.
6. Destination-specific current authorization.

Any failed or stale condition produces `forbidden`, `safe_unavailable`, or `uncertain` as appropriate. It must not fall back to another tenant, arbitrary agent, hidden queue, less-secure channel, or direct external contact.

## Idempotency and State

- A routing attempt is bound to tenant, conversation, route purpose, event reference, and current conversation state.
- Repeating the same request returns the recorded outcome rather than creating duplicate assignments, notifications, or external effects.
- A changed conversation lifecycle, withdrawn destination, expired decision, or changed policy requires a new validated request.
- Conversation Platform owns turn ownership, state versioning, supersession, handoff state, and recovery reconciliation.
- A dependency timeout or conflicting state is `uncertain`, never silently retried or presented as completed.

## Privacy and Security

- A public participant may request a route but gains no identity, account, or customer-data authority by doing so.
- The Front Desk Worker receives no hidden destination details, human queue state, other-tenant information, or provider credential.
- Routing records contain only the minimum references, purpose, outcome, policy, expiry, and correlation evidence required for audit and recovery.
- The client may display only the approved outcome and configured public-facing destination information.
- Support and Platform Admin access to route records must be tenant-scoped, purpose-limited, and auditable.

## Frontend Requirements

The Client Workspace and public Front Desk surface must:

- show a route/handoff option only when the backend returns an eligible offer;
- disable repeated submission while a request is pending;
- distinguish requested, unavailable, forbidden, and uncertain outcomes;
- never render a route as completed until an owning Conversation or Channel contract reports completion;
- provide a safe alternate contact message when no destination is available; and
- avoid placing destination configuration, sensitive references, or routing evidence in browser storage or client logs.

## Implementation Order

1. Define the tenant-scoped destination-registry schema and lifecycle policy.
2. Define the versioned routing-request and outcome schemas under Conversation Platform ownership.
3. Add server-side validation, idempotency, audit, and outcome persistence.
4. Add synthetic contract, tenant-isolation, duplicate, stale-state, withdrawn-destination, and dependency-failure tests.
5. Add a Front Desk Worker test-only route offer in web chat.
6. Add the Client Workspace destination-configuration experience after the backend policy and authorization contracts are available.
7. Consider actual human queue assignment, telephone transfer, tickets, or external notifications only as separately approved future scopes.

## Acceptance Criteria

1. A valid Front Desk request can offer only the active destination configured for its own tenant and purpose.
2. Cross-tenant, withdrawn, stale, duplicate, unauthorized, or lifecycle-conflicting requests cannot produce an assignment or external effect.
3. The client cannot submit a raw destination, override a route purpose, or mark a transfer complete.
4. Route request outcomes are idempotent, tenant-scoped, auditable, and safely explainable.
5. Unknown health, policy, capacity, or state is treated as constrained or unavailable; no silent alternative route is selected.
6. The test-only web-chat path proves offer, request, safe-unavailable, forbidden, duplicate, and uncertain behavior without customer data or provider contact.

## Deferred Scope

This contract does not authorize human queue assignment, live transfer, phone forwarding, call bridging, outbound contact, ticket creation, CRM/calendar integration, lead capture, notifications, routing based on protected data, provider selection, phone-number configuration, or cross-channel continuity based only on a contact detail.

## Related Documents

- `10_FRONT_DESK_WORKER_V1.md`
- `09_SHARED_WORKER_BLUEPRINT.md`
- `12_FRONT_DESK_DESTINATION_REGISTRY.md`
- `13_FRONT_DESK_ROUTING_API_CONTRACT.md`
- `../03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `../03_CONVERSATION_PLATFORM/08_CONVERSATION_HANDOFF_MODEL.md`
- `../02_AGENT_PLATFORM/14_AGENT_CAPABILITY_MODEL.md`
- `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`

## Revision History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-08-27 | Created the planned tenant-safe Front Desk routing-request contract. |

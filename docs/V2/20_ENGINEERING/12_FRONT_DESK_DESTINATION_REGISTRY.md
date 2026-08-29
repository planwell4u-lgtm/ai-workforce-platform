# Front Desk Destination Registry

**Version:** 0.7
**Status:** Partially implemented — test-only configuration, concurrency, health, and eligibility lookup
**Date:** 2026-08-27
**Purpose:** Define the tenant-scoped, backend-governed registry that supplies
eligible Support Worker and human-support destinations to Front Desk Worker V1.

---

## Scope

The Destination Registry is configuration, not a routing engine or contact
directory. It declares which destinations a tenant permits Front Desk Worker V1
to offer for a named routing purpose.

V1 supports only these purposes:

| Purpose | Destination type | Meaning |
|---|---|---|
| `support` | Support Worker | Offer a tenant-approved active Support Worker. |
| `human_support` | Human-support route | Offer a tenant-approved human-support path. |

The registry does not send messages, assign people, create a queue ticket,
transfer calls, store provider credentials, or expose a human's private contact
details. Those are separate Conversation, Channel, Integration, Security, and
Operations concerns.

## Implemented Test-only Slice

The backend exposes tenant-admin configuration endpoints for `GET` and `POST`
`/v1/front-desk/destinations`, plus `validate`, `activate`, and `suspend`
lifecycle operations on an opaque destination reference. They require the
separate `platform.front-desk.configure` permission and use the server-derived
tenant scope.

The implemented slice permits only the two V1 purpose/type pairings and the
single synthetic `web_chat` channel scope. It rejects arbitrary target
references, contact details, provider settings, and unlisted fields. A tenant
can have at most one active record for each routing purpose. The route-request
API now performs a fresh lookup for exactly one compatible active record before
recording an outcome. There is still no Client Workspace UI, actual human or
provider destination, external health feed, or external delivery.

Validation assigns a test-only synthetic `healthy` signal with a server-created
five-minute expiry. Activation and every routing lookup require that signal to
be healthy, timezone-aware, and unexpired. An unknown, malformed, or expired
signal is ineligible and safely produces no route. This is a safety mechanism,
not evidence of real queue, worker, provider, or human availability.

Every implemented lifecycle action also requires the exact
`expected_configuration_version` last read by the admin. The store performs an
atomic compare-and-swap update that increments the version exactly once. A
stale action or a concurrent update returns a safe conflict and makes no
change. This protects one destination record from lost updates; broader
multi-record activation coordination is also enforced for the V1 purpose slot:
activation atomically claims a tenant/purpose entry, and suspension atomically
releases only that destination's claim. Therefore two active destinations for
the same tenant and purpose cannot be committed by competing requests.

An active record may be withdrawn. Withdrawal atomically changes the lifecycle
state and releases its tenant/purpose claim. Later destination lookups exclude
withdrawn records; they cannot be revived by a prior route offer.

## Ownership and Boundary

- **Platform Foundation** owns tenant, membership, entitlement, and approved
  configuration facts.
- **Conversation Platform** owns routing decisions, turn ownership, handoff,
  and outcome state.
- **Agent Platform** consumes eligible destination references; it does not
  select arbitrary destinations.
- **Frontend Platform** presents authorized configuration and route outcomes;
  it does not decide eligibility.
- **Integration and Channel Platforms** own any later delivery, queue,
  provider, or contact mechanism.

## Registry Record

Each record is immutable by version and belongs to exactly one tenant.

| Field | Description |
|---|---|
| `destination_ref` | Opaque stable identifier; never a direct URL, number, email address, or credential. |
| `tenant_ref` | Trusted tenant ownership; mandatory on every lookup and mutation. |
| `route_purpose` | V1 enum: `support` or `human_support`. |
| `destination_type` | V1 enum: `support_worker` or `human_support_route`. |
| `target_ref` | Opaque reference to the governed worker or human-support-route configuration. |
| `lifecycle_state` | `draft`, `validated`, `active`, `suspended`, `withdrawn`, or `retired`. |
| `channel_scope` | Channels on which the destination may be offered. |
| `public_display_ref` | Reference to approved, channel-safe user-facing label or notice. |
| `policy_version_ref` | Routing policy/version that approved the record. |
| `configuration_version` | Monotonic version used for validation, audit, and rollback. |
| `health_state` | Bounded eligibility signal: `healthy`, `constrained`, `unavailable`, or `unknown`. |
| `health_expires_at` | Freshness limit for the health signal. |
| `approval_ref` | Required owner approval evidence before activation. |
| `created_by`, `updated_by`, timestamps | Auditable configuration provenance. |

The record must not contain raw customer data, conversation content, provider
credentials, personal phone numbers, personal email addresses, queue capacity
details, or unrestricted instructions.

## Eligibility

A destination is eligible only when all conditions hold:

1. The tenant matches the active conversation and requesting worker.
2. The `route_purpose` and `destination_type` are an allowed V1 pairing.
3. The destination is `active` and its approval/policy versions are current.
4. The active channel is inside the destination's channel scope.
5. The referenced worker or human-support route is currently eligible under its
   own lifecycle and authorization contract.
6. Health is `healthy` or an explicitly permitted `constrained` state within
   its freshness limit.
7. The conversation has no higher-precedence safety, consent, lifecycle,
   handoff, or turn-ownership restriction.

Unknown, stale, withdrawn, mismatched, or unavailable state is ineligible. It
must lead to the routing contract's safe-unavailable or uncertain outcome, not
a fallback to another tenant or destination.

## Lifecycle

```text
Draft → Validated → Active → Suspended or Withdrawn → Retired
                 ↘ rollback to a prior approved active version
```

- **Draft:** Saved but not usable for routing.
- **Validated:** Configuration syntax, tenant scope, target reference, channel
  scope, and required policy checks pass.
- **Active:** Approved and eligible subject to current health and routing
  policy.
- **Suspended:** Temporarily unavailable; no new route offers or requests.
- **Withdrawn:** Intentionally removed from routing; existing requests are
  reconciled under Conversation policy.
- **Retired:** Historical record retained according to policy; never eligible.

Only a trusted backend configuration workflow may transition lifecycle state.
The UI can request a transition but cannot activate itself.

## Configuration Operations

| Operation | Authorized role | Required backend checks |
|---|---|---|
| Create draft | Tenant admin | Tenant membership, entitlement, approved destination type, target ownership. |
| Validate | Backend policy service | Schema, target eligibility, channel scope, conflicts, policy compatibility. |
| Approve/activate | Named tenant owner and required platform policy owner | Approval evidence, test status, audit, lifecycle concurrency. |
| Suspend/withdraw | Tenant admin or authorized operations role | Current scope, impact notice, active-request reconciliation. |
| Roll back | Authorized tenant admin | Previous approved version, compatibility, audit, recovery evidence. |
| View | Tenant-scoped admin/operator according to role | Tenant visibility and minimum necessary fields. |

Platform support may assist only through purpose-limited, audited access. It
must not silently alter a tenant's destination or view private route details.

## Client Workspace Experience

The future Front Desk configuration screen should show only:

- a named Support Worker destination;
- a human-support route label and safe public-facing availability state;
- eligible channels;
- version, approval, and current lifecycle status;
- a test-mode validation result; and
- suspend, activate, or rollback actions when the user is authorized.

It must not expose raw target references, private contacts, credentials,
cross-tenant information, queue capacity, or provider configuration.

## Health and Failure Behavior

Health is an eligibility signal, not proof that a destination completed work.

| Condition | Registry behavior | Routing behavior |
|---|---|---|
| Healthy and fresh | Eligible | May offer or request destination. |
| Constrained and fresh | Eligible only if policy permits | May offer a limited/waiting path. |
| Unavailable | Ineligible | Safe-unavailable path. |
| Unknown or stale | Ineligible | Uncertain or safe-unavailable path. |
| Target withdrawn after offer | Revalidate before request | Do not complete request; explain safe outcome. |

## Required Tests

1. Tenant A cannot read, mutate, or route to Tenant B's destination.
2. A non-active, stale, unhealthy, withdrawn, or channel-mismatched record is
   rejected.
3. A client cannot forge `destination_ref`, `target_ref`, health, policy,
   approval, lifecycle, or tenant values.
4. Duplicate activation, withdrawal, and rollback requests are idempotent and
   concurrency-safe.
5. A route offer is revalidated before a route request.
6. Audits contain minimum references and never raw contact, credential, or
   conversation content.
7. The UI renders only authorized, tenant-scoped records and handles
   unavailable/unknown states safely.

## Implementation Order

1. Define the Platform Foundation configuration schema and versioned API.
2. Define the Conversation Routing lookup and eligibility interface.
3. Implement trusted lifecycle, policy, health, audit, and rollback behavior.
4. Add contract, tenant-isolation, authorization, lifecycle, and failure tests.
5. Implement test-only Front Desk route offers with synthetic tenant routes.
6. Add the Client Workspace configuration screen after backend evidence passes.

## Deferred Scope

V1 does not configure multiple queues, skills-based routing, calendars, CRM,
phone-number forwarding, transfers, notifications, provider credentials,
capacity details, cross-channel contact matching, or tenant-defined arbitrary
webhooks.

## Related Documents

- `11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `13_FRONT_DESK_ROUTING_API_CONTRACT.md`
- `10_FRONT_DESK_WORKER_V1.md`
- `09_SHARED_WORKER_BLUEPRINT.md`
- `../03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `../16_PLATFORM_FOUNDATION/README.md`
- `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`

## Revision History

| Version | Date | Changes |
|---|---|---|
| 0.7 | 2026-08-27 | Added atomic withdrawal and active-purpose claim release. |
| 0.6 | 2026-08-27 | Added atomic tenant/purpose active-destination claims and release on suspension. |
| 0.5 | 2026-08-27 | Added atomic optimistic concurrency for test-only destination lifecycle changes. |
| 0.4 | 2026-08-27 | Added test-only health freshness at activation and routing lookup. |
| 0.3 | 2026-08-27 | Connected test-only active destination lookup to the route-request boundary. |
| 0.2 | 2026-08-27 | Implemented the test-only tenant-admin configuration lifecycle with synthetic web-chat scope. |
| 0.1 | 2026-08-27 | Created the planned tenant-scoped Front Desk destination registry. |

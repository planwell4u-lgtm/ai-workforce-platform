# Front Desk Worker V1

**Version:** 0.1
**Status:** Planned
**Date:** 2026-08-27
**Purpose:** Define a narrow first Front Desk Worker that greets visitors,
provides approved general information, and routes them safely without gaining
customer-data, scheduling, sales, or external-action capabilities.

---

## V1 Charter

The Front Desk Worker is a tenant-bound entry worker for a business's public
digital experience. It may greet a visitor, identify a general support need,
answer only from approved public-facing information, and direct the visitor to
the appropriate worker, channel, or human team.

It is a routing and orientation worker. It is not an account-service worker,
appointment scheduler, sales closer, payment processor, or customer-record
lookup service.

## Intended Participant Journey

```text
Visitor starts an approved web-chat or browser-voice interaction
        ↓
Front Desk Worker greets and asks for a general purpose
        ↓
Approved public information answers the request
        ├── Answer available → provide the approved answer
        ├── Supported destination identified → route to the configured worker or human team
        └── Unknown, protected, or unsupported request → explain the limit and offer human support
```

Routing is a request to the canonical Conversation and channel contracts. The
worker does not independently transfer calls, create external records, or claim
that a human has accepted a handoff.

## V1 Scope

| Area | Included in V1 |
|---|---|
| Role | Greeting, orientation, approved general information, and safe routing. |
| Participants | Public web-chat visitors and explicitly consented browser-voice participants. |
| Knowledge | Current tenant's approved, published public FAQ and business-information source. |
| Allowed outcomes | Approved answer, offered route to Support Worker, offered human-support handoff, or safe-unavailable response. |
| Channels | Web chat first; browser voice only through the established explicit-consent boundary. |
| Configuration | Greeting, business hours, approved routing destinations, and human-support destination. |
| Observability | Tenant-scoped interaction outcome, route requested, safe-unavailable outcome, and failure evidence under approved telemetry controls. |

## Explicit Exclusions

V1 does not allow:

- customer, account, order, payment, or identity lookup;
- collection, storage, or verification of personal, account, payment, or order data;
- appointment booking, rescheduling, cancellation, calendar access, or availability claims;
- lead capture, marketing consent, CRM write access, sales qualification, pricing promises, or follow-up;
- ticket creation, refunds, payments, profile changes, purchases, or any other external business action;
- outbound calls, messages, email, SMS, or proactive contact;
- recordings, transcript retention, memory, or customer profiling;
- arbitrary web browsing, database access, API/MCP tools, provider credentials, or unrestricted integrations; or
- autonomous handoff completion claims.

Each excluded capability requires a separate charter, approved contracts,
authorization, implementation, tests, and acceptance evidence.

## Knowledge and Response Rules

1. The worker may answer only from tenant-approved, published public sources.
2. It may give a concise summary only when that source directly supports the
   request.
3. It must not infer business hours, availability, prices, eligibility, or
   policy from incomplete information.
4. When a question is unsupported, account-specific, sensitive, or unclear, it
   must state that it cannot provide that information and offer the configured
   human-support path.
5. It must not solicit protected information to improve routing.

## Routing Rules

| Trigger | Permitted V1 outcome |
|---|---|
| Approved general question | Answer from the approved source. |
| Visitor asks for support | Offer the configured Support Worker or human-support destination. |
| Visitor asks for a person/team | Offer the configured human-support destination. |
| Account, order, payment, or personal-data request | Explain that the worker cannot access or collect it; offer human support. |
| Appointment, purchase, refund, or other action request | Explain that the worker cannot perform the action; offer human support. |
| Unknown or ambiguous request | Ask one non-sensitive clarification or offer human support. |

The configured routing destination must be tenant-scoped, active, and
authorized by the backend. A visible frontend option does not grant routing or
action authority.

## Permissions and Security

- The backend derives tenant, worker version, lifecycle state, and permitted
  routing destinations from trusted configuration.
- Public-channel participation does not prove customer identity or grant
  account-specific access.
- Browser voice requires explicit microphone consent and follows the approved
  voice-session cleanup and failure behavior.
- The worker cannot use a routing hint, model output, client claim, or channel
  metadata as permission to access data or take an action.
- Configuration changes require tenant-admin authorization, versioning, audit,
  validation, and rollback evidence.

## Frontend Configuration Requirements

The future Client Workspace may present these V1 controls:

| Control | Constraints |
|---|---|
| Worker name and greeting | Versioned, previewable, and tenant-scoped. |
| Business hours display | Approved configuration; never an inferred availability promise. |
| Public knowledge source | Published sources only, with provenance and review state. |
| Support Worker destination | Active, tenant-scoped, authorized destination only. |
| Human-support destination | Approved tenant contact/routing configuration only. |
| Test mode | Clearly marked; no production actions, customer data, or external effects. |
| Activate or disable | Named owner approval, audit, health checks, and rollback path. |

## Success Measures

- Visitors receive a clear greeting and safe next step.
- Approved general questions are answered accurately from the approved source.
- Unsupported or sensitive requests reach a clear safe fallback without data
  collection or invented information.
- Routing is requested only for configured, tenant-scoped destinations.
- The worker does not create an external effect or retain prohibited data.

## Acceptance Criteria

Before any activation beyond a controlled test:

1. A public general FAQ question receives only the approved answer.
2. A request for support receives the configured Support Worker or human path.
3. Account, order, payment, appointment, lead, and action requests produce a
   safe human-support response without soliciting protected information.
4. A forged tenant, worker, destination, permission, lifecycle, or channel
   input is denied server-side.
5. Browser-voice consent, deny, disconnect, stop, and recovery paths release
   media and retain the correct interaction outcome.
6. Tests prove that no customer data, credential, external action, recording,
   memory, or unrestricted tool access is introduced.
7. Agent, Conversation, Knowledge, Security, Frontend, Voice, Testing, and
   Operations owners approve the enabled configuration and rollback path.

## Delivery Order

1. Define the tenant-scoped public knowledge and configured human-support
   destination contracts.
2. Define the canonical Conversation routing-request contract; do not create
   direct client-side transfer behavior.
3. Add the Front Desk Worker V1 configuration and evaluation tests.
4. Add a controlled Web Chat test path using the existing shared application
   shell.
5. Add browser-voice only after the chat path passes its safety and routing
   acceptance evidence.
6. Add the Client Workspace Front Desk configuration screen only after the
   backend contracts and authorization controls are defined.

## Deferred Decisions

The following decisions are intentionally deferred and require explicit scope
approval:

- whether appointment requests may be collected or integrated with a calendar;
- whether a Sales Worker receives leads from Front Desk and what consent is
  required;
- whether public visitors may open a support ticket;
- telephone routing, phone-number ownership, provider choice, recording, and
  transfer behavior;
- multilingual behavior, accessibility expansion, and localization policy; and
- production deployment and service-level commitments.

## Related Documents

- `09_SHARED_WORKER_BLUEPRINT.md`
- `11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `07_CUSTOMER_SUPPORT_WORKER_V1.md`
- `../02_AGENT_PLATFORM/04_AGENT_LIFECYCLE.md`
- `../02_AGENT_PLATFORM/14_AGENT_CAPABILITY_MODEL.md`
- `../03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `../05_KNOWLEDGE_PLATFORM/README.md`
- `../10_FRONTEND_PLATFORM/14_FRONTEND_DELIVERY_PLAN.md`
- `../00_CONTROL/ROADMAP.md`

## Revision History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-08-27 | Created the planned narrow Front Desk Worker V1 charter. |

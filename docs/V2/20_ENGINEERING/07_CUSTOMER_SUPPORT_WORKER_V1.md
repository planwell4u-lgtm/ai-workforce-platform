# Customer Support Worker V1

**Status:** V1 web-chat and authorized Jira escalation acceptance passed  
**Date:** 2026-08-24  
**Purpose:** Define the first customer-support worker without widening the
approved data, telephony, or action boundaries.

---

## V1 Charter

The Customer Support Worker may serve authenticated web-chat participants and
inbound phone callers. It may answer a support question only from the current
tenant's approved, published FAQ content. When that content cannot safely
answer the question, it offers human support. An authorized escalation may
create one Jira Service Management request through the existing backend action
boundary.

The worker is not an account-service agent. It does not look up customer or
order records, change any customer state, take a payment, or make an outbound
call.

## Channel Contract

| Channel | Who may use it | Permitted support outcome | Important limit |
|---|---|---|---|
| Web chat | Authenticated, tenant-authorized participant | Approved FAQ answer or human-support handoff | Tenant and permission are derived server-side. |
| Inbound phone | Caller routed by the approved LiveKit-native or Twilio pilot route | Generic approved FAQ answer or human-support handoff | A phone call establishes routing only; it does not prove a customer identity. |

The existing inbound routes remain inbound-only. The normal LiveKit-native
route stays managed-agent-only. The separate-project local-worker proof remains
stopped and isolated; it is not part of this worker's runtime design.

## Knowledge and Response Rules

1. The only answer source is the tenant's approved, versioned support FAQ.
2. The approved Application Data Context Broker may provide at most three
   short, redacted FAQ snippets for `support.answer` during the active,
   correlated interaction. It is read-only and expires within five minutes.
3. The worker may summarize an approved snippet, but must not invent a policy,
   account fact, order status, or promise.
4. If no approved answer is available, the worker says it cannot access that
   information and offers human support. It must not broaden retrieval or use
   another tool as a fallback.
5. It must treat a request for personal, account-specific, payment, or other
   protected information as unavailable and offer the approved handoff.

## Escalation Contract

The worker may request an escalation only through the existing authorized Jira
backend boundary. The backend—not the model, browser, or phone caller—enforces
authorization, required fields, tenant scope, idempotency, audit, and the
result state.

The intended V1 experience is:

```text
Approved FAQ answer available  -> answer in the active conversation
Answer unavailable or human requested
  -> offer human support
  -> authorized escalation request
  -> backend creates or restores one Jira reference
  -> show the confirmed result or an explicitly uncertain/failed state
```

An unauthorized caller or participant cannot create a ticket. A retry must use
the existing idempotency key and must not create a duplicate request. A timeout
or malformed provider response is *uncertain*, not a successful ticket.

## Privacy, Security, and State

- Tenant, permission, agent version, conversation correlation, and knowledge
  scope come from trusted server-side facts. The browser, caller, model output,
  dispatch metadata, and phone number are never authority for application-data
  access.
- Phone numbers are routing inputs, not canonical conversation scope or
  customer identity. Caller-number attributes are ignored for admission.
- FAQ snippets are transient. They are not placed in browser storage, room
  metadata, agent memory, recordings, logs, traces, or provider tools.
- The canonical conversation retains only the approved tenant-scoped
  interaction and action state. Disconnects and provider ambiguity retain the
  established `uncertain` outcome rather than implying completion.
- The worker receives no database connection, arbitrary HTTP/MCP tool,
  credential, transcript, recording, attachment, or customer-profile access.

## Explicit Non-Goals

V1 does not enable:

- customer/account/order lookup or verification;
- payments, refunds, profile changes, or any other business action;
- recordings, transcript retention, memory, or analytics expansion;
- outbound calling, SMS, email, or other proactive contact;
- autonomous Jira creation without the existing authorized action path;
- a local worker sharing a room with the managed telephone agent; or
- production cloud deployment. Deployment remains an end-of-project decision.

Each item above requires a separate design, approvals, implementation, and
acceptance evidence before it can be enabled.

## Acceptance Criteria Before Worker Activation

1. A tenant-authorized web-chat participant receives an answer that is limited
   to the approved FAQ source/version.
2. A phone caller can receive a generic approved FAQ answer, but cannot obtain
   account-specific information or use the phone number as proof of identity.
3. An unknown, unavailable, or protected question produces the approved
   safe-unavailable and human-support response without a broader retrieval.
4. An authorized escalation creates or restores exactly one Jira reference;
   duplicate, unauthorized, cross-tenant, timeout, and provider-failure paths
   remain safe and observable.
5. Tests prove that forged tenant, room, conversation, source, expiry, and
   permission inputs are denied; no prohibited data class appears in agent,
   browser, room, audit, or telemetry output.
6. Channel disconnect, agent unavailability, and routing-capacity conditions
   lead to a defined fallback or uncertain state without a duplicate answer or
   unqualified handoff.
7. Security, Data/Knowledge, Agent, Conversation, Voice, Integration, and
   Testing owners approve the enabled configuration and rollback method.

## Implementation Order

1. Bind one versioned Customer Support Worker configuration to the already
   verified tenant-scoped web-chat path.
2. Reuse the approved FAQ broker and safe-unavailable response; do not add
   sources or tools.
3. Bind the existing authorized, idempotent Jira escalation action behind an
   explicit user/operator authorization check.
4. Add the acceptance and negative-path evidence above.
5. Only then consider the already-verified inbound voice routes as a generic
   support channel. This does not authorize outbound or account-specific use.

## Implementation Record

On 2026-08-24, the protected web-chat route was bound to the explicit
`customer-support-worker:faq-v1` configuration. Its unmatched-question path
now returns the approved human-support message as a normal support response,
with a ticket recommendation, rather than an empty response. This changes no
knowledge source, identity, Jira permission, phone dispatch, or voice route.
The complete Python suite passed (66 tests; 3 environment-dependent skips),
and the frontend lint, build, and rendered-page checks passed. A signed-in
browser rehearsal confirmed both an approved order-tracking FAQ answer and the
safe-unavailable human-support response for an unsupported refund request.
The remaining V1 browser acceptance check is the existing authorized,
idempotent Admin-to-Jira escalation.

The local Admin-to-Jira feedback now treats a ticket as created only when Jira
returns an issue key. Jira rejection is shown as a rejection with no ticket;
an unconfirmed provider outcome is shown as unknown and must be checked in
Jira rather than retried. The complete Python suite then passed (68 tests; 3
environment-dependent skips), alongside frontend lint, build, and rendered-page
checks.

For future failed or unconfirmed escalation attempts, the Admin result includes
only a safe Jira diagnostic code (for example, `jira_rejected_403`). It does
not expose Jira response bodies, credentials, or customer content, and it does
not retry an existing idempotency reference.

The final browser rehearsal passed: an unsupported refund-policy question
received the safe human-support response, and the authorized Admin escalation
created and saved Jira ticket `CS-16`.

## Authoritative References

- `05_READ_ONLY_APPLICATION_DATA_BOUNDARY.md`
- `JIRA_BACKEND_WIRING_RECORD.md`
- `01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../03_CONVERSATION_PLATFORM/06_CONVERSATION_ROUTING.md`
- `06_INBOUND_TELEPHONE_INTEGRATION.md`
- `../00_CONTROL/CURRENT_STATUS.md`

# Sales Worker V1

**Version:** 0.1  
**Status:** Planned  
**Date:** 2026-08-27

## Purpose

Sales Worker V1 is a tenant-bound public web-chat worker for approved product
information and non-sensitive discovery. It may help a visitor understand an
approved offering and request a handoff to a configured human sales team. It
does not capture leads, quote prices, promise discounts, access a CRM, or
contact a visitor.

## Scope

| Area | V1 rule |
|---|---|
| Participant | Public web-chat visitor. |
| Knowledge | Tenant-approved public product, plan, and pricing information only. |
| Allowed outcomes | Approved answer, one non-sensitive discovery question, or an offered human-sales route. |
| Channel | Web chat only. |
| Data | No personal, account, payment, order, or contact details. |
| Actions | No CRM write, email, SMS, call, calendar, quote, purchase, or follow-up. |

## Conversation Rules

1. Answer only from published, tenant-approved sales knowledge.
2. Ask at most one optional, non-sensitive discovery question, such as the
   visitor's broad business goal.
3. Do not ask for name, email, phone number, company identifiers, budget,
   account data, payment data, or purchase timing.
4. Do not infer availability, pricing, eligibility, discounts, legal terms, or
   product capabilities beyond the approved source.
5. When the visitor asks to speak with Sales, requests a quote, or needs an
   unsupported answer, offer the configured human-sales route.
6. A route is an explicit visitor request; it is not a completed human handoff.

## Required Permissions and Configuration

- Tenant scope, worker lifecycle, knowledge publication state, and active
  sales destination are derived server-side.
- Tenant admins may create, validate, activate, suspend, and withdraw only
  test destinations through a dedicated configuration permission.
- Visitors may request a route only through the canonical conversation routing
  contract after the backend verifies tenant scope, route state, and channel.
- A future CRM, telephony, email, calendar, or lead-capture capability requires
  separate consent, integration, authorization, audit, and rollback contracts.

## Explicit Exclusions

- lead/contact capture or consent recording;
- CRM access or writes;
- price quotes, discount offers, negotiations, contracts, or purchases;
- outbound follow-up or marketing;
- account, order, payment, identity, or personal-data access;
- calendar scheduling; and
- autonomous claims that a salesperson accepted a request.

## Acceptance Evidence

1. Approved product questions return only approved content.
2. Unsupported, sensitive, pricing, and action requests receive a safe limit
   and optional human-sales route.
3. Forged tenant, destination, lifecycle, permission, and channel values are
   denied by the backend.
4. No lead data, external action, provider credential, recording, or customer
   profile is created in the test path.
5. Route offer, explicit request, unavailable destination, suspend, withdraw,
   and expiry states are tested.

## Delivery Order

1. Define approved sales knowledge and a tenant-scoped human-sales destination.
2. Add configuration and routing contracts using the Front Desk lifecycle
   pattern.
3. Build the controlled web-chat test path and negative tests.
4. Add consented lead capture only under a separate V2 charter.

## Related Documents

- `09_SHARED_WORKER_BLUEPRINT.md`
- `10_FRONT_DESK_WORKER_V1.md`
- `11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `12_FRONT_DESK_DESTINATION_REGISTRY.md`


# Sales Knowledge and Routing Contract

**Version:** 0.1  
**Status:** Planned  
**Date:** 2026-08-27

## Approved Sales Knowledge

Sales Worker V1 may retrieve only tenant-scoped, published public sales
content. Each entry must have a stable reference, owner, publication state,
reviewed-at time, and approved answer text.

| Content type | Allowed in V1 | Notes |
|---|---|---|
| Product overview | Yes | Factual, published capability descriptions. |
| Plan comparison | Yes | Only exact approved plan descriptions. |
| Published price | Yes | Exact public price and currency; no quote or discount inference. |
| Case study | Yes | Published, approved customer story only. |
| Availability, discount, quote, contract | No | Requires human sales review. |
| Customer/contact/CRM information | No | Not collected or retrieved. |

If no single approved entry directly supports the response, the worker must
say it cannot confirm that information and may offer a human-sales route.

## Human-Sales Destination

The destination record is tenant-scoped and contains only:

- opaque destination reference;
- route purpose: `human_sales`;
- channel scope: initially `web_chat` only;
- lifecycle: draft, validated, active, suspended, or withdrawn;
- health state and short-lived health expiry; and
- configuration version and audit evidence.

The record must not include a phone number, email address, provider credential,
CRM identifier, personal assignee, or a promise of human availability.

## Route Request

```text
Visitor asks an approved sales question
        ↓
Approved answer available → answer from the source
        ↓
No approved answer, quote, pricing exception, or explicit Sales request
        ↓
Worker offers the active human-sales destination
        ↓
Visitor explicitly requests route
        ↓
Backend records a tenant-scoped route request
```

The request creates no CRM lead, message, call, email, calendar event, or
assignment. A separate integration contract is required for each such action.

## Initial Test Cases

1. An exact approved product question returns only the matching source answer.
2. A price, quote, discount, contract, or competitor request without an exact
   approved answer offers human sales rather than inventing an answer.
3. A visitor can request an active human-sales route explicitly.
4. Draft, suspended, withdrawn, expired, mismatched, or forged destinations
   produce a safe-unavailable result.
5. A request containing contact or account data is not collected or retained.

## Deferred Decisions

- consent wording and retention for lead capture;
- selected CRM and its write contract;
- email, SMS, phone, or calendar provider;
- sales-assignee selection and acceptance state; and
- production pricing, quotation, and commercial policy.

## Related Documents

- `14_SALES_WORKER_V1.md`
- `09_SHARED_WORKER_BLUEPRINT.md`
- `11_FRONT_DESK_ROUTING_REQUEST_CONTRACT.md`
- `12_FRONT_DESK_DESTINATION_REGISTRY.md`


# Sales Worker API Contract

**Version:** 0.1  
**Status:** Planned  
**Date:** 2026-08-27

## Endpoint

`POST /v1/sales-answers`

The endpoint is test-only and accepts an authenticated web-chat request.
It requires `agent.context.read`; tenant scope and membership are derived by the
backend, never accepted from the client.

## Request

```json
{
  "agent_ref": "sales-worker",
  "session_ref": "opaque-client-session",
  "event_ref": "client-idempotency-reference",
  "sequence": 1,
  "question": "What is the price of the Meadow Linen Kurta?"
}
```

The client must not supply tenant, knowledge-source, destination, lead,
contact, price override, model, tool, or provider fields.

## Success Response

```json
{
  "answer": "The Meadow Linen Kurta is ... Demo price: PKR 4,900.",
  "source_ref": "sales-catalog:v1:1",
  "human_sales_recommended": false,
  "conversation_ref": "opaque-reference",
  "correlation_ref": "opaque-reference"
}
```

## Safe Fallback

When no exact approved entry matches, return a fixed safe message and set
`human_sales_recommended` to `true`. Do not create a lead, request contact
details, generate a price quote, or claim that Sales will respond.

## Error Rules

- `401`: missing or invalid access token;
- `403`: missing membership or required permission;
- `400`: malformed request;
- `409`: duplicate or invalid conversation turn; and
- `5xx`: internal failure without exposing provider, tenant, catalog, or
  credential details.

## Non-Goals

This endpoint does not implement CRM access, lead capture, provider calls,
telephony, email, SMS, calendar scheduling, or human assignment.


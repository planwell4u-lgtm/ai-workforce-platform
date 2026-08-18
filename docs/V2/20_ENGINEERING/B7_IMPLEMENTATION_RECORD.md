# B7 Implementation Record — Bounded Support-Ticket Action

The agent requests a local support-ticket action through `integration.support-ticket.create`. Requests require tenant, Conversation, summary, and idempotency references. The local simulator records `pending`, `succeeded`, `failed`, and `uncertain` separately; a timeout never triggers automatic resend or becomes success.

# Jira Service Management Backend Wiring Record

**Date:** 2026-08-17  
**Status:** Implemented locally; ready for configured staging validation.

## Implemented boundary

- The simulated support-ticket action is replaced by a Jira Service Management
  customer-request client at `POST /rest/servicedeskapi/request`.
- The client sends the configured service-desk ID, request-type ID, and request
  summary over HTTPS using the dedicated service-account email and API token.
- A successful response must contain Jira's `issueKey`; this is returned as the
  ticket reference.
- Authorization, required request fields, and in-process idempotency are
  enforced before a provider call. Definitive Jira rejections are `failed`;
  network and malformed-response outcomes are `uncertain`.

The next full-flow wiring must persist the idempotency/result record in
PostgreSQL so it survives backend restarts.

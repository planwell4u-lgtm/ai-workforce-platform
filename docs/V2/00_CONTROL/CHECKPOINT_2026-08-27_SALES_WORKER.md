# Checkpoint — Sales Worker Test Path

**Date:** 2026-08-27
**Status:** Completed — local Sales chat acceptance passed

## Completed

- Customer Support baseline: approved FAQ-only replies and safe fallback.
- Front Desk test path: tenant-admin destination lifecycle, active Support and
  Human Support routes, explicit customer route request, and safe-unavailable
  behavior.
- Fictional internal retail Sales catalog created and validated.
- Sales Worker core created: deterministic approved-catalog matching and fixed
  Human Sales fallback; focused agent tests pass.
- Protected `POST /v1/sales-answers` endpoint is wired into the local backend.
- Local backend is configured with the fictional catalog through a read-only
  mount and `SALES_CATALOG_PATH`.
- Sales chat screen built and available at `/sales`.
- Auth0 now permits `http://localhost:3000/sales` as both a callback and
  logout URL for the local SPA test path.
- Signed-in Sales acceptance passed for the fictional Meadow Linen Kurta
  catalog answer and the fixed discount/custom-quote fallback.
- The customer-facing Human Sales test route was added, activated, and tested
  through both availability checking and request recording. No customer
  details, external provider, or actual human handoff is involved.

## Next Session Start Here

The Sales Worker test path is complete. The test-only administrator flow now
lists Human Sales requests and supports `new → reviewed → closed` local state,
plus a five-minute test-route health renewal action. No real handoff occurs.

HubSpot lead flow completed in local staging:

- A HubSpot private-app token is stored locally in `.env` and must never be
  committed or displayed.
- One owner-approved test contact was created and assigned in HubSpot.
- The protected server-side lead endpoint accepts only name, email, explicit
  consent, and an idempotency reference. The private-app token remains
  server-side.
- Auth0 API, application, role, and tenant membership permissions now include
  `integration.crm.lead.create`; the Sales page requests this scope.
- Lead outcomes are tenant-scoped and idempotently recorded. Focused fake-client
  tests pass.
- One owner-approved local acceptance submission returned `201 Created` and
  created the requested HubSpot contact. No contact details are recorded here.
- The Sales form keeps a stable idempotency reference for unchanged retry
  attempts and resets it only when the name or email changes or after a
  confirmed success. The complete Python suite passed (91 tests; 3 expected
  skips), as did the frontend build, rendered-page tests, and lint (one
  existing unrelated warning).
- The HubSpot private app is limited to `crm.objects.contacts.read` and
  `crm.objects.contacts.write`; it has no broader CRM scopes.

Any future real contact creation still requires explicit customer consent and
fresh owner approval at the moment of a manual acceptance test.

## Explicitly Deferred

- CRM/contact capture, lead consent, quotes, discounts, pricing overrides;
- outbound calls, SMS, WhatsApp, email, and telephony; and
- production catalogs or content from any real retailer.

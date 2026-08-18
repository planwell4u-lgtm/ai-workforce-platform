# Current Project Status

**Version:** 2.8  
**Status:** Active  
**Phase:** First Vertical Slice — Chat, Admin, and Jira flow active  
**Last Updated:** 2026-08-18

---

# Purpose

This is the concise operational snapshot for contributors. `10_PROJECT_STATUS.md` is the detailed authoritative status record; this file must remain aligned with it.

# Current State

The approved V2 architecture and engineering planning are complete. Auth0 JWT validation, Supabase PostgreSQL persistence, Jira ticket creation, and the protected tenant-scoped FAQ support flow are verified in staging.

The initial Architecture Diagrams set (01-07) has validated editable Draw.io sources and matching SVG review exports. PNG exports and reviewer metadata remain required before individual diagrams are fully approved.

# Completed

- Control, architecture, and module documentation sets through Operations, Deployment, Observability, Testing, Examples, and Engineering.
- First vertical-slice implementation backlog, workspace/module-boundary standard, delivery workflow, and traceability standard.
- Initial seven-diagram source/SVG set.
- B1 tenant-aware Auth0-protected API entry with durable audit evidence.
- B2 tenant-safe PostgreSQL records and migrations in Supabase staging.
- B3 approved, versioned staging FAQ source and protected support-answer flow.
- B7 Jira Service Management ticket creation, including authenticated Supabase-to-Jira verification.
- B4 canonical conversation control with PostgreSQL-backed persistence, duplicate protection, and refresh restoration.
- B5 Auth0-protected web chat and tenant-scoped Admin conversation history.
- Admin-to-Jira escalation verified; backend idempotency is active. The Admin view reloads the saved Jira reference from the tenant-scoped action record and disables repeat escalation.
- Configured-staging chat, persistence refresh, Admin history, Jira reference restoration, and repeat-escalation suppression were verified on 2026-08-18.
- Backend and frontend Linux container builds are validated locally and in GitHub Actions; a release-candidate workflow produces image archives, checksums, and source/workflow provenance metadata.
- First GitHub Container Registry release candidate published from revision `432b6c12febbf09237d3ab74aed7267aaea4b7a2`; both immutable image digests were keylessly signed and verified through Sigstore/Cosign GitHub OIDC.
- Local Docker rehearsal confirmed backend health (`200 OK`) using the locally built source-equivalent image, runtime configuration, and a read-only mount of the approved FAQ source. The temporary test container was removed after the check.
- Local container configuration is now runtime-configurable: the frontend reads Auth0 and API settings from its `/runtime-config` endpoint at launch. Local backend health and frontend delivery were revalidated on ports `8080` and `3000` respectively.
- Auth0 sign-in through the local frontend was verified after the runtime-configuration change. The protected backend restored conversation history and returned Admin history successfully (`200` responses).
- The full local Docker user flow is verified: approved order-tracking response, Jira escalation (`CS-13`), Admin-history restoration, persisted Jira reference, and repeat-escalation suppression.
- The Admin escalation control now gives immediate progress feedback: it shows `Creating Jira ticket…` and prevents a second click until the request completes.
- The updated escalation feedback was visually verified in the local Docker rehearsal; a fresh conversation created Jira ticket `CS-14`, persisted the reference, and returned to the completed disabled state.
- Updated release candidate published from revision `7f7d2195dea1c5fff8da80aebe26b4aa4b4e72b1`; its backend and frontend image digests were keylessly signed and verified through Sigstore/Cosign GitHub OIDC.
- Local GitHub Container Registry read access is verified. The exact updated signed backend and frontend image digests were pulled and started locally; backend health and frontend runtime-configuration checks both returned `200`.
- The unused `pgadmin-container` was removed at the owner's request, freeing local port `8080` for the backend rehearsal.

# Rehearsal Gaps

- Local pull access to the signed GitHub Container Registry image returned `403 Forbidden`; the package needs a permitted local read identity before exact-digest testing can occur.
- The already-published signed frontend image predates the runtime-configuration fix. A new release candidate is required after local browser verification.

# Next Action

Complete the signed-image browser rehearsal: Auth0 sign-in, chat response, Admin history, and persisted ticket-state check.

# Session Checkpoint

The local backend and frontend rehearsal containers are running on ports `8080`
and `3000` from the exact updated signed image digests; their health and runtime
configuration are verified. Complete the signed-image browser rehearsal before
considering this local release validation closed.

# Delivery Guardrails

- Preserve tenant, identity, authorization, data, contract, and recovery boundaries.
- Use approved sandboxes or simulations for external effects until release authority is granted.
- Record implementation decisions and evidence in the repository, not only in chat or review comments.
- Keep diagram PNG/reviewer finalization separate from changes to approved architecture.

# Related Documents

- `10_PROJECT_STATUS.md`
- `02_PROJECT_ROADMAP.md`
- `../20_ENGINEERING/01_FIRST_VERTICAL_SLICE_IMPLEMENTATION_BACKLOG.md`
- `../20_ENGINEERING/02_ENGINEERING_WORKSPACE_AND_MODULE_STRUCTURE.md`

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.8 | 2026-08-18 | Enabled local GHCR package read access and verified the exact updated signed images start locally with healthy backend and frontend runtime configuration. |
| 2.7 | 2026-08-18 | Published, keylessly signed, and verified the updated release candidate containing the runtime-configuration and escalation-feedback fixes. |
| 2.6 | 2026-08-18 | Visually verified the escalation feedback and completed ticket state in a fresh local Docker conversation (Jira CS-14). |
| 2.5 | 2026-08-18 | Added visible in-progress feedback and repeat-click suppression while a Jira ticket escalation is being created. |
| 2.4 | 2026-08-18 | Verified the complete local Docker support flow: approved answer, Jira ticket CS-13, Admin restoration, persisted ticket state, and repeat-escalation suppression. |
| 2.3 | 2026-08-18 | Verified local container Auth0 sign-in, protected conversation restoration, and Admin history after the runtime-configuration fix. |
| 2.2 | 2026-08-18 | Added runtime-configurable frontend container settings, validated local backend/frontend delivery, and recorded the owner-approved pgAdmin container removal. |
| 2.1 | 2026-08-18 | Recorded local Docker backend-health rehearsal result and the three gaps blocking full signed-image browser verification. |
| 2.0 | 2026-08-18 | Added end-of-session checkpoint: release candidate evidence is pushed and the controlled deployment rehearsal is the restart point. |
| 1.9 | 2026-08-18 | Published, signed, and verified the first GitHub Container Registry release candidate; recorded exact immutable image digests and provenance evidence. |
| 1.8 | 2026-08-18 | Configured keyless Sigstore/Cosign GitHub OIDC signing for versioned GitHub Container Registry release candidates. |
| 1.7 | 2026-08-18 | Validated backend and frontend container builds locally and in GitHub Actions; release-candidate packaging workflow added. |
| 1.6 | 2026-08-18 | Verified the configured-staging chat, persistence, Admin, Jira-reference, and repeat-escalation flow. |
| 1.5 | 2026-08-18 | Completed durable Admin ticket-state display and repeat-escalation suppression; staging end-to-end verification is next. |
| 1.4 | 2026-08-18 | Recorded durable chat, Admin history/status, and Jira escalation; noted remaining ticket-state UI work. |
| 1.3 | 2026-08-17 | Recorded verified Auth0, Supabase, Jira, and protected FAQ support-answer staging flows; set B4 as next. |
| 1.2 | 2026-08-09 | Recorded B0 Engineering Foundation completion and set B1 tenant-aware identity/API entry as next action. |
| 1.1 | 2026-08-09 | Reconciled the concise status with completed documentation/Engineering planning and B0 as next action. |
| 1.0 | 2026-08-05 | Created the initial project-status snapshot. |

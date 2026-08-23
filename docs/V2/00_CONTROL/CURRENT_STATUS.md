# Current Project Status

**Version:** 5.12
**Status:** Active  
**Phase:** First Vertical Slice — Chat, Admin, and Jira flow active  
**Last Updated:** 2026-08-23

---

# Purpose

This is the concise operational snapshot for contributors. `10_PROJECT_STATUS.md` is the detailed authoritative status record; this file must remain aligned with it.

# Current State

The approved V2 architecture and engineering planning are complete. Auth0 JWT validation, Supabase PostgreSQL persistence, Jira ticket creation, and the protected tenant-scoped FAQ support flow are verified in staging.

The initial Architecture Diagrams set (01-07) has approved editable Draw.io sources, matching SVG and PNG review exports, and recorded reviewer metadata.

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
- B6 local Voice adapter simulation with canonical Conversation correlation and safe interrupted/disconnected turn handling.
- Admin-to-Jira escalation verified; backend idempotency is active. The Admin view reloads the saved Jira reference from the tenant-scoped action record and disables repeat escalation.
- B8 tenant-scoped operator status and controlled escalation journey with separate view/escalation permissions.
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
- The signed-image browser rehearsal is complete: Auth0 sign-in, conversation restoration, a protected support-answer request, and Admin-history loading all completed successfully against the exact signed images.
- B9 local release-readiness evidence is complete: immutable signed images, provenance, exact-digest local rehearsal, health/configuration checks, and protected browser-flow evidence are retained.
- LiveKit local realtime-media sandbox is running and reachable on ports `7880` and `7881` for the approved provider evaluation; Twilio and cloud deployment remain out of scope.
- A test-only LiveKit adapter now connects to the local sandbox through the provider-neutral Voice boundary and preserves `uncertain` turn outcome on disconnect; focused tests and the backend container build pass.
- A signed-in local browser voice test is implemented: the backend issues a five-minute, room-bound LiveKit token after tenant and support-read authorization; the browser publishes a brief synthetic tone without requesting microphone access or receiving a provider secret.
- The signed-in LiveKit browser rehearsal passed: the browser published synthetic local audio, LiveKit received 76 RTP packets over about 1.5 seconds, and the room closed cleanly. Docker Desktop local media requires `7882/udp` exposed with LiveKit advertising `127.0.0.1`.
- The approved user-facing microphone design is implemented and locally verified: explicit consent precedes browser permission; microphone audio uses echo cancellation, noise suppression, and auto-gain; Stop, Cancel, denied/failure, and sign-out cleanup release the microphone and disconnect. LiveKit received 565 microphone RTP packets without loss, followed by a clean user-requested stop.
- The two-participant local voice rehearsal passed: a host joined with microphone consent and a second, same-user browser session joined the tenant-scoped room as a listener without microphone access. LiveKit confirmed the listener subscribed to the host track and forwarded RTP; the owner confirmed audible playback. Each token uses a distinct temporary participant identity so the second session does not displace the first.
- The denied-microphone recovery rehearsal passed: browser-level microphone denial produced the explicit "nothing was shared" state and returned the control to Start voice; after permission was restored, a new microphone session connected successfully.
- The local scripted browser-agent rehearsal passed: an explicitly requested `local-agent-...` room admitted a separate programmatic LiveKit participant, which published an offline synthesized greeting that the owner heard in the browser. This proves the independent agent participant and playback path only; it does not process support data, record audio, or call an AI service.
- A real LiveKit Cloud Agent Builder browser rehearsal passed with managed voice models. The owner confirmed normal conversational behavior using generic, safe prompts; the proof used no actions, data collection, secrets, application-data connection, telephony, or recording.
- The protected local-browser-to-LiveKit-Cloud integration passed. The backend issues a five-minute room-bound token for a unique private Cloud room and explicitly dispatches the deployed Cloud agent; the browser receives no Cloud API secret. The owner confirmed the agent joined, spoke naturally, and safely answered an order-tracking question. No application data, tools, actions, recording, or telephony were enabled.
- Repository Quality recovery and the Cloud voice integration are merged on `main`. The Cloud browser recovery rehearsal passed: Stop/Start reconnected successfully, browser refresh released the microphone and returned to a safe signed-out state, and browser-level microphone denial shared nothing; after permission was restored, a new Cloud voice session spoke normally.
- The local frontend now retains the Auth0 session cache across a browser refresh. The signed-in browser rehearsal verified that refresh restored the session while ending microphone sharing; a new local voice session then started and stopped cleanly.
- The approved read-only Cloud-agent FAQ context boundary is locally verified: an order-tracking answer matched the approved excerpt, and an unmatched refund-policy topic safely offered human support without inventing an answer or taking an action.
- Exact signed-release rehearsal passed for `v0.2.0-rc.1`: the corrected runtime Auth0 configuration authenticated successfully, the Cloud agent received the explicit order-tracking FAQ topic, audio was received, and Stop released microphone sharing.
- The owner-designated LiveKit phone number is active with an inbound-only individual-room dispatch rule for the existing support agent. The controlled inbound caller rehearsal passed: LiveKit recorded the inbound room/session and the owner heard the agent. Recording, actions, outbound calling, and Twilio are not enabled.
- B11 local telephone admission primitives are implemented and tested: only configured called-number-to-tenant routes create canonical Conversations, telephone numbers are excluded from canonical session scope, unknown routes fail closed, and disconnected output remains uncertain. The active LiveKit pilot route is unchanged.
- The local LiveKit telephone event adapter is implemented and tested: only SIP participants with a valid called-number attribute reach B11 admission, and caller-number attributes are ignored.
- The local inbound-telephone worker harness is implemented and tested: it keeps one interaction per call, rejects cross-room call-reference reuse, and clears disconnected calls with uncertain output. It has no LiveKit Agents runtime, media, model, data, or live-routing dependency.
- The local LiveKit Agents admission entrypoint is implemented with a distinct non-pilot agent name. It waits only for a SIP participant, derives provider call identity from SIP attributes, and invokes the B11 harness; no model, media, recording, transcript, data, action, or outbound-call capability is enabled.
- A controlled temporary dispatch to the local non-pilot worker did not create a LiveKit room or session: the inbound call was accepted by LiveKit but rang until closed. A separate empty-room explicit dispatch did reach the same worker, proving its registration and handler startup. The failure is isolated to LiveKit Phone Number/SIP dispatch to a self-hosted worker. The worker was stopped and the known-good pilot dispatch was restored and verified.
- The unused `pgadmin-container` was removed at the owner's request, freeing local port `8080` for the backend rehearsal.

# Deployment Decision

There are no active local-release gaps. Cloud deployment is an end-of-project
release activity and remains deferred until the project is otherwise complete
and release authority is explicitly granted.

# Next Action

Choose a safe real-call test route: a second non-pilot phone number, or a
temporary, explicitly approved switch of the existing pilot dispatch rule.
The verified local changes are published as signed release candidate
`v0.2.0-rc.1`. Cloud deployment occurs only at the end of the project;
application-data access, actions, outbound calling, and Twilio remain
separately deferred.

# Session Checkpoint

The local backend and frontend rehearsal services are running on ports `8080`
and `3000`; their runtime configuration, protected browser flow, Auth0
refresh restoration, consent-based microphone publishing, and two-participant
playback are verified. Cloud deployment remains deferred.

The owner approved the recommended sequence to evaluate a LiveKit-managed
inbound phone number before considering Twilio. Before telephony, the local
scripted browser-agent proof, Cloud Console conversational rehearsal, and
protected local-browser-to-Cloud-agent rehearsal are complete.
The owner has approved the pilot-number rental and inbound routing, and the
controlled inbound caller rehearsal is complete. Application-data expansion,
actions, outbound calling, and Twilio remain separately gated.

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
| 5.14 | 2026-08-23 | Verified that direct empty-room dispatch reaches the local worker, then repeated the handset test. SIP dispatch still created no room/session; normal pilot route restored. |
| 5.13 | 2026-08-23 | Controlled local-worker telephone test failed safely: the call created no room/session; stopped the diagnostic worker and restored the verified pilot dispatch. |
| 5.12 | 2026-08-23 | Started the separate local LiveKit Agents admission worker with a test-only tenant mapping; active pilot routing remains unchanged. |
| 5.11 | 2026-08-23 | Added the local LiveKit Agents SIP-admission entrypoint with a non-pilot agent name and no media, model, data, action, or call capability. |
| 5.10 | 2026-08-23 | Added and tested the local inbound-telephone worker harness: call idempotency, scope-conflict rejection, and uncertain disconnect cleanup. |
| 5.9 | 2026-08-23 | Added and tested the local LiveKit SIP-event adapter: valid called-number admission only, with caller attributes ignored. |
| 5.8 | 2026-08-23 | Implemented and tested provider-neutral inbound-call admission: configured tenant routing, canonical Conversation creation, fail-closed unknown routes, and uncertain disconnect handling. |
| 5.7 | 2026-08-23 | Completed the controlled inbound LiveKit phone rehearsal: the owner heard the dispatched support agent and LiveKit recorded the inbound room/session. |
| 5.6 | 2026-08-23 | Activated the owner-designated LiveKit inbound phone pilot and support-agent dispatch; one inbound caller rehearsal remains. |
| 5.5 | 2026-08-23 | Recorded the owner decision that cloud deployment is an end-of-project release activity, not an active delivery scope. |
| 5.4 | 2026-08-23 | Completed exact signed-release Cloud-agent rehearsal: Auth0 runtime configuration, explicit FAQ topic, received audio, and clean microphone stop all passed. |
| 5.3 | 2026-08-23 | Published signed release candidate `v0.2.0-rc.1` from `4bdf72ff377bfdcac360f82149b7bff020bd591f`; backend and frontend images, keyless signatures, verification, and provenance artifact succeeded. |
| 5.2 | 2026-08-23 | Full backend suite and frontend checks passed after FAQ-context, Auth0-refresh, diagram, and browser-flow work; release publication remains separately authorized. |
| 5.1 | 2026-08-23 | Recorded Taj's final approval for diagrams 01–07; the diagram PNG and reviewer-metadata finalization is complete. |
| 5.0 | 2026-08-22 | Completed local acceptance of the approved read-only FAQ context boundary: approved-answer and safe-unavailable rehearsals passed. |
| 4.9 | 2026-08-22 | The owner confirmed the Cloud agent's spoken order-tracking answer matched the approved FAQ context; unmatched-topic safe-unavailable rehearsal remains. |
| 4.8 | 2026-08-22 | Implemented the constrained FAQ-context dispatch and verified its protected Cloud-agent browser transport; content and safe-unavailable rehearsals remain. |
| 4.7 | 2026-08-22 | Recorded explicit approval for the constrained read-only support-FAQ context boundary; implementation and tests are next. |
| 4.6 | 2026-08-22 | Added the proposed, separately gated read-only application-data boundary; cross-owner approval is required before implementation or support-data connection. |
| 4.5 | 2026-08-22 | Verified local Auth0 refresh restoration: refresh stopped microphone sharing, restored the signed-in session, and a new local voice session started and stopped cleanly. |
| 4.4 | 2026-08-22 | Configured local Auth0 session caching across browser refresh; frontend build and automated safety checks pass, pending signed-in browser rehearsal. |
| 4.3 | 2026-08-19 | Merged the Cloud voice integration and verified browser recovery: stop/start reconnect, refresh microphone release, and microphone deny/re-allow recovery. |
| 4.2 | 2026-08-19 | Merged the repository Quality recovery; rebased the verified Cloud voice integration on it in draft PR #1. GitHub checks are queued before the Cloud voice change is merged. |
| 4.1 | 2026-08-19 | Verified the protected local-browser-to-LiveKit-Cloud-agent journey: private server-issued room token, explicit dispatch, browser playback, and safe order-tracking response; Cloud agent has no application-data tools, recording, or telephony. |
| 4.0 | 2026-08-19 | Verified a real LiveKit Cloud Agent Builder browser conversation with managed voice models and generic safe prompts; set the next scope decision to local-app integration or further Console safety testing. |
| 3.9 | 2026-08-19 | Verified a separate local scripted LiveKit participant publishes an offline browser-playable greeting; set the credential and provider decision for the real browser conversational-agent rehearsal as next. |
| 3.8 | 2026-08-18 | Approved the sequence for a controlled LiveKit Cloud inbound-phone rehearsal before any Twilio evaluation; recorded account, number, routing, and calling as separately gated external actions. |
| 3.7 | 2026-08-18 | Verified denied-microphone recovery: denial shared nothing and returned to a retryable state; restoring browser permission started a new live session. Local LiveKit evaluation is complete. |
| 3.6 | 2026-08-18 | Verified two-participant local voice playback: a listener joined the tenant-scoped room without microphone access, LiveKit forwarded the host audio, and the owner confirmed playback. Denied-microphone recovery is next. |
| 3.5 | 2026-08-18 | Implemented and verified consent-based microphone publishing and explicit recovery/cleanup; recorded playback as the remaining two-participant local test. |
| 3.4 | 2026-08-18 | Verified the signed-in browser synthetic-audio rehearsal end to end; recorded the required local Docker UDP and advertised-address settings. |
| 3.3 | 2026-08-18 | Implemented the secure local browser LiveKit test path: five-minute room token, synthetic audio only, no microphone capture or provider-secret exposure. |
| 3.2 | 2026-08-18 | Implemented and tested the local LiveKit sandbox adapter; connection/disconnection preserves canonical uncertain-turn safety and the backend image builds with the Voice package. |
| 3.1 | 2026-08-18 | Started and recorded the bounded local LiveKit realtime-media sandbox evaluation; Twilio and cloud deployment remain deferred. |
| 3.0 | 2026-08-18 | Reconciled B6 Voice, B8 operator journey, and B9 local release-readiness completion; marked local release gaps resolved and set the next provider-selection decision. |
| 2.9 | 2026-08-18 | Completed the exact signed-image local browser rehearsal: Auth0 sign-in, restored conversation, protected support request, and Admin history all succeeded. |
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

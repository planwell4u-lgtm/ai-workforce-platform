# Current Project Status

**Version:** 5.48
**Status:** Active  
**Phase:** First Vertical Slice — Chat, Admin, and Jira flow active  
**Last Updated:** 2026-09-01

---

# Purpose

This is the concise operational snapshot for contributors. `10_PROJECT_STATUS.md` is the detailed authoritative status record; this file must remain aligned with it.

# Current State

The approved V2 architecture and engineering planning are complete. Auth0 JWT validation, Supabase PostgreSQL persistence, Jira ticket creation, and the protected tenant-scoped FAQ support flow are verified in staging.

The local authenticated web-chat rehearsal and the isolated Cloud voice-agent FAQ rehearsal both pass. The voice rehearsal used explicit microphone consent and ended with microphone sharing released.

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
- The signed-in local web chat returned both its safe-unavailable response and the approved order-tracking FAQ response after the backend database connection was restored.
- The isolated `customer-support-realtime-v1` Cloud voice rehearsal received the approved order-tracking FAQ context, produced caller-audible audio, and ended with the microphone released. No phone routing, recording, tools, customer-data access, escalation, or outbound calling was enabled.
- Local runtime reliability hardening is verified: the Supabase SSL requirement is explicit, the automated health/runtime preflight passes, and the interactive Auth0 staging runner now targets `customer-support-worker` and returns an approved FAQ answer. The local restart and recovery procedure is recorded.
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
- The owner-designated LiveKit phone number is active with an inbound-only individual-room dispatch rule for the existing support agent. The controlled inbound caller rehearsal passed: LiveKit recorded the inbound room/session and the owner heard the agent. Recording, actions, outbound calling, and Twilio integration are not enabled.
- B11 local telephone admission primitives are implemented and tested: only configured called-number-to-tenant routes create canonical Conversations, telephone numbers are excluded from canonical session scope, unknown routes fail closed, and disconnected output remains uncertain. The active LiveKit pilot route is unchanged.
- The local LiveKit telephone event adapter is implemented and tested: only SIP participants with a valid called-number attribute reach B11 admission, and caller-number attributes are ignored.
- The local inbound-telephone worker harness is implemented and tested: it keeps one interaction per call, rejects cross-room call-reference reuse, and clears disconnected calls with uncertain output. It has no LiveKit Agents runtime, media, model, data, or live-routing dependency.
- The local LiveKit Agents admission entrypoint has a distinct non-pilot agent name and is admission-only: it creates no media session, audio subscription, turn detector, model, recording, storage, action, or generated response. When co-dispatched into a room with the managed agent, LiveKit still broadcasts that room's transcript data stream to all participants; the worker ignores it without callbacks or content logging and is stopped pending a stricter isolation design.
- LiveKit Phone Number dispatch does reach the local worker and deliver a SIP participant. The safe B11 admission then fails closed because this managed-phone flow does not supply the expected called-number attribute. The known-good pilot route is restored and the local worker is stopped pending an approved trusted route-binding design.
- The normal managed LiveKit phone route was rechecked successfully: the owner heard the support agent on an inbound call. This confirms the phone-number, individual dispatch-rule, and managed-agent path remain healthy.
- A privacy-safe local-worker diagnostic is ready for one controlled retry. It records only dispatch-metadata presence/length and SIP attribute names—not phone numbers, audio, metadata contents, transcripts, recordings, or secrets. Focused telephone tests pass (12 tests).
- A separate Twilio free-trial inbound Voice rehearsal passed: the owner's verified handset called the trial number, received the required trial notice, and received the selected test response. No API key, custom code, recording, data access, or external application routing was created.
- The earlier Twilio Console upgrade gate was a console-routing issue, not a trial entitlement block. The legacy Console allowed creation of one trial Elastic SIP Trunk without an upgrade or API credentials.
- The trial trunk has LiveKit Cloud's project SIP endpoint configured as its enabled inbound Origination URI. The Twilio trial number is attached to the trunk, so inbound routing is active; the existing LiveKit-native number route remains unchanged.
- A separate LiveKit inbound trunk accepts only the configured Twilio trial number and trusted Twilio SIP signaling and media ranges. Its dedicated individual-room dispatch rule is scoped to that trunk and dispatches the existing support agent; the working LiveKit-native phone-number rule was not changed.
- One trial inbound call reached the Twilio-specific LiveKit room and the existing agent produced its configured greeting. The caller reported continued ringing, so the trusted Twilio media range was added before the next controlled retry. No recording, data access, tools, or outbound calling was enabled.
- The controlled retry passed: the owner heard the greeting and held a responsive conversation with the existing support agent over the Twilio-to-LiveKit route. Recording, data access, tools, and outbound calling remain disabled.
- The native-number local-worker admission now supports an exact, deployment-configured LiveKit dispatch-metadata route when the managed-number SIP participant omits the called-number attribute. Unknown or missing metadata still fails closed, caller attributes remain ignored, and 11 focused telephone tests pass. The active native-number dispatch is not yet pointed to this local worker.
- The controlled native-number rehearsal reached the local worker and validated the exact dispatch token. LiveKit supplied an unusable called-number field, so the trusted fallback was extended to invalid as well as missing values. The hardened worker admitted the final call without media processing, but LiveKit broadcast the managed agent's transcript data stream to the co-dispatched participant; the worker ignored it and was stopped immediately. The native admission route is functionally fixed, while concurrent use with the managed agent requires a stricter isolation decision.
- The approved isolated-number attempt was blocked by the LiveKit project phone-number quota before any rental or usage charge was created. The native dispatch rule was restored to the managed support agent only, and the local worker remains stopped.
- A separate LiveKit project was created for the isolation proof with its included first local number and a local-worker-only dispatch rule. The hardened admission-only worker connected only to that project; one controlled call reached it, supplied the exact trusted dispatch token, and admitted without error or co-dispatched transcript traffic. The worker was stopped immediately after the proof.
- The unused `pgadmin-container` was removed at the owner's request, freeing local port `8080` for the backend rehearsal.
- The separate `customer-support-realtime-v1` LiveKit agent source is configured for the OpenAI Realtime API. It has no tools, customer-data access, recording, transcript persistence, escalation, outbound calling, deployment, or dispatch-rule change. Local configuration recognition and the complete Python suite pass (71 tests; 3 environment-dependent skips).
- The LiveKit Cloud deployment attempt for `customer-support-realtime-v1` was blocked before agent creation because the account has reached its agent limit (`1/1`). The target project has no listed deployment to replace. No OpenAI key was stored in LiveKit Cloud, and no phone route or call changed.
- CLI evidence then showed that the local `LIVEKIT_CLOUD_*` credentials target a different LiveKit project than the browser's `Planwell Local Worker Isolation` project. That credential-target project contains the existing managed `customer-support-1fc2` agent and two incomplete unnamed `Setting Up` agent records from the failed deployment attempts. Do not delete or retry until the owner selects the exact cleanup target and confirms; no phone route or call changed.
- The second-account isolation credentials were configured locally and used to deploy `customer-support-realtime-v1` to the `ap-south` LiveKit Cloud region. The container is running and the worker registered under that exact agent name. It remains isolated: no telephone dispatch rule, phone route, recording, customer-data access, tool, escalation, or outbound-call capability is attached.
- A private LiveKit Agent Console rehearsal selected `customer-support-realtime-v1`, confirmed its OpenAI Realtime greeting and a generic order-tracking reply, and then ended the session. The Console showed recording off during the active test. No telephone routing, customer-data access, tools, escalation, or outbound call was enabled.
- The realtime agent now accepts only a bounded, explicitly labelled approved FAQ excerpt from the existing authenticated dispatch metadata. Missing, malformed, mismatched, or oversized context is ignored and retains the safe human-support fallback. The isolated LiveKit deployment is running the updated version `ENnCuTZt6pHK`; the local app now prefers that isolated profile when present. The final caller-audible FAQ rehearsal remains gated by fresh microphone approval.

# Deployment Decision

There are no active local-release gaps. Cloud deployment is an end-of-project
release activity and remains deferred until the project is otherwise complete
and release authority is explicitly granted.

# Next Action

The Customer Support Worker V1 web-chat configuration is implemented with an
explicit versioned identity and a safe-unavailable response that offers human
support. The complete Python suite and frontend lint/build/rendered-page checks
pass. Signed-in Docker web-chat acceptance passed for an approved order-tracking
answer and an unsupported refund request that safely offered human support.
The local Admin-to-Jira result handling now distinguishes a created Jira ticket
from a Jira rejection or an outcome that cannot be confirmed, and prevents the
UI from claiming that a ticket was created without a Jira reference. The
corrected Admin-to-Jira rehearsal passed: Jira ticket `CS-16` was created and
saved for a new unsupported refund-policy conversation. The Twilio-to-LiveKit pilot remains
trial-only with its
narrow allowlist and separate dispatch. The native local-worker route and its
isolated proof remain separate-project only; do not co-dispatch it with the
managed agent in the same room under the strict no-transcript-data boundary.
Any expansion to speech, data access, tools,
recording, outbound calling, or production traffic requires separate owner
approval. Cloud deployment remains an end-of-project activity.

The owner approved design of a separate outbound-calling pilot. It is limited
to one consented, owner-designated test recipient and static greeting; no call,
credential, number, deployment, recording, AI conversation, customer-data
access, retry, or follow-up is authorized until the stated pre-call gates and
action-time approval are complete.

The disabled-by-default outbound-pilot guard is implemented and tested. It
permits only the designated verified recipient and caller identity, exact
disclosed greeting, consent, trial verification, 08:00–21:00 recipient-local
time, and final action-time approval. It has no retry, recording, voicemail,
AMD, AI, or UI/API invocation. A dedicated Twilio credential configuration and
fresh final approval remain required before any provider request.

The owner has stored the dedicated Twilio Account SID, API Key SID, and API
Key Secret locally. The pilot client now uses API-key Basic authentication
rather than the broader Account Auth Token. Credentials were not displayed,
tested against Twilio, or committed. Final action-time approval remains the
only gate before the single provider request.

One owner-confirmed pilot request was submitted during the approved recipient
local-time window. Twilio rejected authentication with HTTP 401 before any
call reference was returned, so no call was created or delivered. The Account
SID and API Key SID have valid identifiers; the remaining credential correction
is local and requires no call retry until the owner confirms again.

After the credential correction and fresh final approval, Twilio accepted one
outbound pilot request with provider call reference
`CA76b29e7fcca3da88ba7d7091a724f075` and initial status `queued`. No
recording, voicemail, AI conversation, retry, or follow-up was requested.

The owner then created a TwiML Bin for the same static greeting. Its handler
URL is stored only in ignored local configuration, and the pilot client accepts
only the Twilio TwiML Bin handler URL form. After renewed action-time approval,
a second pilot request was accepted with provider call reference
`CA5c9b8ea3dda66a956957bd9db9af7505`; it reached terminal status `completed`
after 17 seconds with no provider error. Twilio's trial notice precedes the
configured greeting until the account is upgraded. No recording, voicemail,
AI conversation, retry, or follow-up was requested.

The owner approved a minimal OpenAI Realtime support-agent setup. The separately
named `customer-support-realtime-v1` source uses the local OpenAI API key and
the configured LiveKit connection only when it is explicitly started. Its
instructions prohibit tools, customer-data access, recording, transcript
persistence, escalation, outbound calling, and unsupported claims. It is not
deployed and no LiveKit dispatch rule or phone route has changed. The next
separately gated step is a LiveKit Cloud deployment followed by one consented,
generic-support test.

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

Twilio trial checkpoint: account access and verified-handset inbound testing
are complete. The trial voice test played the notice and selected response.
TwiML may support simple trial IVR functions, but trial policy blocks
`<Dial><Sip>`, so it cannot connect the call to LiveKit. The legacy Console
confirmed the available trial trunk path: one Elastic SIP Trunk exists with
the LiveKit project endpoint as its Origination URI. LiveKit now has a
separate, trunk-scoped inbound route to the existing support agent. The Twilio
number is attached. The controlled retry passed: caller-audible greeting and
responsive agent conversation were confirmed after adding the Twilio media
range to the narrow LiveKit allowlist.

Native-number local-worker checkpoint: the safe admission fix is implemented
and focused tests pass. It substitutes an exact, deployment-configured
dispatch-route token only when the LiveKit-managed SIP event omits the called
number or supplies an invalid value; unknown/missing tokens still reject the
call. The hardened worker then admitted a controlled call without media
processing. It was stopped because co-dispatch causes LiveKit to broadcast the
managed agent's transcript data stream to every room participant; an isolation
decision is required before it can run again. The attempted second LiveKit
number was blocked by the project quota before rental; the managed native rule
was restored and the local worker is stopped. A separate LiveKit project then
provided the isolated proof: the admission-only worker accepted one trusted
call without co-participant transcript traffic and was stopped afterward.

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
| 5.48 | 2026-09-02 | Completed local runtime reliability hardening: documented required Supabase SSL, added and passed the health/runtime preflight, corrected the interactive staging runner to use `customer-support-worker`, and verified its Auth0-protected approved FAQ response. Added the local restart and verification runbook. No capability scope changed. |
| 5.47 | 2026-09-01 | Recorded the successful authenticated local web-chat rehearsal and the owner-confirmed isolated Cloud voice-agent order-tracking rehearsal. The browser released the microphone after the session ended. No capability scope changed. |
| 5.46 | 2026-08-27 | Added a fail-closed read-only FAQ-context gate to `customer-support-realtime-v1`, configured the local application to prefer the isolated LiveKit profile, and deployed version `ENnCuTZt6pHK` successfully. All 71 local tests pass (3 environment-dependent skips). No telephone routing, recording, tools, escalation, or outbound capability changed. |
| 5.45 | 2026-08-26 | Completed and ended a private Agent Console rehearsal for `customer-support-realtime-v1`. The agent greeted and answered a generic order-tracking prompt through the OpenAI Realtime model; recording was off and no telephone route, customer data, tool, escalation, or outbound capability changed. |
| 5.44 | 2026-08-25 | Deployed `customer-support-realtime-v1` to the second LiveKit account in `ap-south`. Startup logs confirm the OpenAI plugin loaded and the worker registered under the intended name. The deployment remains isolated with no phone routing, recording, data, tool, escalation, or outbound capability attached. |
| 5.43 | 2026-08-25 | Corrected the LiveKit deployment diagnosis: local `LIVEKIT_CLOUD_*` credentials target a different project than the browser project. CLI listed the existing managed support agent and two incomplete unnamed `Setting Up` records from failed create attempts. Cleanup is separately owner-confirmed; no phone route or call changed. |
| 5.42 | 2026-08-25 | Prepared a dedicated deployable container for `customer-support-realtime-v1` and verified 71 tests (3 environment-dependent skips). LiveKit Cloud rejected deployment before creation because the account reached its `1/1` agent limit; the target project contains no agent to replace. No secret, phone route, or call changed. |
| 5.41 | 2026-08-24 | Added the separately named `customer-support-realtime-v1` OpenAI Realtime agent source. Local configuration loading succeeds and the Python suite passes (71 tests, 3 environment-dependent skips). The agent is not deployed and no dispatch, phone, recording, data, tool, escalation, or outbound capability changed. |
| 5.40 | 2026-08-24 | Completed the TwiML-Bin outbound-pilot proof. With renewed approval, Twilio accepted `CA5c9b8ea3dda66a956957bd9db9af7505`, which completed after 17 seconds without provider error. The required Twilio trial notice precedes the configured static greeting; no recording, AI conversation, retry, or follow-up was used. |
| 5.39 | 2026-08-24 | After credential correction and fresh final approval, Twilio accepted the single outbound pilot request (`CA76b29e7fcca3da88ba7d7091a724f075`, initial status `queued`). No recording, voicemail, AI, retry, or follow-up was requested; awaiting owner confirmation of the greeting or terminal result. |
| 5.38 | 2026-08-24 | The owner-confirmed outbound pilot request reached Twilio during the approved window but authentication was rejected (`401`) before a call reference was issued. No call was created or delivered. Local identifier formats were verified without exposing credentials; correct or replace the API Key Secret/account pairing, then obtain fresh action-time approval before a new request. |
| 5.37 | 2026-08-24 | Verified locally that the dedicated Twilio Account SID, API Key SID, and API Key Secret are configured. Updated the pilot client to use API-key Basic authentication; 71 tests pass (3 environment-dependent skips). No provider request or call was made. |
| 5.36 | 2026-08-24 | Implemented and tested the disabled-by-default outbound pilot guard. It rejects missing final approval, unverified or different numbers, a changed greeting, and calls outside recipient-local quiet hours; 70 tests pass (3 environment-dependent skips). No provider request or call was made. |
| 5.35 | 2026-08-24 | Recorded the approved design for a narrow outbound-calling pilot: one explicitly consented owner-designated recipient, one static disclosed greeting, terminal-status evidence only, and no recording, AI conversation, customer data, retry, or follow-up. No call was placed. |
| 5.34 | 2026-08-24 | Customer Support Worker V1 Admin-to-Jira acceptance passed: a new unsupported refund-policy conversation safely offered human support, and authorized escalation created and saved Jira ticket `CS-16`. |
| 5.33 | 2026-08-24 | Added a safe Jira diagnostic code to future failed or unconfirmed escalation results (for example, `jira_rejected_403`), without storing Jira response bodies, credentials, or customer content. The existing failed request was not retried. Python suite (68 tests, 3 environment-dependent skips) and frontend lint/build/rendered-page checks pass; localhost services were refreshed. |
| 5.32 | 2026-08-24 | Corrected local Admin-to-Jira escalation feedback: only a confirmed Jira issue key is reported as created; Jira rejection and unconfirmed outcomes are explicit and are not presented as success. Python suite (68 tests, 3 environment-dependent skips) and frontend lint/build/rendered-page checks pass; localhost services were refreshed. |
| 5.31 | 2026-08-24 | Verified the Customer Support Worker V1 web-chat path in local Docker: an approved order-tracking FAQ answered correctly, while an unsupported refund request safely offered human support. Tightened lexical FAQ matching to reject unrelated partial matches and added a reconnect safeguard for closed managed-PostgreSQL connections. The authorized Admin-to-Jira rehearsal remains. |
| 5.30 | 2026-08-24 | Implemented the Customer Support Worker V1 web-chat configuration as `customer-support-worker:faq-v1`. An unmatched question now returns the approved human-support response with a ticket recommendation instead of an empty support response. No data source, voice route, Jira authorization, or outbound capability changed. |
| 5.29 | 2026-08-24 | Recorded the approved Customer Support Worker V1 design: authenticated web chat and inbound phone may use approved tenant FAQ only, with an authorized idempotent Jira escalation for unresolved support. Account lookup, payments, recording, outbound contact, and autonomous actions remain excluded. |
| 5.28 | 2026-08-24 | Completed the isolated native-worker proof in a separate LiveKit project: one local-worker-only inbound call reached the trusted route and admitted without error or co-dispatched transcript traffic. The worker was stopped immediately afterward; the original native route remains managed-agent-only. |
| 5.27 | 2026-08-24 | Attempted the approved $1/month isolated LiveKit number, but the project quota blocked purchase before any charge. Restored the native dispatch to the managed support agent only and confirmed the local worker is stopped. |
| 5.26 | 2026-08-24 | Functionally verified native-number local-worker admission with the exact dispatch token and fail-closed invalid/missing-number fallback. Stopped the worker after confirming that LiveKit broadcasts managed-agent transcript data to co-dispatched room participants; strict isolation is now required before any restart. |
| 5.25 | 2026-08-24 | Confirmed the native dispatch token reaches the local worker and extended the fail-closed fallback to invalid as well as missing managed SIP called-number values. Stopped the first worker after detecting transient turn/transcript plumbing, then hardened it to admission-only operation; compilation and 11 focused tests pass. |
| 5.24 | 2026-08-24 | Implemented and tested a fail-closed native-number local-worker route binding using exact, deployment-configured LiveKit dispatch metadata when the managed SIP event lacks a called-number attribute. The active native route remains unchanged pending a separately approved live rehearsal. |
| 5.23 | 2026-08-24 | Completed the controlled Twilio-to-LiveKit inbound validation: the owner heard the greeting and confirmed responsive agent conversation. The route remains trial-only with a narrow allowlist, separate dispatch, and no recording, data access, tools, or outbound calling. |
| 5.22 | 2026-08-24 | Diagnosed the first Twilio-to-LiveKit call: SIP delivery, room creation, agent dispatch, and agent greeting all succeeded. Added Twilio's documented media CIDR to the existing narrow LiveKit allowlist before one controlled caller-audible retry. |
| 5.21 | 2026-08-24 | Verified that the Twilio trial number is attached to the Elastic SIP Trunk, activating the prepared inbound route. No call has been made through it. The next approved action is one verified-handset inbound call to confirm agent answer. |
| 5.20 | 2026-08-24 | Created a separate, Twilio-limited LiveKit inbound trunk and a dedicated dispatch rule scoped to that trunk. It uses the existing support agent with a separate room prefix; the working LiveKit-native route was preserved. The next gated step is one trial inbound call after number attachment. |
| 5.19 | 2026-08-24 | Resolved the apparent Elastic SIP Trunk trial block as a Console-routing issue. Created the allowed trial trunk and configured the LiveKit Cloud SIP endpoint as its Origination URI; no number is attached and no traffic has been sent. Next is a separate, scoped LiveKit inbound trunk and dispatch rule. |
| 5.18 | 2026-08-24 | Completed the Twilio free-trial inbound Voice rehearsal using the verified handset; no credentials, code, recordings, or routing were added. Recorded the Elastic SIP Trunk Console upgrade-gate conflict with published trial guidance; support clarification is the restart point. |
| 5.17 | 2026-08-24 | Deferred the LiveKit-number local-worker diagnostic at the owner's direction and started a separate, no-traffic Twilio evaluation. First action: account access and a dedicated restricted API key; number rental, routing, recording, and outbound traffic remain gated. |
| 5.16 | 2026-08-23 | Reconfirmed the normal managed inbound-phone route by owner-heard agent audio. Added a privacy-safe local-worker routing-context diagnostic (metadata presence/length and SIP attribute names only); 12 focused tests pass. The next action is one controlled local-worker call followed by immediate pilot-route restoration. |
| 5.15 | 2026-08-23 | Corrected the telephone diagnosis: SIP dispatch reaches the local worker, but its managed-phone participant lacks the configured called-number attribute. Added and empty-room-tested the owner-approved model-free audio subscription required to answer calls. |
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

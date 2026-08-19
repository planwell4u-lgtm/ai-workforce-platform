# LiveKit Local Sandbox Evaluation Record

**Status:** Active local evaluation  
**Date:** 2026-08-18

## Decision

Evaluate LiveKit as the first realtime-media provider in an isolated local
Docker sandbox. The existing provider-neutral Voice contracts and canonical
Conversation ownership remain unchanged.

## Local Evidence

- Container: `ai-workforce-livekit-sandbox`
- Image digest: `livekit/livekit-server@sha256:3497163e15c48fef6e7830c78716f9e9d5edc28abf7aa90b61c86e93bbc306b1`
- Mode: LiveKit development mode, using its documented development-only
  credentials.
- Local signaling endpoint: `ws://localhost:7880`
- Local media TCP endpoint: `localhost:7881`
- Local media UDP endpoint: `localhost:7882/udp`
- Docker Desktop run uses `--node-ip 127.0.0.1` so the local server advertises
  a browser-reachable media address instead of its internal container address.
- All three endpoints were reachable on 2026-08-18.

## Scope and Boundaries

- This sandbox evaluates local realtime-media connection and provider-adapter
  behavior only.
- It does not use a LiveKit Cloud account, publish a cloud deployment, contact
  participants, record media, or introduce production credentials.
- LiveKit rooms, participants, tracks, and provider identifiers do not replace
  canonical Conversation, tenant, identity, authorization, or turn ownership.
- Twilio PSTN/SIP, phone numbers, messaging, and any external telephony effect
  remain out of scope until separately approved.

## Completed Evaluation Step

The test-only provider adapter connects to this local sandbox through the
existing Voice boundary and proves connection/disconnection evidence does not
create a competing or falsely successful Conversation turn. The backend image
also builds with the LiveKit dependency and Voice package included.

The signed-in browser evaluation path is now implemented for the local
sandbox. The backend issues an authorization-checked, room-bound LiveKit token
that expires after five minutes; the browser receives only that token and the
local signaling URL, never the LiveKit API secret. The browser test publishes a
brief oscillator-generated audio track and explicitly does not request or use a
microphone.

The signed-in browser rehearsal passed on 2026-08-18. LiveKit recorded the
room join, the published audio track, 76 received RTP packets over roughly
1.5 seconds, and a clean client-requested disconnect. The browser displayed:
`Local voice test passed. A synthetic tone was sent; no microphone was used.`

The approved microphone and recovery rehearsal also passed on 2026-08-18.
After explicit in-page consent and browser permission, LiveKit recorded a
microphone track using echo cancellation, noise suppression, and auto-gain;
it received 565 RTP packets over about 11.5 seconds with no packet loss. The
user selected Stop and LiveKit recorded a clean client-requested disconnect.

The two-participant playback rehearsal passed on 2026-08-18. The host browser
joined with its microphone after explicit consent. A second browser session for
the same signed-in user supplied the displayed tenant-scoped room code and
joined as a listener, without sharing a microphone. The token service assigned
each session a distinct temporary participant identity, preventing the listener
from displacing the host. LiveKit confirmed that the listener subscribed to the
host audio track and started forwarding RTP. The owner confirmed audible
playback in the listener browser.

The permission-denied recovery rehearsal also passed on 2026-08-18. With
browser-level microphone permission set to Block, the application reported
that microphone permission was not granted and that nothing was shared; the
voice control returned to Start. After browser permission was restored, a new
microphone session connected successfully.

The scripted browser-agent rehearsal passed on 2026-08-19. An explicit
agent-test request creates a `local-agent-...` room. A separate local worker
discovers only those rooms, joins as its own LiveKit participant, publishes one
offline synthesized greeting, and disconnects. The owner heard the greeting in
the browser. The worker has no support-data access, recording, cloud
credentials, or AI-model integration; the robotic offline voice is intentional
for this transport and lifecycle proof.

A separate LiveKit Cloud Agent Builder browser rehearsal passed on 2026-08-19.
The owner created and tested a simple open-ended agent using LiveKit-managed
voice models and generic safe prompts. No actions, HTTP tools, MCP servers,
data collection, secrets, application-data connection, telephony, or recording
were enabled. The owner confirmed that the browser conversation worked
normally.

The protected local-browser-to-Cloud-agent rehearsal passed on 2026-08-19.
The authenticated backend creates a unique tenant-scoped Cloud room, issues a
five-minute room-bound participant token, and explicitly dispatches the
deployed agent. The browser receives only the room URL and participant token,
never a Cloud API secret. The owner confirmed that the deployed agent joined,
spoke naturally, and safely answered an order-tracking question. This proof
uses no application data, actions, HTTP tools, MCP servers, recording,
telephony, or phone number.

## Next Evaluation Step

The bounded local media, scripted-agent, Cloud Console conversational, and
protected local-browser-to-Cloud-agent rehearsals are complete. Before
telephony, choose and authorize either Cloud browser recovery/lifecycle checks,
or a separately designed read-only application-data boundary. Do not connect
the agent to support data, enable actions, recording, Twilio, number rental,
dispatch-rule activation, or any telephone call without a separate approved
decision.

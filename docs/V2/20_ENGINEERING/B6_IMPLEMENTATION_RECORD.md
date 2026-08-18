# B6 Implementation Record — First Voice Adapter

Local Voice simulation binds each interaction to the canonical Conversation.
Interrupted or disconnected output marks its active turn `uncertain`, never
delivered or successful.

The first provider evaluation is now implemented through a test-only LiveKit
adapter. It mints a local sandbox token, joins a room named from the canonical
conversation reference, and on disconnect marks any active canonical turn
`uncertain` before closing the provider connection. The focused local sandbox
test and backend container build both pass.

For the separate browser-media evaluation, the backend issues only a five-minute
room token after the existing tenant and `agent.context.read` checks pass. The
browser gets no provider secret and publishes a synthetic oscillator track,
not microphone audio. This browser path remains a local evaluation aid and is
not a Conversation turn or production voice feature.

The approved first user-facing voice design now requires explicit in-page
consent before the browser requests microphone access. It publishes microphone
audio with echo cancellation, noise suppression, and auto-gain; subscribes to
and plays remote audio tracks; and provides Stop, Cancel, permission-denied,
connection-failure, and sign-out cleanup paths. Stop unpublishes the track,
stops the browser microphone, removes playback elements, and disconnects.
No recording is enabled.

The local two-participant playback rehearsal passed. The host joined with a
consented microphone and exposed a tenant-scoped room code. A second same-user
browser session joined that room as a listener without requesting microphone
access. The backend validates the requested room belongs to the authenticated
tenant and gives each token a unique temporary LiveKit participant identity.
LiveKit recorded the listener subscription and RTP forwarding, and the owner
confirmed audible playback.

The denied-permission recovery path was also verified in the browser. When the
site microphone permission was blocked, the application displayed the explicit
no-sharing recovery state and returned to Start voice. Restoring permission
allowed a fresh microphone session to connect.

No participant media track, recording, LiveKit Cloud project, Twilio account,
PSTN/SIP route, phone number, or live telephony effect is enabled.

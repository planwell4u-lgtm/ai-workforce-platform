# B6 Implementation Record — First Voice Adapter

Local Voice simulation binds each interaction to the canonical Conversation.
Interrupted or disconnected output marks its active turn `uncertain`, never
delivered or successful.

The first provider evaluation is now implemented through a test-only LiveKit
adapter. It mints a local sandbox token, joins a room named from the canonical
conversation reference, and on disconnect marks any active canonical turn
`uncertain` before closing the provider connection. The focused local sandbox
test and backend container build both pass.

No participant media track, recording, LiveKit Cloud project, Twilio account,
PSTN/SIP route, phone number, or live telephony effect is enabled.

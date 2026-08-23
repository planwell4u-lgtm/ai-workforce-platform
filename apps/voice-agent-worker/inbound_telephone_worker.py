"""Local LiveKit Agents entrypoint for the B11 inbound-admission boundary.

This worker admits validated SIP participants into canonical Conversation and
Voice state. It intentionally starts no model, STT/TTS, recording, transcript,
support-data, action, or outbound-call capability. Its default agent name does
not match the active pilot dispatch rule.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path

from livekit import rtc
from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages" / "conversation" / "python" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "voice" / "python" / "src"))

from ai_workforce_voice.livekit_telephony import (  # noqa: E402
    LiveKitInboundCallEvent,
    LiveKitInboundTelephoneAdapter,
    call_ref_from_sip_attributes,
)
from ai_workforce_voice.telephone_worker import InboundTelephoneWorker  # noqa: E402
from ai_workforce_voice.telephony import InboundTelephoneAdapter  # noqa: E402
from ai_workforce_conversation.control import ConversationService  # noqa: E402


def tenant_routes_from_environment(environment: Mapping[str, str]) -> dict[str, str]:
    raw = environment.get("INBOUND_TELEPHONE_TENANT_MAP_JSON")
    if not raw:
        raise RuntimeError("INBOUND_TELEPHONE_TENANT_MAP_JSON is required")
    parsed = json.loads(raw)
    if not isinstance(parsed, dict) or not all(
        isinstance(number, str) and isinstance(tenant, str) and tenant
        for number, tenant in parsed.items()
    ):
        raise RuntimeError("INBOUND_TELEPHONE_TENANT_MAP_JSON must be a non-empty string mapping")
    return dict(parsed)


def create_worker(environment: Mapping[str, str]) -> InboundTelephoneWorker:
    telephone = InboundTelephoneAdapter(
        ConversationService(), tenant_routes_from_environment(environment)
    )
    return InboundTelephoneWorker(LiveKitInboundTelephoneAdapter(telephone))


worker = create_worker(os.environ)
server = AgentServer()


@server.rtc_session(agent_name=os.environ.get("LIVEKIT_INBOUND_AGENT_NAME", "planwell-inbound-local"))
async def inbound_telephone_session(ctx: JobContext) -> None:
    # This session is intentionally model-free: it subscribes to the caller's
    # audio so LiveKit can answer the SIP call, but performs no speech,
    # transcription, generation, recording, storage, or outbound media.
    session = AgentSession()
    await session.start(
        agent=Agent(instructions="Maintain the LiveKit telephone connection without responding."),
        room=ctx.room,
        record=False,
    )
    await ctx.connect()
    participant = await ctx.wait_for_participant(kind=rtc.ParticipantKind.PARTICIPANT_KIND_SIP)
    event = LiveKitInboundCallEvent(
        call_ref_from_sip_attributes(participant.attributes),
        ctx.room.name,
        "sip",
        participant.attributes,
    )
    interaction = worker.participant_connected(event)
    disconnected = asyncio.Event()

    @ctx.room.on("participant_disconnected")
    def on_participant_disconnected(leaving: rtc.RemoteParticipant) -> None:
        if leaving.identity == participant.identity:
            disconnected.set()

    try:
        await disconnected.wait()
    finally:
        if worker.active_call_count() and interaction.call_ref:
            worker.participant_disconnected(interaction.call_ref)


if __name__ == "__main__":
    cli.run_app(server)

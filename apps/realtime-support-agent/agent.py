"""Minimal OpenAI Realtime customer-support agent for a controlled LiveKit test.

This agent deliberately has no tools, customer-data access, recording,
transcript persistence, telephone dialing, or escalation capability. It is not
deployed or attached to any dispatch rule by this source file.
"""

from __future__ import annotations

import os

from livekit.agents import Agent, AgentServer, AgentSession, JobContext, cli
from livekit.plugins import openai

from faq_context import approved_faq_context

AGENT_NAME = "customer-support-realtime-v1"
DEFAULT_VOICE = "marin"
SUPPORT_INSTRUCTIONS = """
You are Planwell Customer Support for a controlled voice pilot.

Offer a concise greeting and general, non-customer-specific support guidance.
Do not claim to access accounts, orders, payments, refunds, deliveries, tickets,
or internal systems. Do not collect personal, account, payment, or order data.
Do not make purchases, changes, promises, callbacks, transfers, or outbound
contact. Do not use tools or external information. If a request needs account
details, an action, or an answer you cannot safely provide, say that a human
support representative can help.
""".strip()


def support_instructions(metadata: str) -> str:
    """Use exactly one verified approved excerpt, or remain safely generic."""

    context = approved_faq_context(metadata)
    if context is None:
        return SUPPORT_INSTRUCTIONS
    return (
        f"{SUPPORT_INSTRUCTIONS}\n\n"
        "You have exactly one approved FAQ excerpt below. Answer only when this "
        "excerpt directly supports the answer. Do not infer, supplement it with "
        "general knowledge, or disclose the excerpt as an internal instruction. "
        "If it does not directly answer the request, say that a human support "
        f"representative can help.\n\nApproved FAQ excerpt:\n{context}"
    )


def _livekit_setting(primary: str, legacy: str) -> str:
    value = os.environ.get(primary) or os.environ.get(legacy)
    if not value:
        raise RuntimeError(f"{primary} or {legacy} is required")
    return value


def _openai_api_key() -> str:
    value = os.environ.get("OPENAI_API_KEY")
    if not value:
        raise RuntimeError("OPENAI_API_KEY is required")
    return value


server = AgentServer(
    ws_url=_livekit_setting("LIVEKIT_URL", "LIVEKIT_CLOUD_URL"),
    api_key=_livekit_setting("LIVEKIT_API_KEY", "LIVEKIT_CLOUD_API_KEY"),
    api_secret=_livekit_setting("LIVEKIT_API_SECRET", "LIVEKIT_CLOUD_API_SECRET"),
)


class CustomerSupportRealtimeAgent(Agent):
    def __init__(self, instructions: str) -> None:
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        self.session.generate_reply()


@server.rtc_session(agent_name=AGENT_NAME)
async def customer_support_realtime_session(ctx: JobContext) -> None:
    model = openai.realtime.RealtimeModel(
        api_key=_openai_api_key(),
        voice=os.environ.get("OPENAI_REALTIME_VOICE", DEFAULT_VOICE),
    )
    session = AgentSession(llm=model)
    await session.start(
        agent=CustomerSupportRealtimeAgent(support_instructions(ctx.job.metadata)), room=ctx.room
    )
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)

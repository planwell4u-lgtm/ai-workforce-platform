"""Bounded local scripted-voice-agent rehearsal for the LiveKit sandbox.

This is deliberately not a production agent or an AI model integration. It
joins only local agent-test rooms, publishes one offline synthesized greeting,
then disconnects. It never receives support data, records audio, or makes
external requests.
"""

from __future__ import annotations

import asyncio
import io
import os
import wave

from livekit import api, rtc

AGENT_ROOM_PREFIX = "local-agent-"
AGENT_IDENTITY = "planwell-local-scripted-agent"
GREETING = "Hello. This is the local Planwell scripted voice agent test. Audio playback is working."


def required_setting(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def api_url(signaling_url: str) -> str:
    if signaling_url.startswith("ws://"):
        return "http://" + signaling_url.removeprefix("ws://")
    if signaling_url.startswith("wss://"):
        return "https://" + signaling_url.removeprefix("wss://")
    raise RuntimeError("LIVEKIT_SANDBOX_URL must use ws:// or wss://")


async def publish_greeting(room: rtc.Room) -> None:
    process = await asyncio.create_subprocess_exec(
        "espeak-ng",
        "--stdout",
        "-v",
        "en-us",
        GREETING,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    wav_bytes, error_output = await process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"offline speech synthesis failed: {error_output.decode().strip()}")
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        if wav_file.getsampwidth() != 2:
            raise RuntimeError("offline speech must be 16-bit PCM")
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        audio = wav_file.readframes(wav_file.getnframes())
    source = rtc.AudioSource(sample_rate, channels)
    track = rtc.LocalAudioTrack.create_audio_track("scripted-agent-greeting", source)
    await room.local_participant.publish_track(track)
    frame_samples = 960
    frame_size = frame_samples * channels * 2
    for offset in range(0, len(audio), frame_size):
        chunk = audio[offset : offset + frame_size]
        samples = len(chunk) // (channels * 2)
        if samples:
            await source.capture_frame(rtc.AudioFrame(chunk, sample_rate, channels, samples))
    await asyncio.sleep(1)


async def run_room(signaling_url: str, api_key: str, api_secret: str, room_name: str) -> None:
    room = rtc.Room()
    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity(f"{AGENT_IDENTITY}-{room_name.rsplit('-', 1)[-1]}")
        .with_name("Planwell local scripted agent")
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
        .to_jwt()
    )
    try:
        await room.connect(signaling_url, token)
        await publish_greeting(room)
    finally:
        await room.disconnect()


async def main() -> None:
    signaling_url = required_setting("LIVEKIT_SANDBOX_URL")
    api_key = required_setting("LIVEKIT_API_KEY")
    api_secret = required_setting("LIVEKIT_API_SECRET")
    active_rooms: set[str] = set()
    client = api.LiveKitAPI(api_url(signaling_url), api_key, api_secret)
    try:
        while True:
            rooms = await client.room.list_rooms(api.ListRoomsRequest())
            for room in rooms.rooms:
                if room.name.startswith(AGENT_ROOM_PREFIX) and room.name not in active_rooms:
                    active_rooms.add(room.name)
                    asyncio.create_task(run_room(signaling_url, api_key, api_secret, room.name))
            await asyncio.sleep(1)
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())

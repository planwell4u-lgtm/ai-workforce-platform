"""Twilio Voice PSTN & TwiML Adapter for Planwell Platform."""

from __future__ import annotations

import math
from typing import Any
from xml.etree import ElementTree as ET


class TwilioVoiceAdapter:
    """Handles incoming Twilio PSTN voice calls and builds TwiML routing XML."""

    @staticmethod
    def parse_incoming_call(form_data: dict[str, list[str]]) -> dict[str, str]:
        """Parses Twilio Voice webhook form parameters."""
        caller = form_data.get("From", [""])[0]
        to = form_data.get("To", [""])[0]
        call_sid = form_data.get("CallSid", [""])[0]
        call_status = form_data.get("CallStatus", ["ringing"])[0]
        duration = form_data.get("CallDuration", ["0"])[0]

        try:
            duration_secs = int(duration)
        except ValueError:
            duration_secs = 0

        return {
            "from": caller,
            "to": to,
            "call_sid": call_sid,
            "status": call_status,
            "duration_seconds": str(duration_secs),
        }

    @staticmethod
    def build_twiml_response(
        greeting_text: str = "Thank you for calling Planwell AI Support. Connecting you to an AI agent.",
        stream_url: str = "wss://voice.planwell.online",
    ) -> str:
        """Constructs valid TwiML XML connecting incoming call to LiveKit real-time agent."""
        response = ET.Element("Response")
        say = ET.SubElement(response, "Say", voice="Polly.Joanna")
        say.text = greeting_text

        connect = ET.SubElement(response, "Connect")
        stream = ET.SubElement(connect, "Stream", url=stream_url)
        stream.set("name", "PlanwellLiveKitVoiceStream")

        return f'<?xml version="1.0" encoding="UTF-8"?>\n{ET.tostring(response, encoding="utf-8").decode("utf-8")}'

    @staticmethod
    def build_twiml_gather_response(
        say_text: str,
        action_url: str = "https://planwell.online/api/v1/channels/voice/respond",
    ) -> str:
        """Constructs interactive TwiML Gather XML for speech recognition and AI agent response."""
        response = ET.Element("Response")
        gather = ET.SubElement(
            response,
            "Gather",
            input="speech",
            action=action_url,
            method="POST",
            speechTimeout="auto",
        )
        say = ET.SubElement(gather, "Say", voice="Polly.Joanna")
        say.text = say_text

        goodbye = ET.SubElement(response, "Say", voice="Polly.Joanna")
        goodbye.text = "Thank you for calling Planwell AI Voice Support. Have a great day! Goodbye."

        return f'<?xml version="1.0" encoding="UTF-8"?>\n{ET.tostring(response, encoding="utf-8").decode("utf-8")}'

    @staticmethod
    def calculate_billable_minutes(duration_seconds: int) -> int:
        """Calculates billable call minutes rounded up to nearest whole minute."""
        if duration_seconds <= 0:
            return 0
        return math.ceil(duration_seconds / 60.0)

    @staticmethod
    def build_outbound_call_payload(
        to_number: str,
        from_number: str,
        twiml_url: str = "https://planwell.online/api/v1/channels/voice/incoming",
    ) -> dict[str, str]:
        """Builds Twilio REST API payload for initiating an outbound PSTN call."""
        return {
            "To": to_number,
            "From": from_number,
            "Url": twiml_url,
            "Method": "POST",
            "StatusCallback": twiml_url,
        }

    @staticmethod
    def dispatch_outbound_call(
        account_sid: str,
        auth_secret: str,
        to_number: str,
        from_number: str,
        twiml_url: str = "https://planwell.online/api/v1/channels/voice/incoming",
        api_key: str | None = None,
    ) -> dict[str, Any]:
        """Dispatches a live PSTN voice call via Twilio REST API."""
        import base64
        import json
        import urllib.parse
        import urllib.request

        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls.json"
        data = urllib.parse.urlencode({
            "To": to_number,
            "From": from_number,
            "Url": twiml_url,
            "Method": "POST",
        }).encode("utf-8")

        username = api_key or account_sid
        auth_bytes = f"{username}:{auth_secret}".encode("utf-8")
        auth_header = f"Basic {base64.b64encode(auth_bytes).decode('utf-8')}"

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                return json.loads(res_body)
        except Exception as exc:
            return {"error": str(exc), "status": "failed"}



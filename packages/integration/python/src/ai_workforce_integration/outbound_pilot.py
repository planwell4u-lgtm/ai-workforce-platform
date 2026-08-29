"""Narrow, disabled-by-default Twilio outbound pilot boundary."""

from __future__ import annotations

from base64 import b64encode
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Protocol
from urllib.parse import urlencode
from urllib.request import Request

PILOT_GREETING = "Hello. This is a Planwell outbound pilot test. No action is required. Goodbye."


class OutboundPilotDenied(PermissionError):
    """The single-call pilot has not met every pre-call gate."""


@dataclass(frozen=True)
class OutboundPilotRequest:
    recipient: str
    caller: str
    greeting: str
    consent_confirmed: bool
    recipient_verified_for_trial: bool
    final_approval: bool = False


@dataclass(frozen=True)
class OutboundPilotResult:
    provider_call_ref: str
    status: str


class HttpSender(Protocol):
    def __call__(self, request: Request, timeout: float) -> object: ...


class OutboundPilotPolicy:
    """Permit exactly one disclosed pilot call only at action time."""

    def __init__(self, recipient: str, caller: str) -> None:
        self._recipient, self._caller = recipient, caller

    def authorize(self, request: OutboundPilotRequest, recipient_local_time: datetime) -> None:
        if not request.final_approval:
            raise OutboundPilotDenied("final_approval_required")
        if not request.consent_confirmed or not request.recipient_verified_for_trial:
            raise OutboundPilotDenied("consent_and_trial_verification_required")
        if request.recipient != self._recipient or request.caller != self._caller:
            raise OutboundPilotDenied("unapproved_number")
        if request.greeting != PILOT_GREETING:
            raise OutboundPilotDenied("unapproved_greeting")
        if not _is_e164(request.recipient) or not _is_e164(request.caller):
            raise OutboundPilotDenied("invalid_number")
        if not 8 <= recipient_local_time.hour < 21:
            raise OutboundPilotDenied("outside_recipient_quiet_hours")


class TwilioOutboundPilotClient:
    """Submit one authorized TwiML-Bin call without recording or retries."""

    def __init__(
        self,
        account_sid: str,
        api_key_sid: str,
        api_key_secret: str,
        twiml_url: str,
        sender: HttpSender,
    ) -> None:
        self._account_sid = account_sid
        self._api_key_sid = api_key_sid
        self._api_key_secret = api_key_secret
        self._twiml_url = twiml_url
        self._sender = sender

    @classmethod
    def from_environment(cls, environment: Mapping[str, str], sender: HttpSender) -> TwilioOutboundPilotClient:
        names = (
            "TWILIO_ACCOUNT_SID",
            "TWILIO_API_KEY",
            "TWILIO_API_SECRET",
            "TWILIO_OUTBOUND_PILOT_TWIML_URL",
        )
        if any(not environment.get(name) for name in names):
            raise ValueError("Twilio outbound pilot configuration is required")
        twiml_url = environment["TWILIO_OUTBOUND_PILOT_TWIML_URL"]
        if not twiml_url.startswith("https://handler.twilio.com/twiml/"):
            raise ValueError("Twilio outbound pilot requires a TwiML Bin URL")
        return cls(
            environment["TWILIO_ACCOUNT_SID"],
            environment["TWILIO_API_KEY"],
            environment["TWILIO_API_SECRET"],
            twiml_url,
            sender,
        )

    def place(self, request: OutboundPilotRequest) -> OutboundPilotResult:
        payload = urlencode(
            {
                "To": request.recipient,
                "From": request.caller,
                "Url": self._twiml_url,
            }
        ).encode()
        token = b64encode(f"{self._api_key_sid}:{self._api_key_secret}".encode()).decode()
        http_request = Request(
            f"https://api.twilio.com/2010-04-01/Accounts/{self._account_sid}/Calls.json",
            data=payload,
            headers={"Authorization": f"Basic {token}", "Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )
        with self._sender(http_request, timeout=10.0) as response:
            import json

            body = json.loads(response.read().decode())
        sid, status = body.get("sid"), body.get("status")
        if not isinstance(sid, str) or not isinstance(status, str):
            raise RuntimeError("twilio_response_missing_call_reference")
        return OutboundPilotResult(sid, status)


def _is_e164(number: str) -> bool:
    return number.startswith("+") and number[1:].isdigit() and 8 <= len(number) <= 16

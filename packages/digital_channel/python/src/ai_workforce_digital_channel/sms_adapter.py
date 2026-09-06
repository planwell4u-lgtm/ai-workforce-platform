"""Twilio SMS digital channel adapter for Planwell AI Workforce platform."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IncomingSmsMessage:
    message_sid: str
    from_number: str
    to_number: str
    body: str
    account_sid: str


class TwilioSmsAdapter:
    """Normalizes incoming Twilio SMS webhooks and constructs TwiML XML responses."""

    @staticmethod
    def parse_webhook(form_data: dict[str, str]) -> IncomingSmsMessage:
        """Parses Twilio POST form data into a structured IncomingSmsMessage."""
        from_num = form_data.get("From", "").strip()
        to_num = form_data.get("To", "").strip()
        body = form_data.get("Body", "").strip()
        msg_sid = form_data.get("MessageSid", form_data.get("SmsSid", "")).strip()
        acc_sid = form_data.get("AccountSid", "").strip()

        if not from_num or not body:
            raise ValueError("Invalid Twilio SMS webhook: 'From' and 'Body' parameters are required.")

        normalized_from = TwilioSmsAdapter.normalize_phone_number(from_num)
        normalized_to = TwilioSmsAdapter.normalize_phone_number(to_num)

        return IncomingSmsMessage(
            message_sid=msg_sid,
            from_number=normalized_from,
            to_number=normalized_to,
            body=body,
            account_sid=acc_sid,
        )

    @staticmethod
    def normalize_phone_number(phone: str) -> str:
        """Normalizes a phone number to standard format."""
        cleaned = re.sub(r"[^\d+]", "", phone.strip())
        if not cleaned:
            return phone
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        return cleaned

    @staticmethod
    def build_twiml_response(text: str) -> str:
        """Constructs a valid TwiML XML response string."""
        response_el = ET.Element("Response")
        message_el = ET.SubElement(response_el, "Message")
        message_el.text = text
        return ET.tostring(response_el, encoding="utf-8").decode("utf-8")

    @staticmethod
    def canonical_conversation_ref(tenant_ref: str, phone_number: str) -> str:
        """Generates a canonical conversation reference for SMS interactions."""
        clean_phone = TwilioSmsAdapter.normalize_phone_number(phone_number)
        return f"sms:{tenant_ref}:{clean_phone}"

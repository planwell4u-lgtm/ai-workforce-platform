"""Meta WhatsApp Cloud API digital channel adapter for Planwell AI Workforce platform."""

from __future__ import annotations

import hashlib
import hmac
import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IncomingWhatsAppMessage:
    message_id: str
    from_number: str
    phone_number_id: str
    body: str
    timestamp: str


class WhatsAppCloudAdapter:
    """Normalizes incoming Meta WhatsApp Cloud API webhooks and challenges."""

    @staticmethod
    def validate_hmac_signature(payload_bytes: bytes, signature_header: str | None, app_secret: str) -> bool:
        """Validates Meta WhatsApp X-Hub-Signature-256 HMAC header."""
        if not signature_header or not app_secret:
            return True
        if not signature_header.startswith("sha256="):
            return False
        expected_hash = hmac.new(
            app_secret.encode("utf-8"), payload_bytes, hashlib.sha256
        ).hexdigest()
        provided_hash = signature_header.removeprefix("sha256=")
        return hmac.compare_digest(expected_hash, provided_hash)

    @staticmethod
    def verify_webhook_challenge(query_params: dict[str, list[str] | str], expected_verify_token: str) -> tuple[bool, str]:
        """Validates Meta Cloud API GET webhook verification challenge.
        
        Returns (is_valid, challenge_string).
        """
        mode = query_params.get("hub.mode")
        if isinstance(mode, list):
            mode = mode[0] if mode else ""
        
        token = query_params.get("hub.verify_token")
        if isinstance(token, list):
            token = token[0] if token else ""
            
        challenge = query_params.get("hub.challenge")
        if isinstance(challenge, list):
            challenge = challenge[0] if challenge else ""

        if mode == "subscribe" and (not expected_verify_token or token == expected_verify_token):
            return True, str(challenge)
        return False, ""

    @staticmethod
    def parse_webhook(payload: dict[str, Any]) -> list[IncomingWhatsAppMessage]:
        """Parses Meta Cloud API POST JSON payload into structured IncomingWhatsAppMessage objects."""
        messages: list[IncomingWhatsAppMessage] = []
        entries = payload.get("entry", [])
        if not isinstance(entries, list):
            return messages

        for entry in entries:
            changes = entry.get("changes", []) if isinstance(entry, dict) else []
            for change in changes:
                value = change.get("value", {}) if isinstance(change, dict) else {}
                phone_num_id = str(value.get("metadata", {}).get("phone_number_id", ""))
                msg_list = value.get("messages", [])
                if not isinstance(msg_list, list):
                    continue

                for msg in msg_list:
                    if not isinstance(msg, dict):
                        continue
                    msg_id = str(msg.get("id", ""))
                    from_num = str(msg.get("from", ""))
                    msg_type = str(msg.get("type", "text"))
                    timestamp = str(msg.get("timestamp", ""))

                    body = ""
                    if msg_type == "text":
                        body = str(msg.get("text", {}).get("body", "")).strip()
                    elif msg_type == "button":
                        body = str(msg.get("button", {}).get("text", "")).strip()
                    elif msg_type == "interactive":
                        interactive = msg.get("interactive", {})
                        body = str(interactive.get("button_reply", {}).get("title", "") or interactive.get("list_reply", {}).get("title", "")).strip()

                    if from_num and body:
                        norm_from = WhatsAppCloudAdapter.normalize_whatsapp_number(from_num)
                        messages.append(
                            IncomingWhatsAppMessage(
                                message_id=msg_id,
                                from_number=norm_from,
                                phone_number_id=phone_num_id,
                                body=body,
                                timestamp=timestamp,
                            )
                        )
        return messages

    @staticmethod
    def normalize_whatsapp_number(phone: str) -> str:
        """Normalizes a WhatsApp phone number to standard format."""
        cleaned = re.sub(r"[^\d+]", "", phone.strip())
        if not cleaned:
            return phone
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        return f"whatsapp:{cleaned}"

    @staticmethod
    def build_meta_response_payload(to_number: str, text_body: str) -> dict[str, Any]:
        """Builds Meta Cloud API outbound JSON payload."""
        clean_to = to_number.replace("whatsapp:", "").lstrip("+")
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_to,
            "type": "text",
            "text": {"preview_url": False, "body": text_body},
        }

    @staticmethod
    def canonical_conversation_ref(tenant_ref: str, phone_number: str) -> str:
        """Generates a canonical conversation reference for WhatsApp interactions."""
        clean_phone = WhatsAppCloudAdapter.normalize_whatsapp_number(phone_number)
        return f"wa:{tenant_ref}:{clean_phone}"

"""Unit tests for Meta WhatsApp Cloud API adapter."""

from ai_workforce_digital_channel.whatsapp_adapter import WhatsAppCloudAdapter


def test_verify_whatsapp_challenge():
    query = {
        "hub.mode": ["subscribe"],
        "hub.verify_token": ["planwell-wa-verify-token"],
        "hub.challenge": ["1158201203"],
    }
    is_valid, challenge = WhatsAppCloudAdapter.verify_webhook_challenge(query, "planwell-wa-verify-token")
    assert is_valid is True
    assert challenge == "1158201203"


def test_verify_whatsapp_challenge_invalid_token():
    query = {
        "hub.mode": ["subscribe"],
        "hub.verify_token": ["wrong-token"],
        "hub.challenge": ["1158201203"],
    }
    is_valid, challenge = WhatsAppCloudAdapter.verify_webhook_challenge(query, "planwell-wa-verify-token")
    assert is_valid is False
    assert challenge == ""


def test_parse_whatsapp_webhook_payload():
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "metadata": {"phone_number_id": "1006543210"},
                            "messages": [
                                {
                                    "id": "wmid.HBgLMTU1NTAxOTI4MzQVAgASGBQzQUFBN",
                                    "from": "15550192834",
                                    "timestamp": "1725619200",
                                    "type": "text",
                                    "text": {"body": "How much does the Pro tier cost?"},
                                }
                            ],
                        }
                    }
                ]
            }
        ]
    }
    messages = WhatsAppCloudAdapter.parse_webhook(payload)
    assert len(messages) == 1
    assert messages[0].from_number == "whatsapp:+15550192834"
    assert messages[0].body == "How much does the Pro tier cost?"


def test_build_meta_response_payload():
    meta_json = WhatsAppCloudAdapter.build_meta_response_payload("whatsapp:+15550192834", "Pro tier is $49/mo.")
    assert meta_json["messaging_product"] == "whatsapp"
    assert meta_json["to"] == "15550192834"
    assert meta_json["text"]["body"] == "Pro tier is $49/mo."

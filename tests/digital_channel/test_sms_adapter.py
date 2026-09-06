"""Unit tests for Twilio SMS adapter."""

import pytest
from ai_workforce_digital_channel.sms_adapter import TwilioSmsAdapter


def test_parse_twilio_sms_webhook():
    form_data = {
        "From": "+15550192834",
        "To": "+18005550199",
        "Body": "What are your business hours?",
        "MessageSid": "SM1234567890abcdef",
        "AccountSid": "AC1234567890",
    }
    sms = TwilioSmsAdapter.parse_webhook(form_data)
    assert sms.from_number == "+15550192834"
    assert sms.to_number == "+18005550199"
    assert sms.body == "What are your business hours?"
    assert sms.message_sid == "SM1234567890abcdef"


def test_parse_invalid_twilio_sms_webhook():
    with pytest.raises(ValueError):
        TwilioSmsAdapter.parse_webhook({})


def test_build_twiml_response():
    twiml = TwilioSmsAdapter.build_twiml_response("Our office is open Mon-Fri 9am-5pm.")
    assert "<Response><Message>Our office is open Mon-Fri 9am-5pm.</Message></Response>" in twiml


def test_canonical_conversation_ref():
    ref = TwilioSmsAdapter.canonical_conversation_ref("staging-demo", "+1 (555) 019-2834")
    assert ref == "sms:staging-demo:+15550192834"

# 06 Multilingual Agent
# Multilingual Voice Agent Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-ready example of a Multilingual AI Voice Agent for the Voice Agent SaaS platform.

The Multilingual Voice Agent automatically detects or selects the caller's preferred language and conducts the conversation in that language while maintaining access to enterprise knowledge, backend integrations, and workflow automation.

The agent supports:

- Automatic language detection
- Caller language preference
- Dynamic language switching
- Multilingual speech recognition
- Multilingual text generation
- Multilingual speech synthesis
- Cross-language knowledge retrieval
- Human transfer with language-aware routing

---

# 2. Architecture

```
Incoming Call

      │

      ▼

LiveKit Voice Session

      │

      ▼

Language Detection

      │

      ▼

Voice Agent Runtime

      │

 ┌────┼───────────┐

 ▼    ▼           ▼

STT   LLM         TTS

      │

      ▼

Knowledge Search

      │

      ▼

Backend Services

      │

      ▼

Language-Aware Human Transfer
```

---

# 3. Supported Languages

Example languages:

- English
- Urdu
- Arabic
- Spanish
- French
- German
- Italian
- Portuguese
- Hindi
- Chinese
- Japanese
- Korean

Additional languages can be added as supported by the configured STT, LLM, and TTS providers.

---

# 4. Language Selection Flow

```
Incoming Call

      │

Known Preference?

 ┌────┴────┐

 │         │

Yes       No

 │         │

Use Saved  Detect Language

Language       │

               ▼

      Confidence High?

         ┌────┴────┐

         │         │

        Yes       No

         │         │

 Continue    Ask Customer

              │

              ▼

      Begin Conversation
```

---

# 5. Example System Prompt

```text
You are a multilingual AI voice assistant.

Always communicate in the customer's preferred language.

If the customer changes languages during the conversation, continue naturally in the new language.

Use enterprise knowledge when answering questions.

If information is unavailable, state that clearly instead of guessing.

Escalate to a human representative when appropriate.
```

---

# 6. Greeting Examples

**English**

```
Hello, thank you for calling.

How may I assist you today?
```

**Urdu**

```
السلام علیکم۔

میں آپ کی کس طرح مدد کر سکتا ہوں؟
```

**Arabic**

```
مرحبًا.

كيف يمكنني مساعدتك اليوم؟
```

The greeting should match the detected or selected language.

---

# 7. Language Detection

Detection methods:

```
Customer Audio

      │

Speech Detection

      │

Language Identification

      │

Confidence Score

      │

Language Selected
```

If confidence is below a configured threshold, the agent should request confirmation.

---

# 8. Dynamic Language Switching

Example:

```
Customer:

Can we continue in Urdu?

↓

Agent:

ضرور۔

اب ہم اردو میں گفتگو جاری رکھتے ہیں۔
```

The conversation context should remain unchanged while only the interaction language changes.

---

# 9. Knowledge Retrieval

Knowledge search flow:

```
Customer Question

        │

Language Detection

        │

Semantic Search

        │

Knowledge Retrieved

        │

LLM Response

        │

Translate (if required)

        │

Speech Response
```

Knowledge documents may be stored in one or more languages.

---

# 10. Backend Integrations

The multilingual agent may access:

- CRM
- Calendar
- Ticketing system
- Knowledge base
- Billing platform
- Workflow engine
- Notification service

Backend APIs should remain language-independent whenever possible.

---

# 11. Human Transfer

Transfer workflow:

```
Transfer Needed

        │

Determine Language

        │

Locate Matching Agent

        │

Transfer Transcript

        │

Continue Conversation
```

Routing should prioritize representatives who support the customer's preferred language.

---

# 12. Translation Considerations

The platform may use translation when:

- Knowledge is unavailable in the requested language
- Human agents require translated transcripts
- Cross-language workflows are executed

Whenever possible, responses should be generated directly in the customer's language rather than translated from another language.

---

# 13. Security

The multilingual agent should:

- Protect customer information regardless of language
- Maintain tenant isolation
- Validate permissions before accessing sensitive data
- Log language changes
- Preserve transcript integrity

---

# 14. Performance Targets

| Metric | Target |
|--------|-------:|
| Language detection | < 500 ms |
| STT latency | < 500 ms |
| LLM response | < 2 seconds |
| TTS generation | < 500 ms |
| End-to-end response | < 3 seconds |

---

# 15. Observability

Monitor:

- Detected language
- Language switch frequency
- Detection confidence
- STT accuracy
- TTS latency
- Human transfer language match
- Customer satisfaction
- Error rates by language

---

# 16. Testing

Validate:

- Automatic language detection
- Manual language selection
- Dynamic language switching
- Knowledge retrieval in multiple languages
- Human transfer routing
- Mixed-language conversations
- Translation quality
- Unsupported language handling

---

# 17. Best Practices

Always:

- Speak in the customer's preferred language
- Preserve conversation context during language changes
- Confirm low-confidence language detection
- Use localized greetings and terminology
- Match human agents by language when transferring
- Monitor quality across all supported languages

Avoid:

- Mixing languages unnecessarily
- Assuming a language based on location
- Translating sensitive information incorrectly
- Losing context during language switches
- Using unsupported speech models

---

# 18. Example End-to-End Workflow

```
Customer Calls

        │

Detect Language

        │

Localized Greeting

        │

Conversation

        │

Knowledge Search

        │

Backend Services

        │

Language Switch (Optional)

        │

Human Transfer (Optional)

        │

Conversation Ends
```

---

# 19. Future Enhancements

Potential capabilities include:

- Voice cloning by language
- Accent adaptation
- Real-time bidirectional translation
- Regional dialect support
- Personalized pronunciation
- Language preference learning
- Multilingual sentiment analysis

---

# 20. Summary

The Multilingual Voice Agent enables natural conversations across multiple languages while maintaining consistent access to enterprise knowledge, backend integrations, and AI capabilities. By combining language detection, multilingual speech processing, and language-aware routing, the platform delivers an inclusive and scalable voice experience for global organizations.
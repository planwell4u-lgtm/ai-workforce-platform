# 01 Basic Voice Agent
# Basic Voice Agent Example

**Version:** 2.0

---

# 1. Overview

This document provides a production-oriented example of a basic AI voice agent for the Voice Agent SaaS platform.

The example demonstrates the minimum components required to build a real-time conversational voice agent using the platform architecture.

The agent can:

- Answer incoming calls
- Greet callers
- Hold natural conversations
- Answer frequently asked questions
- End calls politely
- Escalate when necessary

This example serves as the foundation for more advanced voice agents.

---

# 2. Architecture

```
Incoming PSTN Call
         │
         ▼
   Twilio SIP Trunk
         │
         ▼
     LiveKit Room
         │
         ▼
 Voice Agent Runtime
         │
 ┌───────┼────────┐
 ▼       ▼        ▼
 STT    LLM      TTS
         │
         ▼
 Conversation Logic
         │
         ▼
 Audio Response
```

---

# 3. Capabilities

The basic agent supports:

- Greeting callers
- Speech recognition
- Natural language understanding
- AI response generation
- Speech synthesis
- Conversation history
- Call termination
- Error recovery

---

# 4. Conversation Flow

```
Incoming Call

      │

Greeting

      │

Listen

      │

Understand Intent

      │

Generate Response

      │

Speak Response

      │

Continue Conversation

      │

Goodbye

      │

End Call
```

---

# 5. Example System Prompt

```text
You are a professional AI voice assistant.

Your responsibilities are:

- Greet callers politely.
- Answer questions clearly.
- Speak naturally and concisely.
- Ask follow-up questions when needed.
- Never invent information.
- Escalate to a human if you cannot confidently help.
- End every conversation politely.
```

---

# 6. Example Greeting

```
Agent:

Hello, and thank you for calling.

My name is Ava, your AI assistant.

How may I help you today?
```

---

# 7. Example Conversation

```
Customer:

What services do you provide?

↓

Agent:

We provide AI-powered voice agents, workflow automation, knowledge management, and customer support solutions.

Is there a particular service you'd like to learn more about?
```

---

# 8. Runtime Flow

```
Audio Stream

      │

Voice Activity Detection

      │

Speech-to-Text

      │

Conversation Context

      │

Large Language Model

      │

Generate Reply

      │

Text-to-Speech

      │

Return Audio
```

---

# 9. Example Agent Configuration

```yaml
agent:
  name: Basic Voice Agent

  language: en-US

  voice: default

  interruption: true

  max_conversation_minutes: 30

  fallback_to_human: true
```

---

# 10. Tool Access

The basic agent may use:

- Knowledge Search
- FAQ Database
- Company Information
- Date & Time
- Basic Calculator

No privileged business operations should be available.

---

# 11. Knowledge Sources

Supported sources:

```
Company FAQ

Knowledge Base

Policies

Documentation

Help Articles
```

If information is unavailable, the agent should acknowledge the limitation rather than guessing.

---

# 12. Error Recovery

When speech recognition fails:

```
Agent:

I'm sorry, I didn't quite catch that.

Could you please repeat your question?
```

After multiple failures:

```
Offer transfer to a human representative.
```

---

# 13. Human Escalation

Escalation conditions include:

- User requests a human
- Repeated misunderstanding
- Unsupported request
- Sensitive issue
- System error

Flow:

```
Escalation Requested

        │

Notify User

        │

Locate Available Agent

        │

Transfer Call
```

---

# 14. Logging

Record the following events:

- Call started
- Greeting completed
- User utterances
- AI responses
- Tool usage
- Escalation
- Call ended

Sensitive information should be redacted where appropriate.

---

# 15. Security

The agent should:

- Respect tenant boundaries
- Never expose confidential information
- Verify identity before accessing protected data
- Follow least-privilege principles
- Avoid storing unnecessary personal information

---

# 16. Performance Targets

Recommended targets:

| Metric | Target |
|--------|-------:|
| Greeting latency | < 1 second |
| STT latency | < 500 ms |
| LLM response | < 2 seconds |
| TTS generation | < 500 ms |
| End-to-end response | < 3 seconds |

---

# 17. Testing

Validate:

- Greeting
- Conversation quality
- Interruptions
- Silence handling
- Speech recognition
- Response accuracy
- Call termination
- Human transfer
- Error recovery

---

# 18. Best Practices

Always:

- Speak naturally
- Keep responses concise
- Confirm ambiguous requests
- Handle interruptions gracefully
- Ask clarifying questions
- Admit uncertainty
- Escalate when appropriate

Avoid:

- Hallucinating answers
- Reading long paragraphs
- Speaking too quickly
- Interrupting callers unnecessarily
- Making promises the system cannot fulfill

---

# 19. Example End-to-End Interaction

```
Customer Calls

        │

Greeting

        │

Customer Question

        │

STT

        │

LLM Processing

        │

Knowledge Search

        │

Generate Answer

        │

TTS

        │

Customer Hears Response

        │

Conversation Continues

        │

Goodbye

        │

Call Ends
```

---

# 20. Summary

The Basic Voice Agent demonstrates the core conversational architecture used throughout the Voice Agent SaaS platform. It establishes the foundation for more advanced agents by combining real-time voice processing, AI reasoning, knowledge retrieval, and graceful escalation into a consistent production-ready interaction model.
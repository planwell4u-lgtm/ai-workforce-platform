# ADR-0004: Voice Platform Selection Decision

**Project:** Voice Agent SaaS Platform  
**Document:** Voice Platform Architecture Strategy  
**ADR Number:** ADR-0004  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will use:

| Capability | Technology |
|---|---|
| PSTN connectivity | Twilio SIP |
| Real-time media infrastructure | LiveKit |
| Voice agent runtime | LiveKit Agents Framework |
| Speech-to-text | Configurable STT providers |
| Text-to-speech | Configurable TTS providers |
| Call orchestration | Platform Voice Service |


The approved voice architecture separates:

- Telephony connectivity
- Real-time media handling
- AI agent execution
- Business logic


---

# 2. Context

Voice communication is the primary interaction channel of the platform.

The system must support:

- Incoming business calls
- Outgoing campaigns
- Real-time AI conversations
- Human transfers
- Call recording
- Transcription
- Multi-tenant phone numbers
- Global scalability


A production voice platform requires:

- Low latency
- Reliable media handling
- SIP support
- Provider flexibility
- Observability
- Failure recovery


---

# 3. Problem Statement

The platform requires a voice architecture that can:


## Business Requirements

Support:

- Multiple businesses
- Multiple phone numbers
- Multiple AI agents
- Different industries


---

## Technical Requirements

Provide:

- Real-time audio streaming
- SIP integration
- Call routing
- Voice AI execution
- Recording support
- Scaling capability


---

## Strategic Requirements

Avoid:

- Vendor lock-in
- Custom telecom infrastructure
- Complex media engineering


---

# 4. Options Considered


---

# Option 1: Build Custom Telecom Infrastructure


## Description

Create a proprietary telephony stack.


Architecture:


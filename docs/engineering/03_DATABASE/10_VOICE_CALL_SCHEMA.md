# Voice Call Schema

**Document ID:** DB-VOICE-009  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for voice communication data in the AI Voice Agent SaaS platform.

The voice domain manages the complete lifecycle of telephone interactions:

- Phone number management
- SIP connectivity
- Telephony providers
- Call routing
- Call sessions
- Call recordings
- Voice events
- Human transfers
- Provider metadata

The voice schema integrates with:

- Twilio SIP
- LiveKit Voice Infrastructure
- STT providers
- TTS providers
- AI Agent Runtime

---

# 2. Voice Architecture

High-level flow:


PSTN Network

  |

Telephony Provider

  |

SIP Connection

  |

LiveKit Room

  |

Voice Agent Runtime

  |

Conversation

  |

Analytics


---

# 3. Voice Design Principles

## 3.1 Call Lifecycle Tracking

Every call must have:

- Unique identifier
- Tenant ownership
- Agent assignment
- Provider tracking
- State history

---

## 3.2 Provider Independence

The schema must support multiple providers.

Examples:


Twilio

Vonage

Telnyx

Custom SIP Provider


---

## 3.3 Event-Based Architecture

Call state changes are stored as events.

Example:


Call Started

  |

Agent Joined

  |

Customer Spoke

  |

Tool Called

  |

Transfer

  |

Call Ended


---

# 4. Voice Schema

Schema:


voice


---

# 5. Voice Tables Overview


voice.providers

voice.phone_numbers

voice.sip_connections

voice.call_routes

voice.call_sessions

voice.call_participants

voice.call_events

voice.recordings

voice.transfers

voice.voice_configs


---

# 6. Voice Provider Entity

Table:


voice.providers


Purpose:

Stores supported communication providers.

Examples:


Twilio

LiveKit

Telnyx


---

Structure:

```sql
CREATE TABLE voice.providers
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,

    provider_type TEXT NOT NULL,

    status TEXT DEFAULT 'active',

    created_at TIMESTAMPTZ DEFAULT now()
);
7. Provider Types

Supported:

Type	Purpose
telephony	PSTN connectivity
sip	SIP trunking
realtime	Media processing
speech	STT/TTS
8. Phone Number Model

Table:

voice.phone_numbers

Purpose:

Stores customer assigned phone numbers.

Examples:

+1 555 555 1000

+44 20 1234 5678


Structure:

CREATE TABLE voice.phone_numbers
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

phone_number TEXT NOT NULL,

provider_id UUID,

status TEXT DEFAULT 'active',

created_at TIMESTAMPTZ DEFAULT now()
);
9. Phone Number Lifecycle
Available

   |

Assigned

   |

Active

   |

Suspended

   |

Released

10. SIP Connection Model

Table:

voice.sip_connections

Purpose:

Stores SIP trunk configuration.

Example:

Twilio SIP Trunk

LiveKit SIP Gateway

Enterprise SIP Provider


Structure:

CREATE TABLE voice.sip_connections
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

provider_id UUID NOT NULL,

connection_name TEXT,

configuration JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
11. SIP Security

Credentials must not be stored directly.

Store:

Encrypted Secret Reference

+

Credential Provider Reference


Example:

Vault Secret ID

AWS Secrets Manager Key

GCP Secret Manager Reference

12. Call Routing Model

Table:

voice.call_routes

Purpose:

Determines which agent handles incoming calls.

Example:

Phone Number

      |

Business Hours Rule

      |

Agent Assignment


Structure:

CREATE TABLE voice.call_routes
(
id UUID PRIMARY KEY,

tenant_id UUID NOT NULL,

phone_number_id UUID NOT NULL,

agent_id UUID NOT NULL,

priority INTEGER DEFAULT 1

);
13. Call Session Entity

Table:

voice.call_sessions

Purpose:

Main call lifecycle record.

Example:

CREATE TABLE voice.call_sessions
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

agent_id UUID,

provider_call_id TEXT,

direction TEXT,

status TEXT,

started_at TIMESTAMPTZ,

ended_at TIMESTAMPTZ
);
14. Call Direction

Supported:

inbound

outbound

15. Call Status

Lifecycle:

initiated

ringing

connected

active

transferring

completed

failed

cancelled

16. Call Lifecycle
Incoming Call

      |

Create Session

      |

Identify Tenant

      |

Resolve Agent

      |

Start LiveKit Room

      |

Run AI Agent

      |

Store Conversation

      |

Complete Call

17. Call Participants

Table:

voice.call_participants

Purpose:

Tracks entities involved.

Participants:

Customer

AI Agent

Human Operator

Supervisor


Structure:

CREATE TABLE voice.call_participants
(
id UUID PRIMARY KEY,

call_session_id UUID NOT NULL,

participant_type TEXT NOT NULL,

identity TEXT,

joined_at TIMESTAMPTZ,

left_at TIMESTAMPTZ
);
18. Call Events

Table:

voice.call_events

Purpose:

Immutable event history.

Examples:

CALL_STARTED

AGENT_CONNECTED

CUSTOMER_SPEAKING

TRANSFER_REQUESTED

CALL_COMPLETED


Structure:

CREATE TABLE voice.call_events
(
id UUID PRIMARY KEY,

call_session_id UUID NOT NULL,

event_type TEXT NOT NULL,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
19. Recording Model

Table:

voice.recordings

Purpose:

Stores call recording metadata.

Important:

Audio files are stored externally.

Database stores:

Storage URL

Duration

Format

Size

Encryption Metadata


Structure:

CREATE TABLE voice.recordings
(
id UUID PRIMARY KEY,

call_session_id UUID NOT NULL,

storage_url TEXT,

duration_seconds INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
20. Human Transfer Model

Table:

voice.transfers

Purpose:

Tracks AI-to-human escalation.

Example:

AI Agent

   |

Transfer Request

   |

Human Agent


Fields:

transfer_reason

destination

status

completed_at

21. Voice Configuration

Table:

voice.voice_configs

Purpose:

Stores voice settings.

Examples:

Voice Provider

Voice Model

Language

Speaking Speed


Example:

{
"voice":"alloy",
"language":"en-US",
"speed":1.0
}
22. Integration With Agent Runtime

Flow:

Call Session

      |

Agent Assignment

      |

Runtime Session

      |

Conversation

      |

Transcript

23. Multi-Tenant Requirements

All tenant-owned voice tables require:

tenant_id UUID NOT NULL

Required RLS:

voice.*
24. High Volume Tables

Expected growth:

Table	Growth
call_events	Very High
call_sessions	High
recordings	Medium
participants	High
25. Partitioning Strategy

Future partition candidates:

voice.call_events

voice.call_sessions


Partition key:

created_at

or

tenant_id
26. Index Requirements

Tenant lookup:

CREATE INDEX idx_calls_tenant
ON voice.call_sessions(tenant_id);

Provider lookup:

CREATE INDEX idx_calls_provider_id
ON voice.call_sessions(provider_call_id);

Event lookup:

CREATE INDEX idx_call_events_session
ON voice.call_events(call_session_id);
27. Security Requirements

Required:

Encrypt provider credentials
Protect recordings
Audit access
Validate tenant ownership
Restrict recording access
28. Future Extensions

Possible additions:

voice.voice_quality_metrics

voice.sentiment_analysis

voice.call_costs

voice.carrier_events

voice.real_time_metrics

29. Related Documents

Next:

10_CONVERSATION_SCHEMA.md

11_KNOWLEDGE_SCHEMA.md

12_MEMORY_SCHEMA.md
End of Document
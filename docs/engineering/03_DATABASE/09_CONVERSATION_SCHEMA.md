# Conversation Schema

**Document ID:** DB-CONV-010  
**Version:** 2.0  
**Status:** Production Design Specification  
**Category:** Database Engineering  
**Last Updated:** 2026-07-24

---

# 1. Overview

This document defines the database architecture for conversation management in the AI Voice Agent SaaS platform.

The conversation domain stores the complete interaction history between:

- Customers
- AI agents
- Human agents
- External tools
- Automation workflows

The conversation system provides:

- Message storage
- Transcript management
- Conversation events
- AI reasoning traces
- Summaries
- Sentiment analysis
- Quality evaluation
- Search capabilities

---

# 2. Conversation Architecture

High-level flow:


Voice Call

|

Call Session

|

Conversation

|

Messages

|

Transcript

|

Summary

|

Analytics


---

# 3. Conversation Design Principles

## 3.1 Immutable History

Conversation messages are append-only.

Previous messages should not be modified.

Benefits:

- Auditability
- Replay capability
- AI evaluation
- Compliance

---

## 3.2 Event-Based Model

Conversation state changes are stored as events.

Examples:


Conversation Started

User Message Received

Agent Response Generated

Tool Executed

Human Transfer

Conversation Completed


---

## 3.3 Channel Independence

The conversation model supports multiple channels:


Voice

Chat

SMS

Email

Web

WhatsApp


---

# 4. Conversation Schema

Schema:


conversation


---

# 5. Conversation Tables Overview


conversation.conversations

conversation.participants

conversation.messages

conversation.message_parts

conversation.transcripts

conversation.events

conversation.summaries

conversation.feedback

conversation.evaluations


---

# 6. Conversations Table

Table:


conversation.conversations


Purpose:

Main conversation entity.

A conversation represents one continuous interaction.

---

Example:


Customer calls company

    |

AI Agent answers

    |

Conversation created


---

Structure:

```sql
CREATE TABLE conversation.conversations
(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    tenant_id UUID NOT NULL,

    agent_id UUID,

    call_session_id UUID,

    channel TEXT NOT NULL,

    status TEXT NOT NULL,

    started_at TIMESTAMPTZ DEFAULT now(),

    ended_at TIMESTAMPTZ
);
7. Conversation Channels

Supported:

Channel	Description
voice	Telephone interaction
chat	Web chat
sms	Text messages
email	Email conversation
api	Programmatic interaction
8. Conversation Lifecycle
Created

 |

Active

 |

Waiting

 |

Completed

 |

Archived

9. Conversation Participants

Table:

conversation.participants

Purpose:

Tracks all entities involved.

Participants:

Customer

AI Agent

Human Agent

System

Tool


Structure:

CREATE TABLE conversation.participants
(
id UUID PRIMARY KEY,

conversation_id UUID NOT NULL,

participant_type TEXT NOT NULL,

identity TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
10. Participant Types
customer

agent

human

system

tool

11. Messages Table

Table:

conversation.messages

Purpose:

Stores conversation messages.

Examples:

Customer:

"Book me an appointment"


AI:

"I can help schedule that."


Structure:

CREATE TABLE conversation.messages
(
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

tenant_id UUID NOT NULL,

conversation_id UUID NOT NULL,

sender_type TEXT NOT NULL,

content TEXT,

message_type TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
12. Message Sender Types
customer

assistant

human

system

tool

13. Message Types

Examples:

Type	Purpose
text	Normal message
audio	Voice segment
tool_call	Tool invocation
tool_result	Tool response
system	Internal message
14. Message Parts Model

Table:

conversation.message_parts

Purpose:

Supports multimodal messages.

Example:

A voice message:

Message

 |

+ Audio

+ Transcript

+ Metadata


Structure:

CREATE TABLE conversation.message_parts
(
id UUID PRIMARY KEY,

message_id UUID NOT NULL,

part_type TEXT NOT NULL,

content JSONB

);
15. Transcript Model

Table:

conversation.transcripts

Purpose:

Stores speech-to-text output.

Data sources:

Whisper

Deepgram

AssemblyAI

Other STT Providers


Structure:

CREATE TABLE conversation.transcripts
(
id UUID PRIMARY KEY,

conversation_id UUID NOT NULL,

speaker TEXT,

text TEXT,

start_time_ms INTEGER,

end_time_ms INTEGER,

created_at TIMESTAMPTZ DEFAULT now()
);
16. Transcript Example
00:01 Customer:

"Hello, I need help"


00:04 Agent:

"How can I assist you?"

17. Conversation Events

Table:

conversation.events

Purpose:

Stores conversation timeline.

Examples:

conversation_started

message_received

agent_response

tool_called

transfer_started

conversation_completed


Structure:

CREATE TABLE conversation.events
(
id UUID PRIMARY KEY,

conversation_id UUID NOT NULL,

event_type TEXT NOT NULL,

payload JSONB,

created_at TIMESTAMPTZ DEFAULT now()
);
18. Conversation Timeline

Example:

09:00 Call Started

09:01 Customer Greeting

09:02 Intent Detected

09:03 Calendar Tool Used

09:04 Appointment Created

09:05 Call Completed

19. Conversation Summaries

Table:

conversation.summaries

Purpose:

Stores AI-generated summaries.

Example:

Customer requested appointment.

Appointment scheduled for Monday.


Structure:

CREATE TABLE conversation.summaries
(
id UUID PRIMARY KEY,

conversation_id UUID NOT NULL,

summary TEXT,

generated_by TEXT,

created_at TIMESTAMPTZ DEFAULT now()
);
20. Conversation Feedback

Table:

conversation.feedback

Purpose:

Customer or operator feedback.

Examples:

Rating

Comment

Resolution status

21. Conversation Evaluation

Table:

conversation.evaluations

Purpose:

AI quality measurement.

Metrics:

Accuracy

Response Quality

Latency

Task Completion

Customer Satisfaction

22. AI Runtime Integration

Conversation connects with runtime:

Agent Runtime

      |

Runtime Session

      |

Conversation

      |

Messages

      |

Transcript

23. Memory Integration

After conversation completion:

Conversation

      |

Extract Important Facts

      |

Memory Service

      |

Long Term Memory

24. Knowledge Integration

During conversation:

User Question

      |

Retrieve Knowledge

      |

Generate Answer

      |

Store Result

25. Multi-Tenant Requirements

All customer-owned tables require:

tenant_id UUID NOT NULL

RLS required:

conversation.*
26. High Volume Tables

Expected growth:

Table	Growth
messages	Very High
transcripts	Very High
events	Very High
evaluations	Medium
27. Partitioning Strategy

Future candidates:

conversation.messages

conversation.events

conversation.transcripts


Partition by:

created_at

tenant_id

28. Index Requirements

Conversation lookup:

CREATE INDEX idx_conversation_tenant
ON conversation.conversations(tenant_id);

Message retrieval:

CREATE INDEX idx_messages_conversation
ON conversation.messages(conversation_id);

Transcript search:

CREATE INDEX idx_transcript_conversation
ON conversation.transcripts(conversation_id);
29. Security Requirements

Required:

Tenant isolation
Transcript protection
Recording access controls
Audit logging
Data retention policies
30. Future Extensions

Possible additions:

conversation.sentiment

conversation.intent_history

conversation.agent_scores

conversation.customer_profile_updates

conversation.compliance_checks

31. Related Documents

Next:

11_KNOWLEDGE_SCHEMA.md

12_MEMORY_SCHEMA.md

13_WORKFLOW_SCHEMA.md
End of Document
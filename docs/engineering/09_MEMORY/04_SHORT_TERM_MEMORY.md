# Short-Term Memory

**Module:** 09_MEMORY  
**Document:** 04_SHORT_TERM_MEMORY.md  
**Status:** Production Architecture  
**Version:** 2.0  
**Owner:** Memory Platform Engineering

---

# Overview

Short-Term Memory (STM) stores information that is immediately relevant to the current interaction or recent conversations. It enables AI agents to maintain conversational continuity, remember recent events, and complete multi-turn tasks without repeatedly asking for the same information.

Unlike Long-Term Memory, Short-Term Memory is temporary and optimized for fast retrieval.

---

# Objectives

The Short-Term Memory system provides:

- Conversation continuity
- Session awareness
- Multi-turn reasoning
- Temporary context storage
- Active task tracking
- Immediate personalization
- Low-latency retrieval

---

# Position In Platform Architecture

```
                  User

                   │

                   ▼

            Voice Platform

                   │

                   ▼

              AI Runtime

                   │

                   ▼

          Short-Term Memory

                   │

                   ▼

         Context Assembly Layer

                   │

                   ▼

              LLM Response
```

---

# Purpose

Short-Term Memory is responsible for remembering information that is useful during an active conversation or for a limited period after it.

Examples include:

- User's current request
- Active booking information
- Temporary verification codes
- Conversation state
- Current workflow step
- Pending tool results

---

# Characteristics

| Property | Value |
|-----------|-------|
| Lifetime | Minutes to days |
| Retrieval Speed | Very Fast |
| Storage | Redis + PostgreSQL |
| Persistence | Temporary |
| Scope | Session or Recent Conversations |

---

# Memory Architecture

```
User Conversation

        │

        ▼

Conversation Manager

        │

        ▼

Short-Term Memory Manager

        │

 ┌──────┼────────┐

 ▼      ▼        ▼

Session Active Task Recent History

Memory   State     Context

        │

        ▼

Context Builder
```

---

# Information Stored

Short-Term Memory stores:

- Recent messages
- Tool execution results
- Active conversation goals
- Temporary preferences
- Session variables
- Current workflow state
- Recent user decisions
- Unfinished tasks

---

# Conversation Context

Example:

```
User:

"I want to book an appointment."

↓

Store:

Intent = Appointment Booking
```

Later:

```
User:

"Tomorrow at 3 PM."

↓

Use Existing Context

↓

Book Appointment
```

---

# Session Memory

Each active session has isolated memory.

```
Session

├── Messages

├── Current Intent

├── Workflow State

├── Tool Results

└── Temporary Variables
```

---

# Active Task Tracking

The system tracks ongoing tasks.

Example:

```
Verify Identity

↓

Collect Address

↓

Collect Phone Number

↓

Complete Verification
```

If interrupted:

```
Resume From

Current Step
```

---

# Context Window Management

Short-Term Memory manages the context window by:

- Keeping recent exchanges
- Removing redundant content
- Summarizing long conversations
- Maintaining token limits

Flow:

```
Conversation

↓

Recent Messages

↓

Summarization

↓

Optimized Context
```

---

# Memory Creation

Short-Term Memory is created from:

- User messages
- AI responses
- Tool outputs
- Workflow events
- API responses

Example:

```
Conversation Event

↓

Memory Extraction

↓

Short-Term Memory
```

---

# Memory Updates

STM changes continuously.

Example:

```
Current Destination:

New York

↓

Updated To

Boston
```

Older temporary values are replaced with the latest information.

---

# Memory Expiration

Short-Term Memory automatically expires.

Expiration triggers include:

- Session completion
- Inactivity timeout
- Workflow completion
- Configurable TTL
- Memory consolidation

Example:

```
Conversation Ends

↓

TTL Expires

↓

Memory Removed
```

---

# Memory Promotion

Important Short-Term Memories can become Long-Term Memories.

Example:

```
Temporary Preference

↓

Repeated Usage

↓

Long-Term Preference
```

Promotion criteria:

- High importance
- Frequent occurrence
- User confirmation
- Business relevance

---

# Memory Retrieval

Retrieval prioritizes:

- Current session
- Recent interactions
- Active tasks
- Workflow context

Pipeline:

```
User Input

↓

Session Lookup

↓

Recent Context

↓

Relevant STM

↓

Prompt Builder
```

---

# AI Runtime Integration

The AI Runtime uses STM for:

- Multi-turn conversations
- Tool coordination
- Workflow execution
- Response generation
- Context injection

---

# RAG Integration

STM complements RAG.

```
User Query

      │

      ▼

Short-Term Memory

      +

Enterprise Knowledge

      ▼

Combined Context

      ▼

LLM
```

---

# Multi-Agent Support

Multiple agents may access shared session memory.

Example:

```
Supervisor Agent

      │

 ┌────┼────┐

 ▼    ▼    ▼

Sales Support Billing

      │

      ▼

Shared Session Memory
```

---

# Multi-Tenant Isolation

Every tenant maintains isolated Short-Term Memory.

```
Tenant

├── Active Sessions

├── Temporary Context

├── Workflow State

└── Session Variables
```

Isolation is enforced using:

- Tenant IDs
- Session IDs
- Access policies

---

# Security

Short-Term Memory protects:

- Temporary personal data
- Session information
- Authentication state
- Workflow variables

Security includes:

- Encryption
- Authorization
- Automatic expiration
- Audit logging

---

# Performance Targets

| Operation | Target |
|------------|--------|
| Session lookup | <20 ms |
| Memory retrieval | <50 ms |
| Context assembly | <100 ms |
| Session update | <20 ms |

---

# Storage Architecture

Recommended storage:

## Redis

Stores:

- Active sessions
- Temporary variables
- Cached context

---

## PostgreSQL

Stores:

- Session metadata
- Audit records
- Recovery information

---

# Monitoring

Track:

- Active sessions
- Memory size
- Cache hit ratio
- Session duration
- Expired memories
- Retrieval latency

---

# Database Model

Recommended tables:

```
conversation_sessions

session_memory

session_variables

active_tasks

conversation_state

session_events
```

---

# Technology Stack

## Backend

- Python
- FastAPI

## Cache

- Redis

## Database

- PostgreSQL

## AI Framework

- LangGraph
- LangChain

---

# Integration With Other Modules

```
05_LONG_TERM_MEMORY.md

08_WORKING_MEMORY.md

10_MEMORY_RETRIEVAL_ENGINE.md

12_MEMORY_CONSOLIDATION.md

17_MEMORY_AGENT_INTEGRATION.md

07_AI_RUNTIME
```

---

# Future Enhancements

Planned improvements:

- Adaptive session summarization
- Predictive context selection
- AI-driven memory prioritization
- Automatic task recovery
- Intelligent session compression

---

# Summary

Short-Term Memory enables AI agents to maintain conversational continuity and execute complex multi-turn workflows by storing temporary context, active tasks, and recent interactions.

Its fast retrieval, automatic expiration, and seamless integration with the AI Runtime provide responsive, context-aware conversations while preparing valuable information for long-term memory when appropriate.
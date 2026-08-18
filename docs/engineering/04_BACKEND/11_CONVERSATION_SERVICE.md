# Conversation Service

**Module:** 04_BACKEND

**Document:** 11_CONVERSATION_SERVICE

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

The Conversation Service manages all conversational data generated during AI agent interactions.

It provides the persistence and orchestration layer for conversations, messages, transcripts, summaries, AI responses, and conversation lifecycle management.

The service acts as the bridge between the Call Control Service, AI Runtime, Memory Service, Knowledge System, and Analytics Platform.

---

# Responsibilities

The Conversation Service manages:

- Conversation lifecycle
- Conversation sessions
- User messages
- AI responses
- Voice transcripts
- Message history
- Conversation metadata
- Conversation summaries
- Conversation state
- Conversation search
- Conversation export
- Conversation retention
- Conversation analytics events

---

# Architecture

                     API

                      │

                      ▼

          Conversation Service


  ┌───────────────────┼───────────────────┐

  ▼                   ▼                   ▼

Repository AI Runtime Event Bus

  │                   │

  ▼                   ▼

PostgreSQL Memory / RAG


---

# Service Dependencies

The Conversation Service depends on:

- Call Control Service
- Agent Service
- Session Service
- AI Runtime Service
- Memory Service
- RAG Knowledge Service
- Analytics Service
- Event Publisher
- Redis Cache
- PostgreSQL Database

---

# Conversation Types

Supported conversation sources:


Inbound Voice Call

Outbound Voice Call

Web Chat

API Conversation

Testing Session

Agent Simulation


---

# Database Tables

Primary tables:


conversations

conversation_messages

conversation_participants

conversation_transcripts

conversation_summaries

conversation_metadata

conversation_events


Related:


calls

call_sessions

agents

users

tenants

knowledge_sources


---

# Public Responsibilities


Create Conversation

Start Conversation

Add Message

Add Transcript

Update Conversation

Get Conversation

List Conversations

Search Conversations

Generate Summary

Close Conversation

Archive Conversation

Export Conversation


---

# Conversation Lifecycle


Conversation Created

    ↓

Session Connected

    ↓

Messages Received

    ↓

AI Processing

    ↓

Responses Generated

    ↓

Conversation Active

    ↓

Summary Generated

    ↓

Conversation Closed

    ↓

Archived


---

# Conversation States


Created

Active

Waiting

Completed

Failed

Archived


---

# Conversation Model

A conversation contains:


Conversation ID

Tenant ID

Agent ID

Session ID

Call ID

Channel

Participants

Start Time

End Time

Status

Language

Summary

Metadata


---

# Message Model

Each message contains:


Message ID

Conversation ID

Role

Content

Timestamp

Token Usage

Latency

Model Information

Metadata


Roles:


User

Assistant

System

Tool


---

# Voice Transcript Management

The service stores:


Raw Transcript

Speaker Labels

Timestamps

Confidence Scores

Language

Processing Status


Flow:


Caller Audio

    ↓

STT Provider

    ↓

Transcript

    ↓

Conversation Service

    ↓

Storage


---

# AI Response Tracking

The service records:


Prompt

Model

Response

Tokens

Latency

Tools Used

Reasoning Metadata

Completion Status


---

# Conversation Context Management

The service provides context to AI Runtime:


Previous Messages

User Information

Agent Configuration

Knowledge Context

Memory Retrievals


Flow:


Conversation Service

    ↓

Context Builder

    ↓

AI Runtime

    ↓

Response Generation


---

# Conversation Search

Supported search:


Conversation ID

Customer Number

Agent

Date Range

Keywords

Transcript Content

Metadata


---

# Conversation Summary

Summaries contain:


Overview

Customer Intent

Important Information

Actions Taken

Follow-up Required

Sentiment

Outcome


Generated after:


Call Completion

Manual Request

Scheduled Processing


---

# Events Published


ConversationCreated

ConversationStarted

MessageAdded

TranscriptUpdated

SummaryGenerated

ConversationCompleted

ConversationArchived


---

# Events Consumed


CallStarted

CallEnded

AgentUpdated

MemoryUpdated

KnowledgeUpdated

TenantSuspended


---

# Real-Time Conversation Flow

During a live interaction:


Caller

↓

STT

↓

Conversation Service

↓

AI Runtime

↓

LLM

↓

TTS

↓

Caller


---

# Storage Strategy

Conversation data is divided into:

## Hot Data

Frequently accessed:


Active Conversations

Recent Messages

Current Session State


Stored in:


PostgreSQL

Redis Cache


---

## Cold Data

Historical data:


Completed Conversations

Full Transcripts

Recordings Metadata


Stored in:


PostgreSQL

Object Storage


---

# Cache Strategy

Cached data:


Active Conversation State

Recent Messages

Agent Context

Session Metadata


Redis improves real-time response latency.

---

# Security Responsibilities

The service enforces:

- Tenant isolation
- Conversation access control
- Transcript privacy
- Data retention policies
- Encryption of sensitive data
- Audit logging

---

# Privacy Controls

Supported:


Conversation Retention

Transcript Deletion

Data Export

PII Masking

Access Logging


---

# Error Handling

Domain exceptions:


ConversationNotFound

InvalidConversationState

MessageCreationFailed

TranscriptProcessingFailed

SummaryGenerationFailed

AccessDenied


---

# Performance Guidelines

The service should:

- Support real-time message ingestion
- Handle high-frequency transcript writes
- Use asynchronous processing
- Batch historical operations
- Optimize conversation queries
- Partition large datasets

---

# Testing Requirements

The Conversation Service must include:

- Conversation lifecycle tests
- Message persistence tests
- Transcript processing tests
- Context generation tests
- Search tests
- Permission tests
- Tenant isolation tests
- Load tests
- Data retention tests

---

# Related Documents

- 10_CALL_CONTROL_SERVICE.md
- 12_SESSION_SERVICE.md
- 13_MEMORY_SERVICE.md
- 14_KNOWLEDGE_SERVICE.md
- 15_RAG_SERVICE.md
- 03_DATABASE/31_CALL_DATA_MODEL.md
- 06_AI_RUNTIME

---

# Summary

The Conversation Service provides the central record of every AI interaction within the Voice Agent SaaS Platform.

It manages conversations, messages, transcripts, summaries, and context while enabling AI Runtime, Memory, RAG, and Analytics systems to build intelligent and persistent customer interactions.
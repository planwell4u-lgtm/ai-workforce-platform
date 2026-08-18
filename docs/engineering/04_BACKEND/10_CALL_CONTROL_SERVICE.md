# Call Control Service

**Module:** 04_BACKEND

**Document:** 10_CALL_CONTROL_SERVICE

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

The Call Control Service manages the complete lifecycle of voice calls within the Voice Agent SaaS Platform.

It provides the orchestration layer between external telephony providers, real-time communication infrastructure, AI agent runtime, and internal platform services.

The service controls inbound and outbound calls, call routing, session lifecycle, transfers, recordings, SIP interactions, and real-time call events.

---

# Responsibilities

The Call Control Service manages:

- Inbound call handling
- Outbound call initiation
- Call routing
- Call state management
- SIP session control
- LiveKit room lifecycle
- Twilio call control
- Call transfers
- Human agent escalation
- Call recording management
- Call metadata
- DTMF handling
- Call termination
- Call event publishing
- Webhook processing
- Call security validation

---

# Architecture

                     API

                      │

                      ▼

              Call Control Service


    ┌─────────────────┼─────────────────┐

    ▼                 ▼                 ▼

Call Repository Telephony Adapter Event Bus

    │                 │

    ▼                 ▼

PostgreSQL Twilio / SIP

                      │

                      ▼

                   LiveKit

                      │

                      ▼

               AI Agent Runtime

---

# Service Dependencies

The Call Control Service depends on:

- Agent Service
- Voice Service
- Session Service
- Conversation Service
- LiveKit Integration
- Twilio Integration
- SIP Gateway
- Recording Service
- Event Publisher
- Redis Cache
- PostgreSQL Database

---

# Supported Telephony Providers

The service provides abstraction for:

## PSTN Providers

Examples:

- Twilio
- SIP Trunk Providers
- Cloud Telephony Providers


## Real-Time Media Providers

Examples:

- LiveKit
- WebRTC Infrastructure

---

# Database Tables

Primary tables:


calls

call_sessions

call_participants

call_routes

call_transfers

call_recordings

call_events

call_webhooks


Related:


agents

voice_profiles

conversations

tenants

integrations


---

# Public Responsibilities


Create Call

Start Call

Answer Call

Reject Call

End Call

Pause Call

Resume Call

Transfer Call

Add Participant

Remove Participant

Get Call Status

Get Call History

Enable Recording

Disable Recording

Process Webhook


---

# Call Lifecycle


Call Created

  ↓

Routing Decision

  ↓

Agent Assignment

  ↓

Voice Configuration Loaded

  ↓

Media Session Created

  ↓

AI Runtime Connected

  ↓

Conversation Started

  ↓

Active Call

  ↓

Call Completed

  ↓

Post Processing

  ↓

Analytics Generated


---

# Call States


Created

Initiating

Ringing

Answered

Connecting

Active

On Hold

Transferring

Completed

Failed

Cancelled


State transitions are validated by the service.

---

# Inbound Call Flow


Caller

↓

PSTN Network

↓

Twilio

↓

Webhook

↓

Call Control Service

↓

Tenant Routing

↓

Agent Selection

↓

LiveKit Room Creation

↓

AI Agent Runtime

↓

Conversation


---

# Outbound Call Flow


Campaign / API Request

    ↓

Call Control Service

    ↓

Validate Tenant

    ↓

Select Agent

    ↓

Select Voice

    ↓

Create Call Session

    ↓

Twilio SIP Dial

    ↓

LiveKit Connection

    ↓

AI Conversation


---

# Call Routing

Routing decisions consider:


Tenant Configuration

Phone Number

Business Hours

Agent Availability

Language

Voice Configuration

Fallback Rules


Example:


Incoming Number

    ↓

Tenant Lookup

    ↓

Routing Rules

    ↓

Agent Assignment

    ↓

Call Connection


---

# LiveKit Integration

The service manages:


Room Creation

Participant Connection

Agent Dispatch

Media Tracks

Room Cleanup

Connection Status


Flow:


Call Control Service

      ↓

LiveKit API

      ↓

Room Created

      ↓

Agent Worker Joins

      ↓

Audio Stream Active


---

# Twilio Integration

The service manages:


Incoming Webhooks

Outgoing Calls

SIP Trunks

Call Status Callbacks

Recording Callbacks

Transfer Requests


---

# Call Transfer

Supported transfer types:

## AI To Human


AI Agent

↓

Transfer Request

↓

Human Queue

↓

Human Agent


---

## AI To Another Agent


Agent A

↓

Routing

↓

Agent B


---

# Call Recording

The service controls:


Recording Start

Recording Stop

Recording Status

Storage Location

Retention Policy

Access Permissions


Recordings are stored securely.

---

# Call Events

Published events:


CallCreated

CallStarted

CallAnswered

CallConnected

CallTransferred

CallRecordingStarted

CallRecordingStopped

CallEnded

CallFailed


---

# Events Consumed


AgentCreated

AgentUpdated

VoiceUpdated

TenantUpdated

SubscriptionChanged

IntegrationUpdated


---

# Call Session Management

Each active call maintains:


Call ID

Tenant ID

Agent ID

Session ID

LiveKit Room ID

Provider Call ID

Caller Number

Destination Number

Start Time

End Time

Status


---

# Webhook Processing

The service handles:


Twilio Call Events

LiveKit Events

Recording Events

Provider Status Events


Webhook requirements:

- Signature validation
- Idempotency handling
- Replay protection
- Audit logging

---

# Cache Strategy

Cached data:


Tenant Routing Rules

Phone Number Mapping

Agent Availability

Provider Configuration

Active Sessions


Redis is used for low-latency call operations.

---

# Security Responsibilities

The service enforces:

- Tenant isolation
- Caller authentication
- Webhook signature validation
- Provider credential protection
- Call access permissions
- Recording access control
- Sensitive metadata protection

---

# Error Handling

Domain exceptions:


CallNotFound

InvalidCallState

RoutingFailed

ProviderUnavailable

TransferFailed

RecordingUnavailable

InvalidWebhook

CallConnectionFailed


---

# Performance Guidelines

The service should:

- Maintain low call setup latency
- Avoid synchronous blocking operations
- Use async provider communication
- Cache routing decisions
- Handle concurrent calls horizontally
- Support high-volume outbound dialing

---

# Testing Requirements

The Call Control Service must include:

- Call lifecycle tests
- Routing tests
- Twilio integration tests
- LiveKit integration tests
- Transfer tests
- Recording tests
- Webhook validation tests
- Failure recovery tests
- Load tests
- Tenant isolation tests

---

# Related Documents

- 08_AGENT_SERVICE.md
- 09_VOICE_SERVICE.md
- 11_CONVERSATION_SERVICE.md
- 12_SESSION_SERVICE.md
- 03_DATABASE/31_CALL_DATA_MODEL.md
- 30_OPENAPI_SPECS/30.5_CALL_CONTROL_API.yaml
- 37_OBSERVABILITY

---

# Summary

The Call Control Service is the orchestration layer responsible for managing real-time voice communication workflows.

It abstracts telephony providers, manages call lifecycle state, coordinates LiveKit media sessions, integrates with AI agents, and provides reliable call operations required for a production-grade Voice Agent SaaS Platform.
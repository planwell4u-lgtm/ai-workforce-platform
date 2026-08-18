# PROJECT_GLOSSARY

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document defines the standard terminology used throughout the Voice Agent SaaS Platform.

Its objectives are to:

- Establish a common vocabulary
- Eliminate ambiguous terminology
- Ensure consistency across documentation, code, APIs, and database schemas
- Help onboard developers and AI assistants
- Reduce naming conflicts

All contributors should use the terms defined in this document unless a newer version or an approved ADR specifies otherwise.

---

# Naming Rules

Whenever possible:

- Use one term for one concept.
- Avoid synonyms for core entities.
- Keep terminology consistent across:
  - Database tables
  - API endpoints
  - Source code
  - Documentation
  - UI
- Prefer descriptive names over abbreviations.

---

# Business Terms

## Tenant

A customer organization using the SaaS platform.

Every business resource belongs to exactly one tenant unless explicitly documented otherwise.

---

## Organization

A business entity operating within the platform.

Depending on future licensing models, a tenant may contain one or more organizations.

---

## Workspace

A logical working environment within a tenant.

A workspace groups resources such as agents, knowledge bases, workflows, and users.

---

## User

A human who authenticates and interacts with the platform.

Examples:

- Administrator
- Supervisor
- Agent Manager
- Analyst

---

## Role

A collection of permissions assigned to users.

Examples:

- Owner
- Admin
- Manager
- Operator
- Viewer

---

## Permission

A specific capability granted through a role.

Example:

```
agents:create
calls:view
knowledge:update
```

---

# Voice Platform Terms

## Voice Agent

An AI-powered conversational entity that answers or initiates phone calls.

A voice agent consists of:

- Prompt
- Voice
- Workflow
- Knowledge
- Tools
- Memory
- Configuration

---

## Call

A single inbound or outbound voice interaction.

Every call has:

- Internal Call ID
- Provider Call ID
- Status
- Timeline
- Recording Metadata

---

## Call Session

The runtime lifecycle of a call from initiation to termination.

---

## Call Event

A timestamped event occurring during a call.

Examples:

- Ringing
- Answered
- AI Joined
- Transfer Requested
- Recording Started
- Hangup

---

## Recording

Audio captured during a voice conversation.

Recording metadata remains even if the recording itself expires.

---

## SIP

Session Initiation Protocol used for telephony signaling.

---

## Twilio Call SID

Provider-generated identifier for a Twilio call.

Stored for external reference but never replaces the internal Call ID.

---

## LiveKit Room

The media room created for an active voice session.

---

# AI Terms

## Large Language Model (LLM)

A language model used for reasoning, conversation, and generation.

Examples:

- GPT models
- Future supported models

---

## Prompt

Instructions supplied to the LLM.

Prompt templates should be versioned.

---

## Prompt Version

A versioned revision of a prompt.

Allows rollback and reproducibility.

---

## Tool

An executable capability available to an AI agent.

Examples:

- CRM lookup
- Calendar booking
- Weather lookup
- HTTP request

---

## Tool Call

A runtime invocation of a tool by an AI model.

---

## Skill

A reusable AI capability composed of prompts, tools, workflows, and configuration.

Examples:

- Appointment Booking
- Lead Qualification
- FAQ Assistant

---

## Agent Runtime

The execution environment responsible for orchestrating AI conversations.

---

## Context Window

The information available to the LLM for generating a response.

---

## Token

The basic unit processed by a language model.

Used for billing and context limits.

---

# LangGraph Terms

## Workflow

A directed sequence of execution steps.

---

## Node

A processing unit within a LangGraph workflow.

---

## Edge

A connection between workflow nodes.

---

## State

The shared data passed between workflow nodes.

---

## Checkpoint

A saved workflow state that allows execution to resume.

---

# Knowledge & RAG Terms

## Knowledge Base

A collection of documents available for retrieval.

---

## Document

A source file ingested into the platform.

Examples:

- PDF
- DOCX
- TXT
- HTML

---

## Chunk

A segment of a document used for embedding and retrieval.

---

## Embedding

A vector representation of content.

---

## Vector

The numerical representation stored in pgvector.

---

## Vector Search

Similarity search performed against stored embeddings.

---

## Metadata

Additional structured information associated with documents or vectors.

Examples:

- Source
- Author
- Language
- Tenant
- Tags

---

## Retrieval

The process of locating relevant knowledge before LLM inference.

---

## Reranking

Improving retrieval quality by reordering retrieved results.

---

# Memory Terms

## Short-Term Memory

Information retained during the current conversation.

---

## Long-Term Memory

Persistent information retained across conversations.

---

## Conversation Memory

Historical exchanges associated with a conversation.

---

## User Memory

Persistent preferences associated with a user.

---

## Memory Policy

Rules governing memory creation, retention, expiration, and deletion.

---

# Database Terms

## Entity

A business object represented by a database table.

---

## Record

A single row within a table.

---

## Primary Key

The unique identifier for an entity.

Standard:

UUIDv7

---

## Foreign Key

A relationship between entities.

---

## Soft Delete

Logical deletion using:

```
deleted_at
```

---

## Audit Fields

Standard fields:

- created_at
- updated_at
- deleted_at
- created_by
- updated_by

---

# API Terms

## Endpoint

A publicly accessible API route.

---

## DTO

Data Transfer Object used between client and server.

---

## Request ID

Identifier used to trace an individual request.

---

## Correlation ID

Identifier used to trace related requests across services.

---

## Idempotency Key

A client-provided identifier preventing duplicate operations.

---

# Infrastructure Terms

## Service

An independently deployable backend component.

---

## Worker

A background process executing asynchronous tasks.

---

## Queue

A mechanism for processing background jobs.

---

## Job

A unit of asynchronous work.

---

## Event

A significant occurrence published within the system.

---

## Webhook

An outbound HTTP callback triggered by an event.

---

# Security Terms

## Authentication

Verification of user identity.

---

## Authorization

Determination of allowed actions.

---

## RBAC

Role-Based Access Control.

---

## Secret

Sensitive configuration value.

Examples:

- API keys
- Tokens
- Passwords

---

## Encryption

Protection of data using cryptographic algorithms.

---

# Observability Terms

## Log

A structured record of runtime activity.

---

## Metric

A numerical measurement describing system behavior.

---

## Trace

A record of a request flowing through multiple services.

---

## Health Check

An endpoint reporting service health.

---

# Status Terms

## Draft

Work has started but is incomplete.

---

## In Review

Awaiting review.

---

## Approved

Accepted but not yet active.

---

## Active

Currently in use.

---

## Deprecated

Supported but scheduled for removal.

---

## Archived

Retained for historical reference only.

---

# Future Additions

This glossary will continue to expand as the platform evolves.

Future sections may include:

- Billing
- Marketplace
- Plugin System
- MCP Ecosystem
- AI Skills Library
- Compliance
- Multi-Region Deployment
- Analytics
- Voice Quality Metrics
- CRM Integrations

---

# Maintenance

When introducing a new business concept, API resource, database entity, or architectural component:

1. Add the term to this glossary.
2. Use the standardized name consistently across the project.
3. Update related documentation if terminology changes.

This glossary is the authoritative vocabulary for the Voice Agent SaaS Platform.
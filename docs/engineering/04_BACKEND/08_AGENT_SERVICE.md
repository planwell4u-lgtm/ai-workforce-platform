# Agent Service

**Module:** 04_BACKEND

**Document:** 08_AGENT_SERVICE

**Version:** 2.0

**Status:** Production Ready

---

# Purpose

The Agent Service is responsible for managing the complete lifecycle of AI voice agents within the Voice Agent SaaS Platform.

An Agent represents a configurable AI assistant capable of handling inbound and outbound voice conversations. The Agent Service manages agent configuration, prompts, voice settings, runtime behavior, tools, workflows, knowledge sources, memory integration, and deployment state.

It serves as the central management service for all AI agents.

---

# Responsibilities

The Agent Service manages:

- Agent creation
- Agent configuration
- Agent deployment
- Agent versioning
- Prompt management
- Voice assignment
- Workflow assignment
- Knowledge attachment
- Memory configuration
- Tool configuration
- Runtime settings
- Agent cloning
- Agent publishing
- Agent archiving

---

# Architecture

```
                    API

                     │

                     ▼

               Agent Service

     ┌──────────────┼──────────────┐

     ▼              ▼              ▼

 Repository     AI Runtime     Event Bus

     │

     ▼

 PostgreSQL
```

---

# Service Dependencies

The Agent Service depends on:

- Agent Repository
- Voice Service
- Workflow Service
- Knowledge Service
- RAG Service
- Memory Service
- Integration Service
- Event Publisher
- Redis Cache

---

# Database Tables

Primary

```
agents

agent_versions

agent_prompts

agent_tools

agent_runtime

agent_settings

agent_deployments
```

Related

```
voices

knowledge_bases

workflows

memory_profiles

rag_profiles

integrations
```

---

# Public Responsibilities

```
Create Agent

Update Agent

Delete Agent

Archive Agent

Clone Agent

Publish Agent

Deploy Agent

Disable Agent

Enable Agent

Assign Voice

Assign Workflow

Assign Knowledge

Assign Memory

Assign Tools

Update Prompt

Create Version

Rollback Version

List Agents

Get Agent
```

---

# Agent Lifecycle

```
Create Agent

↓

Create Default Configuration

↓

Assign Voice

↓

Assign Prompt

↓

Assign Workflow

↓

Attach Knowledge

↓

Configure Memory

↓

Validate Configuration

↓

Publish Event

↓

Ready
```

---

# Agent States

```
Draft

Configured

Testing

Published

Active

Paused

Archived

Deleted
```

Only **Active** agents may receive live calls.

---

# Agent Configuration

Each agent stores:

- Name
- Description
- Persona
- System Prompt
- Welcome Message
- Default Language
- Time Zone
- Voice Provider
- Voice Model
- AI Model
- Temperature
- Max Tokens
- Interrupt Policy
- Silence Timeout

---

# Voice Configuration

Each agent may have:

- Voice Provider
- Voice Model
- Voice Speed
- Voice Stability
- Voice Style
- Pronunciation Dictionary
- Fallback Voice

Voice configuration is managed through the Voice Service.

---

# Prompt Management

Prompt configuration includes:

```
System Prompt

Greeting Prompt

Conversation Rules

Fallback Prompt

Transfer Prompt

Closing Prompt
```

Prompt version history is maintained.

---

# Workflow Integration

Agents execute workflows defined in the Workflow Service.

Supported workflow types:

- Sales
- Customer Support
- Appointment Booking
- Reception
- Lead Qualification
- Medical Assistant
- FAQ Assistant
- Custom Workflows

---

# Knowledge Integration

Agents can attach multiple knowledge bases.

Knowledge sources include:

- Documents
- PDFs
- Websites
- FAQs
- Internal Notes
- Product Catalogs

Retrieval is handled through the RAG Service.

---

# Memory Integration

Each agent may use:

- Conversation Memory
- Long-Term Memory
- Customer Memory
- Session Memory
- Semantic Memory

Memory policies are configured through the Memory Service.

---

# Tool Integration

Agents can invoke external tools.

Examples

```
CRM Lookup

Calendar

Email

SMS

Webhook

ERP

Database Query

Custom API

MCP Tools
```

Tool execution is governed by runtime permissions.

---

# Runtime Configuration

Runtime options include:

- STT Provider
- LLM Provider
- TTS Provider
- VAD Settings
- Turn Detection
- Streaming Mode
- Context Window
- Retry Policy
- Timeout Settings

---

# Deployment

Deployment stages

```
Draft

↓

Validation

↓

Testing

↓

Published

↓

Production
```

Published versions are immutable.

---

# Versioning

Each published configuration creates a new version.

Version includes:

- Prompt
- Voice
- Workflow
- Knowledge
- Memory
- Runtime Settings
- Tool Configuration

Rollback to previous versions is supported.

---

# Events Published

```
AgentCreated

AgentUpdated

AgentDeleted

AgentPublished

AgentActivated

AgentPaused

AgentArchived

AgentVersionCreated

AgentVoiceChanged

AgentWorkflowChanged

AgentKnowledgeUpdated
```

---

# Events Consumed

```
VoiceUpdated

WorkflowUpdated

KnowledgeUpdated

MemoryUpdated

IntegrationUpdated

SubscriptionChanged
```

---

# Cache Strategy

Cached data

```
Agent Configuration

Runtime Settings

Prompt

Voice Settings

Permissions

Deployment Status
```

Cache is invalidated after configuration updates.

---

# Security Responsibilities

The Agent Service enforces:

- Tenant isolation
- Agent ownership
- Role-based permissions
- Runtime authorization
- Tool access validation
- Deployment authorization

---

# Error Handling

Domain exceptions

```
AgentNotFound

AgentAlreadyExists

AgentAlreadyPublished

InvalidConfiguration

InvalidWorkflow

VoiceNotFound

KnowledgeNotFound

DeploymentFailed

VersionNotFound
```

---

# Performance Guidelines

The service should:

- Cache active agent configurations
- Lazy-load large knowledge references
- Minimize joins
- Batch related queries
- Preload runtime configuration before call start

---

# Audit Logging

Audit events include:

- Agent creation
- Configuration changes
- Prompt updates
- Voice changes
- Workflow assignment
- Knowledge assignment
- Memory updates
- Deployment
- Version creation
- Rollback
- Deletion

---

# Testing Requirements

The Agent Service must include tests for:

- Agent lifecycle
- Configuration validation
- Deployment workflow
- Version management
- Knowledge attachment
- Memory configuration
- Voice assignment
- Workflow assignment
- Permission validation
- Tenant isolation
- Cache invalidation
- Event publishing

---

# Related Documents

- 09_VOICE_SERVICE.md
- 10_CALL_CONTROL_SERVICE.md
- 12_KNOWLEDGE_SERVICE.md
- 13_RAG_SERVICE.md
- 14_MEMORY_SERVICE.md
- 15_WORKFLOW_SERVICE.md
- 03_DATABASE/07_AGENT_SCHEMA.md
- 03_DATABASE/08_AGENT_RUNTIME_SCHEMA.md

---

# Summary

The Agent Service is the central orchestration service for AI agents within the Voice Agent SaaS Platform. It manages the complete lifecycle of an agent—from creation and configuration to deployment and versioning—while integrating voice, workflows, RAG, memory, tools, and runtime settings. By separating configuration from execution and supporting versioned deployments, the service provides a scalable, secure, and production-ready foundation for enterprise AI voice agents.
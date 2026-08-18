# Distributed Tracing Specification

**Module:** 13_OBSERVABILITY

**Document:** 06_DISTRIBUTED_TRACING

**Version:** 1.0

**Status:** Production Ready

---

# Purpose

This document defines the distributed tracing specification and architectural standards for the Voice Agent SaaS Platform.

Distributed tracing tracks the lifecycle of requests as they flow through distributed components, including backend APIs, databases, caches, AI runtimes, and voice processing pipelines.

It is the primary tool for identifying performance bottlenecks, analyzing latencies, debugging distributed systems, and visualizing service dependencies.

---

# Objectives

The distributed tracing architecture is designed to:

- Provide end-to-end visibility of requests
- Measure latency across service boundaries
- Identify performance bottlenecks
- Debug multi-service call paths
- Profile database and cache queries
- Monitor AI agent execution steps
- Correlate voice media pipelines with backend events
- Map real-time system dependencies
- Provide contextual data for errors
- Support tenant-level performance analysis

---

# Core Concepts

The tracing model follows the OpenTelemetry specification:

## Trace

A trace represents the complete path of a transaction or request through the system.

A trace is composed of a directed acyclic graph of Spans.

---

## Span

A span represents a single unit of work within a trace.

Spans contain:

- Name
- Start and end timestamps
- Status (Ok, Error)
- Attributes (key-value pairs)
- Events (structured log markers)
- Parent Span ID

---

## Context Propagation

Context propagation allows tracing context to cross service boundaries.

The platform standardizes on W3C Trace Context and W3C Baggage headers:

- `traceparent`: Standard trace headers (`version-traceid-spanid-traceflags`)
- `tracestate`: Vendor-specific routing info
- `baggage`: Metadata passed along the request path (e.g., `tenant_id`, `call_id`)

---

# Context Propagation Flow

```text
  [ Client Request ]
         │
         ▼
 ┌───────────────┐
 │  API Gateway  │  --> Initiates Trace ID (or propagates external)
 └───────┬───────┘
         │  Injects HTTP Headers (traceparent, baggage)
         ▼
 ┌───────────────┐
 │  Backend API  │  --> Extracts parent context, creates active span
 └───────┬───────┘
         │  Injects DB context / RPC metadata
         ├───┬───────────────────────────────┐
         ▼   ▼                               ▼
 ┌───────────┐┌──────────────┐       ┌───────────────┐
 │ Database  ││ Redis Cache  │       │  AI Runtime   │ (LangGraph / LLM)
 └───────────┘└──────────────┘       └───────┬───────┘
                                             │  Propagates via WebSockets/gRPC
                                             ▼
                                     ┌───────────────┐
                                     │ Voice Platform│ (STT/TTS, Media flow)
                                     └───────────────┘
```

---

# Metadata & Semantic Conventions

To ensure traces are searchable and indexable, all spans must follow standardized naming and attributes.

## Standard Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `service.name` | Name of the executing service | `voice-gateway` |
| `service.version` | Version of the service | `1.4.2` |
| `deployment.environment` | Target environment | `production` |
| `tenant.id` | Multi-tenant identifier | `tenant_9a3c8e` |
| `error.type` | Class name of exceptions | `LLMTimeoutError` |

---

## Platform-Specific Attributes

Every trace involving voice calls or agent execution must include the following attributes in its spans:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `call.id` | Unique ID of the active phone call | `call_728f91a` |
| `agent.id` | ID of the AI agent configuration | `agent_xyz_99` |
| `session.id` | Unique LiveKit or WebRTC session ID | `room_88df0a` |
| `conversation.id` | High-level logical conversation ID | `conv_bc8d11` |

---

# Service-Specific Tracing Strategies

## Backend & API Gateway

FastAPI and Gateway services use OpenTelemetry middleware to automatically trace HTTP requests.

- Every incoming HTTP request starts a root span (if no parent header is present)
- Active context is stored in local thread/asyncio context
- Outgoing HTTP client calls (e.g. using `httpx`) inject headers automatically

---

## AI Runtime (LangGraph & LLMs)

AI runtime execution requires specialized tracing to monitor multi-step agent decisions.

- **Graph Tracing**: Every node execution in LangGraph must be represented by a child span
- **LLM Calls**: Calls to LLMs must capture prompt token counts, completion token counts, and LLM provider latency
- **Tool Calls**: Individual tool invocations must be wrapped in separate spans containing the tool name and status

---

## Voice Platform

The Voice Platform traces low-latency media streams, STT, and TTS processing.

- **Call Setup**: Tracing starts from SIP INVITE or WebRTC connection request
- **STT Spans**: Spans record start/end of speech, transcription text latency, and audio length
- **TTS Spans**: Spans record text length, synthesis duration, time-to-first-byte (TTFB), and playback status
- **Media Worker**: Worker scheduling delay is tracked using spans containing queue wait times

---

## Database & Cache Tracing

Database queries and cache accesses are traced to identify slow operations.

- **PostgreSQL**: SQLAlchemy automatically generates spans for every query execution, including database statements (SQL sanitized to remove parameters)
- **Redis**: Redis client calls trace commands (e.g., `GET`, `SET`, `HGETALL`) along with cache hit/miss status

---

# Sampling Policy

Because tracing high-volume voice streams and LLM calls generates significant telemetry, production environments employ a multi-stage sampling strategy:

- **Head-Based Sampling**: API Gateway sample rate set to `20%` for standard successful requests
- **Tail-Based Sampling**: The OpenTelemetry Collector analyzes complete traces before exporting:
  - Error traces: `100%` sampled
  - Latency > 1.5 seconds: `100%` sampled
  - Chat/Voice session initiations: `100%` sampled
  - Standard healthy transactions: `10%` sampled

---

# Performance & Security Considerations

To ensure tracing does not impact voice quality or expose sensitive data:

- **Asynchronous Exporting**: Spans are buffered in memory and exported out-of-band using non-blocking background workers
- **Data Scrubbing**: Tracing middleware must scrub credit card numbers, passwords, API keys, and transcript text containing PII before exporting
- **Trace Context Propagation Limits**: Baggage size is restricted to `1KB` to avoid overhead in packet sizes

---

# Exporters & Storage

The tracing pipeline uses OTLP to transport data:

1. Services export spans to the **OpenTelemetry Collector**
2. Collector batches, compresses, and filters spans
3. Collector exports traces to **Grafana Tempo**
4. Traces are queried and visualized inside **Grafana**

---

# Related Documents

- 01_OBSERVABILITY_ARCHITECTURE.md
- 02_LOGGING_ARCHITECTURE.md
- 05_OPENTELEMETRY_STRATEGY.md
- 13_DATABASE_OBSERVABILITY.md
- 15_AI_RUNTIME_OBSERVABILITY.md
- 16_VOICE_PLATFORM_OBSERVABILITY.md

---

# Summary

Distributed tracing is the cornerstone of observability in a modern, event-driven AI voice platform. By implementing unified context propagation, semantic tagging, and tail-based sampling, the platform ensures complete, secure, and low-overhead visibility into the execution paths of voice calls and agent workflows.

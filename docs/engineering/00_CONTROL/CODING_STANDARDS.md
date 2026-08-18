# CODING_STANDARDS

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document defines the coding standards, engineering practices, and development conventions used throughout the Voice Agent SaaS Platform.

Its goals are to ensure:

- Consistent code quality
- High maintainability
- Production readiness
- Secure development
- Scalable architecture
- Predictable project structure

These standards apply to all contributors, including AI-generated code.

---

# Engineering Philosophy

Our engineering philosophy is based on the following principles:

1. Readability over cleverness.
2. Simplicity over unnecessary complexity.
3. Explicit behavior over implicit behavior.
4. Maintainability over short-term convenience.
5. Security by default.
6. Testability by design.
7. Documentation as part of development.
8. Production-first implementation.

---

# General Principles

## Keep Functions Small

Functions should perform a single responsibility.

Avoid "God" functions.

Prefer:

- 20–40 lines

Maximum:

- 100 lines

---

## Single Responsibility Principle

Each:

- class
- function
- module

should have one clear responsibility.

---

## Avoid Duplicate Code

Prefer reusable components.

Extract common logic into:

- services
- utilities
- shared libraries

---

## Explicit is Better

Avoid hidden behavior.

Prefer:

```python
create_customer(customer_data)
```

instead of

```python
process(customer_data)
```

---

## Defensive Programming

Validate:

- input
- configuration
- API payloads
- database results
- external services

Never assume external systems behave correctly.

---

# Project Structure

Repository layout:

```
docs/
backend/
frontend/
infrastructure/
scripts/
tests/
docker/
.github/
```

Each directory should have a clear purpose.

---

# Backend Structure

```
backend/

app/

api/

core/

config/

models/

schemas/

services/

repositories/

workflows/

agents/

rag/

memory/

integrations/

tasks/

middleware/

dependencies/

events/

telemetry/

security/

utils/

tests/
```

Responsibilities should remain separated.

---

# Frontend Structure

```
frontend/

app/

components/

features/

hooks/

lib/

services/

types/

styles/

public/

tests/
```

Avoid placing business logic inside UI components.

---

# Naming Conventions

## Variables

Use descriptive names.

Good

```python
customer_id
conversation_state
embedding_vector
```

Avoid

```python
x
tmp
obj
```

---

## Functions

Use verbs.

Examples

```
create_agent()

load_prompt()

generate_embedding()

transcribe_audio()

search_documents()
```

---

## Classes

Use PascalCase.

```
VoiceAgent

ConversationManager

KnowledgeRetriever

PromptBuilder
```

---

## Files

Use snake_case.

```
conversation_service.py

agent_runtime.py

voice_pipeline.py
```

---

## Constants

Use UPPER_SNAKE_CASE.

```
MAX_RETRIES

DEFAULT_TIMEOUT

API_VERSION
```

---

# Python Standards

Python version should match the project's supported version.

Use:

- type hints
- dataclasses where appropriate
- Pydantic models for validation

Avoid dynamic typing unless required.

---

## Imports

Preferred order

1 Standard library

2 Third-party

3 Internal modules

Example

```python
import uuid
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.models.agent import Agent
from app.services.agent_service import AgentService
```

---

## Type Hints

Always use type hints.

Good

```python
def get_agent(agent_id: UUID) -> Agent:
```

Avoid

```python
def get_agent(id):
```

---

## Docstrings

Public functions should include concise docstrings.

Example

```python
def create_call() -> Call:
    """
    Creates a new voice call record.

    Returns:
        Newly created Call object.
    """
```

---

# TypeScript Standards

Enable:

```
strict
```

Avoid

```
any
```

Prefer

```
unknown

Record

interfaces

type aliases
```

---

# React Standards

Prefer functional components.

Use hooks.

Avoid class components.

Keep presentation separate from business logic.

---

# Next.js Standards

Use App Router.

Use Server Components by default.

Use Client Components only when necessary.

Use Server Actions only where appropriate.

---

# API Design

REST endpoints

```
GET

POST

PUT

PATCH

DELETE
```

Follow resource-oriented naming.

Good

```
/agents

/calls

/prompts

/knowledge-bases
```

Avoid

```
/createAgent

/getCalls

/doSomething
```

---

# API Versioning

All public APIs must be versioned.

```
/api/v1/
```

Never introduce breaking changes without a new API version.

---

# Error Handling

Never suppress exceptions silently.

Bad

```python
try:
    ...
except:
    pass
```

Good

```python
try:
    ...
except ValidationError as ex:
    logger.exception(ex)
    raise
```

---

# Logging

Use structured JSON logs.

Never use print() for production code.

Every log should contain:

- request_id
- correlation_id
- tenant_id
- service
- severity
- timestamp

---

# Security Basics

Never:

- hardcode secrets
- commit credentials
- expose stack traces
- trust client input

Always validate user input.

---

# Documentation

Every significant module should include documentation.

Architecture changes require documentation updates.

Complex algorithms should be explained.

---

# AI Generated Code

AI-generated code is considered a first draft.

It must be:

- reviewed
- tested
- documented
- validated

before merging.

---

# Compliance

All contributors are expected to follow these standards.

Exceptions require documented justification or an approved ADR.
# AI Development Guide

**Version:** 1.0

**Status:** Active

**Phase:** Foundation

---

# Purpose

This document defines the operating guidelines for AI assistants working on the Voice Agent SaaS Platform.

The purpose is to ensure that AI-generated:

* Architecture
* Documentation
* Code
* Configuration
* Tests
* Refactoring

remain consistent with the project's long-term vision.

This document acts as the instruction layer for AI-assisted development.

---

# AI Assistant Role

The AI assistant should behave as:

* Architecture-aware engineer
* Documentation guardian
* Code quality reviewer
* Implementation assistant

The AI assistant must not behave as:

* Independent architect without context
* Uncontrolled code generator
* Replacement for engineering decisions

---

# Required Reading Order

Before making changes, the AI assistant should read:

```text
00_CONTROL/

    PROJECT_CONTEXT.md

    ARCHITECTURE_PRINCIPLES.md

    AI_DEVELOPMENT_GUIDE.md

    ROADMAP.md

    DECISION_LOG.md

    CURRENT_STATUS.md
```

After understanding project context, read the relevant platform documentation.

---

# Development Workflow

All AI-assisted work should follow:

```text
Understand

    ↓

Analyze Existing Architecture

    ↓

Check Existing Decisions

    ↓

Design Solution

    ↓

Document Changes

    ↓

Implement

    ↓

Test

    ↓

Review
```

---

# Before Creating New Files

The AI assistant must verify:

1. Does this file already exist?
2. Does another module already own this responsibility?
3. Will this create duplication?
4. Does this belong in the selected platform?
5. Is the naming consistent?

Do not create files only because a concept sounds useful.

---

# Architecture Boundary Rules

The AI assistant must respect platform ownership.

Example:

## Agent Platform owns:

* Agent identity
* Capabilities
* Reasoning orchestration
* Tools
* Agent lifecycle

## Conversation Platform owns:

* Conversation state
* Conversation lifecycle
* Routing
* Context handling

## Voice Platform owns:

* Audio
* Telephony
* SIP
* Media transport

## Knowledge Platform owns:

* Documents
* Retrieval
* RAG
* Knowledge lifecycle

## Memory Platform owns:

* Historical context
* User memories
* Memory lifecycle

---

# Documentation Rules

Architecture documents should:

* Explain purpose
* Define boundaries
* Describe responsibilities
* Avoid unnecessary implementation details
* Avoid duplicating other documents

Good:

```text
The Knowledge Platform provides controlled retrieval of organizational information.
```

Bad:

```text
Create this exact database table with these columns.
```

Database implementation belongs elsewhere.

---

# Code Generation Rules

When generating code:

Follow:

* Existing project structure
* Existing naming conventions
* Existing technology choices
* Existing patterns

Do not introduce:

* New frameworks
* New dependencies
* New architecture patterns

without approval.

---

# Change Management

Before modifying existing architecture:

The AI assistant should identify:

* Affected modules
* Existing dependencies
* Possible conflicts
* Required documentation updates

Major changes require an ADR.

---

# Avoiding Duplication

Before adding functionality:

Search existing modules for similar concepts.

Examples:

Do not create:

```text
Agent Memory
Customer History
Conversation Memory
```

as separate systems.

Determine ownership first.

---

# Version Management

When modifying documents:

Version rules:

Minor updates:

```text
1.0 → 1.1
```

Use for:

* Clarifications
* Additional details
* Corrections

Major architectural changes:

```text
1.0 → 2.0
```

Use for:

* New architecture direction
* Changed responsibility
* Breaking changes

---

# Testing Expectations

AI-generated code should include appropriate validation.

Consider:

* Unit tests
* Integration tests
* Security tests
* Failure scenarios
* Edge cases

Testing should be designed with the feature.

---

# Security Expectations

AI assistants must always consider:

* Authentication
* Authorization
* Tenant isolation
* Input validation
* Secret management
* Data protection

Never generate insecure shortcuts.

---

# Production Readiness Checklist

Before considering work complete:

Architecture:

* [ ] Responsibility is clear
* [ ] No module overlap
* [ ] Documentation updated

Code:

* [ ] Follows project standards
* [ ] Tested
* [ ] Handles failures

Operations:

* [ ] Logging considered
* [ ] Monitoring considered
* [ ] Deployment impact reviewed

Security:

* [ ] Access controls reviewed
* [ ] Sensitive data protected

---

# AI Decision Rules

When uncertain:

Priority order:

1. Existing architecture documents
2. Existing ADR decisions
3. Existing code patterns
4. Industry best practices
5. Ask for clarification

Do not invent missing decisions.

---

# Repository Discipline

AI assistants should:

* Keep changes focused
* Avoid unnecessary refactoring
* Explain architectural impact
* Maintain documentation consistency

---

# Summary

This guide establishes how AI assistants should contribute to the Voice Agent SaaS Platform.

The goal is not only to generate code quickly, but to preserve:

* Architecture integrity
* Documentation quality
* Long-term maintainability
* Engineering consistency

AI assistance should accelerate development while protecting the project's design principles.

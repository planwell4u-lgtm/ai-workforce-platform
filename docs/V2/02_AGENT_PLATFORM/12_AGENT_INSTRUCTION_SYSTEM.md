# 12_AGENT_INSTRUCTION_SYSTEM

**Title:** Agent Instruction System

**Version:** 2.1

**Status:** Approved

---

# Overview

The Agent Instruction System defines how AI Employees receive, organize, evaluate, prioritize, validate, and apply instructions during execution.

Instructions represent the rules, constraints, objectives, and policies that guide agent behavior.

The relationship is:

```
Instructions

↓

Agent Context

↓

Execution Engine

↓

Agent Action
```

The Agent Platform manages instruction processing.

---

# Purpose

This document defines:

- Instruction concepts.
- Instruction architecture.
- Instruction hierarchy.
- Instruction sources.
- Instruction scope.
- Instruction evaluation.
- Instruction resolution.
- Instruction templates.
- Instruction parameters.
- Instruction lifecycle.
- Instruction testing.
- Instruction security.

This document does not define:

- Agent personality.
- Communication style.
- Memory.
- Context assembly.
- Tool implementation.
- Model architecture.

Those belong to:

```
13_AGENT_PERSONA_AND_BEHAVIOR_MODEL.md

11_AGENT_CONTEXT_MODEL.md

06_MEMORY_PLATFORM

15_AGENT_TOOL_SYSTEM.md
```

---

# Core Principle

Agents require controlled behavioral guidance.

Agent behavior is created through layered instructions.

```
Agent Intelligence

=

Instructions

+

Context

+

Reasoning

+

Tools

+

State
```

---

# Instruction Definition

An instruction is:

```
A rule, constraint, objective, or policy that influences agent execution.
```

Examples:

```
Always verify customer identity.

Never expose private information.

Follow company refund policy.
```

---

# Instruction Ownership Boundary

## Agent Platform Owns

- Instruction processing.
- Instruction ordering.
- Instruction evaluation.
- Instruction conflict resolution.
- Instruction delivery.
- Instruction lifecycle.

---

## External Platforms Own

| Instruction Type | Owner |
|---|---|
| Platform Rules | Agent Platform |
| Tenant Policies | Tenant Configuration |
| Business Knowledge Rules | Knowledge Platform |
| Security Enforcement Rules | Security Platform |
| Tool Usage Rules | Tool System |
| User Preferences | Memory Platform |

---

# Instruction Architecture

```
Platform Instructions

        ↓

Tenant Instructions

        ↓

Agent Instructions

        ↓

Task Instructions

        ↓

Runtime Instructions

        ↓

Execution Rules
```

---

# Instruction Scope Model

Instructions operate within defined scopes.

```
Instruction Scope

├── Platform Scope

├── Tenant Scope

├── Agent Scope

├── Session Scope

└── Task Scope
```

---

## Platform Scope

Global rules.

Examples:

```
Security requirements

Platform limitations
```

---

## Tenant Scope

Customer-specific policies.

Examples:

```
Company refund policy

Brand requirements
```

---

## Agent Scope

Agent-specific behavior.

Examples:

```
Support agent rules

Sales agent rules
```

---

## Session Scope

Temporary interaction rules.

Example:

```
Handle this customer request with priority.
```

---

## Task Scope

Single objective instructions.

Example:

```
Schedule customer appointment.
```

---

# Instruction Layers

## Platform Instructions

Highest authority rules.

Examples:

- Security requirements.
- Platform limitations.
- Compliance rules.

---

## Tenant Instructions

Customer-defined policies.

Examples:

- Business processes.
- Company policies.
- Brand requirements.

---

## Agent Instructions

Agent-specific rules.

Examples:

- Support workflow.
- Sales approach.

---

## Task Instructions

Current objective rules.

Example:

```
Resolve billing issue.
```

---

## Runtime Instructions

Temporary execution guidance.

Example:

```
Retry external service call.
```

---

# Instruction Priority Model

Priority order:

```
1. Security Instructions

2. Platform Instructions

3. Tenant Instructions

4. Agent Instructions

5. Task Instructions

6. Runtime Instructions

7. Preferences
```

Higher priority instructions override lower priority instructions.

---

# Instruction Override Rules

Allowed:

```
Higher authority

↓

Overrides lower authority
```

Example:

```
Platform Security Rule

overrides

Tenant Preference
```

Not allowed:

```
User Input

↓

Override Security Rule
```

---

# Instruction Template System

Instructions can be created from reusable templates.

```
Instruction Templates

├── Base Template

├── Agent Template

├── Tenant Template

├── Task Template

└── Runtime Template
```

Example:

```
Customer Support Template

+

Company Rules

+

Agent Customization

=

Final Instruction Set
```

---

# Instruction Parameterization

Instructions may contain dynamic values.

Example:

Static:

```
Always answer during business hours.
```

Parameterized:

```
Business hours are:
{{tenant.business_hours}}
```

Parameters may come from:

```
Instruction Parameters

├── Tenant Values

├── Runtime Values

├── Environment Values

└── Agent Values
```

---

# Instruction Registry

The registry manages available instructions.

```
Instruction Registry

├── Instruction ID

├── Type

├── Scope

├── Owner

├── Priority

├── Version

├── Status

└── Metadata
```

---

# Instruction Loading

Instructions may load:

- Agent startup.
- Task creation.
- Runtime events.

Flow:

```
Execution Request

↓

Instruction Loader

↓

Instruction Resolver

↓

Agent Context

↓

Execution Engine
```

---

# Instruction Evaluation Model

Before applying instructions:

```
Instruction

↓

Applicable?

↓

Priority Check

↓

Conflict Check

↓

Validation

↓

Apply
```

Evaluation considers:

- Scope.
- Authority.
- Agent capability.
- Current task.
- Runtime conditions.

---

# Instruction Resolution

When instructions conflict:

Example:

```
Tenant:

Refunds require approval.


Runtime:

Approve refund automatically.
```

Resolution:

```
Tenant Policy Wins
```

Resolution considers:

- Authority.
- Priority.
- Scope.
- Version.
- Validity.

---

# Instruction Context

Instructions become part of execution context.

Flow:

```
Instruction Sources

↓

Instruction Resolver

↓

Validated Instructions

↓

Agent Context

↓

Execution Engine
```

---

# Dynamic Instructions

Some instructions change during execution.

Example:

```
Normal Operation

↓

Security Event

↓

Restricted Operation Mode
```

Dynamic instructions require:

- Authorization.
- Validation.
- Audit logging.

---

# Instruction Versioning

Instructions evolve over time.

Example:

Version 1:

```
Refunds require approval.
```

Version 2:

```
Refunds below $50 are automatic.
```

Versioning provides:

- Change tracking.
- Rollback.
- Auditability.
- Reproducibility.

---

# Instruction Lifecycle

```
Draft

↓

Review

↓

Testing

↓

Approved

↓

Active

↓

Updated

↓

Deprecated

↓

Archived
```

---

# Instruction Deployment Lifecycle

Production changes follow:

```
Create

↓

Review

↓

Validate

↓

Test

↓

Deploy

↓

Monitor

↓

Rollback If Required
```

---

# Instruction Testing Strategy

Instructions require validation before production.

```
Instruction Testing

├── Conflict Testing

├── Regression Testing

├── Safety Testing

├── Compliance Testing

└── Behavior Testing
```

Example:

```
New Instruction

↓

Run Evaluation Tests

↓

Approve Deployment
```

---

# Instruction Validation

Before activation:

```
Instruction Validation

├── Authority Check

├── Syntax Validation

├── Conflict Detection

├── Security Review

└── Version Check
```

---

# Instruction Security

Instructions must protect against:

- Unauthorized changes.
- Instruction injection.
- Privilege escalation.
- Policy conflicts.

---

# Instruction Injection Protection

External input cannot override trusted instructions.

Flow:

```
External Input

↓

Context Processing

↓

Instruction Boundary Check

↓

Execution
```

Example:

User:

```
Ignore all security rules.
```

Result:

```
Rejected
```

---

# Instruction Audit

Changes must be recorded.

```
Instruction Audit

├── Change ID

├── Instruction ID

├── Previous Version

├── New Version

├── Changed By

├── Timestamp

└── Reason
```

---

# Multi-Agent Instructions

Different agents may have different instruction sets.

Example:

```
Sales Agent

↓

Sales Instructions


Support Agent

↓

Support Instructions
```

Shared instructions require:

- Explicit permission.
- Ownership rules.
- Compatibility checks.

---

# Instruction Failure Handling

Possible failures:

- Missing instructions.
- Invalid instructions.
- Conflicting instructions.
- Unauthorized changes.

Handling:

```
Failure

↓

Validate

↓

Resolve

or

Block Execution
```

---

# Instruction vs Context

Instructions:

```
Rules controlling behavior
```

Context:

```
Information used during reasoning
```

Example:

Instruction:

```
Never reveal private data.
```

Context:

```
Customer account information.
```

---

# Instruction vs Persona

Instructions:

```
What the agent must do.
```

Persona:

```
How the agent communicates.
```

Example:

Instruction:

```
Verify customer identity.
```

Persona:

```
Friendly professional tone.
```

---

# Instruction vs Configuration

Configuration:

```
Settings
```

Examples:

```
Model selection

Language

Enabled features
```

Instructions:

```
Rules
```

Examples:

```
Never provide unauthorized refunds.
```

---

# Instruction vs Security Platform

Security Platform:

```
Global protection enforcement.
```

Instruction System:

```
Agent behavioral guidance.
```

Example:

Security:

```
Never expose credentials.
```

Instruction:

```
Ask verification questions before account changes.
```

---

# Observability Requirements

Instruction operations should expose:

- Loaded instructions.
- Applied priority.
- Conflicts.
- Versions used.
- Validation results.
- Deployment history.

Owned by:

```
13_OBSERVABILITY_PLATFORM
```

---

# Architectural Principles

## Instructions Are Layered

Multiple instruction sources combine.

---

## Higher Authority Wins

Priority controls conflicts.

---

## Instructions Are Versioned

Changes are traceable.

---

## Instructions Are Secure

Unauthorized rules cannot influence execution.

---

## Instructions Are Observable

Instruction decisions can be explained.

---

# Architectural Invariants

1. Instructions control agent behavior.
2. Instructions are separate from context.
3. Instructions are separate from memory.
4. Instructions follow hierarchy.
5. Higher authority overrides lower authority.
6. Instructions are versioned.
7. Instructions require validation.
8. External input cannot override trusted instructions.
9. Instruction changes are auditable.
10. Instruction deployment is controlled.
11. Instruction decisions are observable.
12. Instruction ownership remains defined.

---

# Relationship To Other Documents

| Document | Relationship |
|---|---|
| 05_AGENT_IDENTITY_MODEL.md | Agent identity |
| 06_AGENT_CONFIGURATION_MODEL.md | Agent settings |
| 07_AGENT_RUNTIME_ARCHITECTURE.md | Runtime usage |
| 08_AGENT_EXECUTION_ENGINE.md | Execution control |
| 10_AGENT_STATE_MANAGEMENT.md | Runtime state |
| 11_AGENT_CONTEXT_MODEL.md | Context integration |
| 13_AGENT_PERSONA_AND_BEHAVIOR_MODEL.md | Communication behavior |
| 14_AGENT_CAPABILITY_MODEL.md | Agent abilities |
| 15_AGENT_TOOL_SYSTEM.md | Tool rules |
| 11_SECURITY_PLATFORM | Security policies |

---

# Revision History

| Version | Date | Changes |
|---|---|---|
| 2.0 | 2026-08-04 | Initial Agent Instruction System document. |
| 2.1 | 2026-08-04 | Added templates, parameters, scopes, evaluation, override rules, testing, deployment lifecycle, and boundary clarifications. |
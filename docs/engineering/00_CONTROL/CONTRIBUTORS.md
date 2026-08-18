# CONTRIBUTORS

**Project:** Voice Agent SaaS Platform

**Version:** 2.0

**Status:** Active

**Last Updated:** 2026-07-24

---

# Purpose

This document defines contribution guidelines for the Voice Agent SaaS Platform.

The purpose is to ensure that all contributors:

- Follow project architecture decisions
- Maintain documentation quality
- Preserve code standards
- Protect system security
- Make predictable changes

Contributors include:

- Software developers
- AI assistants
- DevOps engineers
- Database engineers
- Documentation contributors
- External collaborators

---

# Core Contribution Principles

All contributors must follow these principles:

## 1. Understand Before Changing

Before modifying existing systems:

- Review relevant documentation
- Review related ADRs
- Understand current architecture
- Identify dependencies

Do not introduce changes without understanding existing decisions.

---

## 2. Documentation Is Part of Development

A feature is incomplete until:

- Code exists
- Tests exist
- Documentation exists
- Project state is updated

---

## 3. Preserve Architectural Decisions

Existing architectural decisions should not be replaced casually.

If a better approach is identified:

1. Explain the problem.
2. Analyze alternatives.
3. Document tradeoffs.
4. Create an ADR if required.

---

# Required Reading Before Contribution

Every contributor should review:

```
docs/00_CONTROL/

AI_CONTEXT.md

PROJECT_MASTER_ROADMAP.md

PROJECT_STATE.md

PROJECT_DECISIONS.md

CODING_STANDARDS.md
```

Additional reading depends on the area being changed.

---

# Development Workflow

## Step 1 — Understand the Task

Before implementation:

- Identify requirements
- Review affected components
- Check existing issues
- Review architecture

---

## Step 2 — Plan the Change

Determine:

- Files affected
- Database changes
- API changes
- Documentation impact
- Security impact

---

## Step 3 — Implement

Follow:

- Coding standards
- Architecture patterns
- Security guidelines
- Testing requirements

---

## Step 4 — Validate

Before submitting:

Run:

- Tests
- Linters
- Type checks
- Security checks

---

## Step 5 — Update Documentation

Update where applicable:

- Architecture documents
- ADRs
- API documentation
- Database documentation
- Project state
- Session log

---

# Git Workflow

## Branch Naming

Recommended format:

```
feature/<name>

bugfix/<name>

hotfix/<name>

docs/<name>

refactor/<name>
```

Examples:

```
feature/agent-builder

feature/livekit-integration

docs/database-schema
```

---

# Commit Standards

Commits should be clear and descriptive.

Preferred format:

```
type: description
```

Examples:

```
feat: add agent configuration API

fix: resolve call timeout handling

docs: update voice architecture

refactor: improve workflow execution
```

---

# Pull Request Guidelines

Every pull request should include:

## Summary

Explain:

- What changed
- Why it changed

---

## Testing

Include:

- Tests performed
- Validation results

---

## Documentation

Identify:

- Documents updated
- ADRs created or modified

---

## Risks

Mention:

- Breaking changes
- Migration requirements
- Deployment concerns

---

# Code Review Expectations

Reviewers should evaluate:

## Correctness

Does it solve the intended problem?

---

## Architecture

Does it follow existing design?

---

## Security

Does it introduce vulnerabilities?

---

## Performance

Will it scale appropriately?

---

## Maintainability

Can future developers understand it?

---

## Testing

Are important cases covered?

---

# AI-Assisted Development Guidelines

AI assistants are allowed and encouraged.

However:

AI-generated code must be:

- Reviewed
- Tested
- Validated
- Documented

AI should not:

- Replace architectural decisions
- Introduce dependencies without review
- Ignore project standards

---

# Database Changes

Database changes require:

- Migration files
- Schema documentation update
- Backward compatibility review

Never manually modify production schemas.

---

# API Changes

API changes require:

- API documentation update
- Versioning review
- Compatibility analysis

Breaking changes require approval.

---

# Security Requirements

Never commit:

- Secrets
- Passwords
- API keys
- Private certificates

Always consider:

- Authentication
- Authorization
- Tenant isolation
- Data protection

---

# Testing Expectations

New functionality should include:

## Unit Tests

For:

- Business logic
- Services
- Utilities

---

## Integration Tests

For:

- APIs
- Database operations
- External integrations

---

## End-to-End Tests

For:

- Critical user workflows

---

# Documentation Contribution Rules

Documentation should be:

- Clear
- Accurate
- Structured
- Cross-referenced

Use existing templates.

Avoid duplicate documentation.

---

# AI Agent Contributors

AI assistants working on this project must:

1. Read project control documents.
2. Preserve existing decisions.
3. Explain tradeoffs.
4. Avoid unnecessary complexity.
5. Update documentation after major changes.
6. Record session progress.

---

# Ownership

Each contributor owns the quality of the changes they introduce.

The contributor is responsible for:

- Implementation quality
- Documentation accuracy
- Testing coverage
- Security considerations

---

# Contribution Checklist

Before completing work:

```
[ ] Reviewed relevant documentation

[ ] Followed architecture decisions

[ ] Followed coding standards

[ ] Added tests

[ ] Updated documentation

[ ] Checked security impact

[ ] Updated project state if required

[ ] Updated session log if required
```

---

# Final Principle

Every contribution should improve the platform without reducing its:

- Security
- Maintainability
- Scalability
- Reliability
- Documentation quality

The goal is not only to build features, but to build a sustainable production-grade platform.
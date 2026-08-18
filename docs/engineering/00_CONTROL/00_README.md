# 00_CONTROL

**Version:** 2.0

**Status:** Active

**Phase:** Foundation

---

# Purpose

The **00_CONTROL** directory contains the project control documents that serve as the operational foundation for the Voice Agent SaaS Platform.

These documents provide continuity, governance, project state, engineering standards, and decision history for both human developers and AI assistants.

Unlike implementation documents, the files in this directory describe **how the project is managed**, **how decisions are made**, and **how development should proceed**.

This directory should always remain up to date.

---

# Repository Control Layer

The repository is the single source of truth.

Every development session should begin by reviewing the control documents before making architectural or implementation changes.

The recommended reading order is:

1. AI_CONTEXT.md
2. PROJECT_MASTER_ROADMAP.md
3. PROJECT_STATE.md
4. SESSION_LOG.md
5. PROJECT_DECISIONS.md
6. CODING_STANDARDS.md
7. IMPLEMENTATION_PROGRESS.md
8. Relevant ADRs
9. Relevant architecture documents

---

# Control Documents

## AI_CONTEXT.md

Defines the operating instructions for AI assistants.

Contains:

- Project overview
- Architecture principles
- Technology stack
- AI responsibilities
- Development workflow
- Documentation update requirements

---

## PROJECT_MASTER_ROADMAP.md

Defines the complete project roadmap.

Contains:

- Long-term vision
- Development phases
- Milestones
- Deliverables
- Dependencies

---

## PROJECT_STATE.md

Represents the current state of the project.

Updated after major work.

Contains:

- Current phase
- Current objective
- Active tasks
- Completed work
- Upcoming work
- Blockers

---

## SESSION_LOG.md

Chronological development journal.

Each working session should append an entry.

Contains:

- Session date
- Work completed
- Decisions made
- Files created
- Next actions

---

## PROJECT_DECISIONS.md

Stores project-wide engineering decisions that do not require an ADR.

Examples:

- Naming conventions
- UUID strategy
- Time zone policy
- Logging rules
- API conventions

---

## CODING_STANDARDS.md

Defines engineering standards.

Includes:

- Naming conventions
- Folder structure
- Error handling
- Logging
- Testing
- API guidelines
- Database conventions

---

## DOCUMENTATION_INDEX.md

Master index of all documentation.

Provides navigation across the repository.

---

## IMPLEMENTATION_PROGRESS.md

Tracks implementation status for every major subsystem.

Examples:

- Foundation
- Authentication
- Voice Platform
- AI Runtime
- RAG
- Memory
- Billing
- Monitoring

---

## PROJECT_GLOSSARY.md

Defines standard terminology used throughout the project.

Prevents inconsistent naming.

---

## TECH_DEBT.md

Tracks technical debt.

Each item should include:

- Description
- Impact
- Priority
- Planned resolution
- Status

---

## KNOWN_LIMITATIONS.md

Documents known platform limitations.

Examples:

- Vendor constraints
- Temporary workarounds
- Third-party limitations
- Performance assumptions

---

## RISKS.md

Documents project risks.

Categories include:

- Technical
- Security
- Operational
- Financial
- Vendor
- Scalability

Each risk should include mitigation strategies.

---

## AI_PROMPTS.md

Reusable prompts for AI-assisted development.

Examples:

- Architecture review
- Security review
- Database review
- API review
- Documentation generation
- Test generation

---

## CHANGELOG.md

Records significant changes between releases.

Should follow semantic versioning principles.

---

## CONTRIBUTORS.md

Defines contribution guidelines.

Includes:

- Roles
- Responsibilities
- Review process
- Documentation expectations

---

## VERSION.md

Tracks repository version information.

Contains:

- Documentation version
- Blueprint version
- Implementation version
- Release history

---

# Update Policy

The following documents should be updated after major work:

Mandatory:

- PROJECT_STATE.md
- SESSION_LOG.md

When applicable:

- IMPLEMENTATION_PROGRESS.md
- CHANGELOG.md
- PROJECT_DECISIONS.md
- TECH_DEBT.md
- RISKS.md

---

# Development Workflow

Every development session should follow this sequence:

1. Review project control documents.
2. Review relevant ADRs.
3. Review relevant architecture documentation.
4. Implement changes.
5. Update documentation.
6. Record project state.
7. Record session history.

---

# Source of Truth

The repository—not chat history or AI memory—is the authoritative source of project knowledge.

All architectural decisions, implementation progress, and engineering standards must be documented within the repository to ensure continuity across developers, AI assistants, and future project phases.

---

# Document Ownership

This document is maintained as part of the Version 2 Production Blueprint.

All contributors are responsible for keeping the control layer accurate, current, and synchronized with the project's evolution.
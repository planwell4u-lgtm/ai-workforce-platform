# AI Context

## Project

Voice Agent SaaS Platform


## Purpose

This document provides context and operating guidelines for any AI assistant working on this project.

The AI assistant should use this document together with:

- PROJECT_MASTER_ROADMAP.md
- PROJECT_STATE.md
- SESSION_LOG.md


---

# AI Role

The AI assistant acts as:

- Senior Software Architect
- Backend Engineer
- AI Systems Engineer
- Database Architect
- DevOps Engineer
- Documentation Engineer


---

# Project Objective

Build a production-grade, multi-tenant AI Voice Agent SaaS platform.

The platform enables businesses to create and deploy AI-powered voice agents for:

- Customer service
- Sales
- Reception
- Appointment booking
- Business automation


---

# Architecture Principles

## 1. Documentation First

Architecture decisions must be documented before major implementation.


## 2. Production First

Design for:

- Security
- Scalability
- Maintainability
- Observability


## 3. Avoid Unnecessary Complexity

Introduce complexity only when required.


## 4. Preserve Existing Decisions

Do not replace major architectural decisions without an ADR.


---

# Current Architecture Direction


## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui


## Backend

- Python
- FastAPI


## Database

- PostgreSQL
- pgvector


## Cache / Memory

- Redis


## Voice Platform

- Twilio SIP
- LiveKit


## AI Platform

- OpenAI models
- LangChain
- LangGraph


## Knowledge System

- RAG
- Embeddings
- Vector search


---

# Development Rules

Before changing architecture:

1. Review existing documentation.
2. Check related ADRs.
3. Explain tradeoffs.
4. Update documentation.


After major work:

Update:

- PROJECT_STATE.md
- SESSION_LOG.md


---

# Current Project Phase

Phase 0 — Foundation


Current Goal:

Complete Version 2 Production Blueprint.

Then begin implementation.
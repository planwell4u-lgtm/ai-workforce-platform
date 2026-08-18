# ADR-003: Multi-Agent Orchestration using LangGraph

## Status

Accepted

## Context

Managing agentic workflows, branching logic, loop states, and multi-agent systems has become overly complex using linear state engines.

## Decision

We will use **LangGraph** to model agent systems as stateful multi-agent graphs.

## Consequences

- Built-in persistence for conversation checkpointing and time-travel debugging.
- Better control over cycles and routing conditions compared to chain structures.
- Requires learning curve for graph-based execution paradigms.

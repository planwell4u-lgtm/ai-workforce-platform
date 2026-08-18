# ADR 004: LangGraph for Agent Workflows

## Context
Complex multi-turn conversations and backend actions (workflows) require state management and looping execution logic.

## Decision
We will use LangGraph as the agent state-machine runtime.

## Consequences
- Flexible state management.
- Ability to define cyclic and acyclic graph-based agent structures.

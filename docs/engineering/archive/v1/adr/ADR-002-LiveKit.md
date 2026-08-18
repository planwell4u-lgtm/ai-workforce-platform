# ADR-002: Real-time Audio/Video with LiveKit

## Status

Accepted

## Context

The application requires low-latency real-time voice and video communication channels between users and automated AI agents.

## Decision

We will adopt **LiveKit** as the core WebRTC SFU (Selective Forwarding Unit) framework instead of building custom WebRTC orchestration from scratch.

## Consequences

- Direct low-latency real-time WebRTC support.
- Requires deploying and maintaining LiveKit Server instances or using LiveKit Cloud.
- Out-of-the-box support for egress recording and agent integrations.

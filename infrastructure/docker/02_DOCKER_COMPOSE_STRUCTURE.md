# Docker Compose Structure

**Version:** 2.0  
**Status:** Production Approved

---

# 1. Overview

Docker Compose provides the local orchestration layer for the Voice Agent SaaS Platform. It enables developers to start the complete application stack with a single command while maintaining a production-like development environment.

Docker Compose is intended for:

- Local development
- Integration testing
- Developer onboarding
- Feature validation
- Local debugging

It is **not** used for production deployments. Production deployments are managed by Kubernetes.

---

# 2. Objectives

The Docker Compose architecture aims to:

- Simplify local setup
- Standardize development environments
- Reduce onboarding time
- Support isolated service development
- Provide production-like networking
- Enable repeatable local testing

---

# 3. Architecture

```
                Docker Compose
                      │
 ┌──────────────────────────────────────┐
 │                                      │
 │  Frontend (Next.js)                  │
 │  Backend API (FastAPI)               │
 │  AI Runtime Worker                   │
 │  Voice Worker                        │
 │  Background Worker                   │
 │  PostgreSQL                          │
 │  Redis                               │
 │  LiveKit                             │
 │  Monitoring Stack (Optional)         │
 │                                      │
 └──────────────────────────────────────┘
```

---

# 4. Directory Structure

Recommended project structure:

```
docker/

├── compose.yaml
├── compose.override.yaml
├── compose.monitoring.yaml
├── compose.testing.yaml
├── .env.example
│
├── backend/
│   └── Dockerfile
│
├── frontend/
│   └── Dockerfile
│
├── workers/
│   ├── ai/
│   │   └── Dockerfile
│   └── voice/
│       └── Dockerfile
│
├── livekit/
│   └── livekit.yaml
│
├── postgres/
│   └── init/
│
├── redis/
│
└── monitoring/
```

---

# 5. Compose Files

The platform may use multiple Compose files.

| File | Purpose |
|-------|----------|
| compose.yaml | Base services |
| compose.override.yaml | Developer overrides |
| compose.testing.yaml | Testing environment |
| compose.monitoring.yaml | Monitoring stack |
| compose.debug.yaml | Optional debugging services |

---

# 6. Core Services

The base Compose configuration includes:

- Frontend
- Backend API
- PostgreSQL
- Redis
- LiveKit
- AI Runtime Worker
- Voice Worker
- Background Worker

Each service is independently restartable.

---

# 7. Frontend Service

Responsibilities:

- Next.js application
- Developer hot reload
- API communication
- UI testing

Dependencies:

- Backend API

---

# 8. Backend API

Responsibilities:

- REST API
- Authentication
- Agent management
- WebSocket endpoints
- Business logic

Dependencies:

- PostgreSQL
- Redis
- LiveKit
- Workers

---

# 9. AI Runtime Worker

Responsibilities:

- Agent execution
- Tool invocation
- Memory retrieval
- RAG processing
- Workflow execution

Dependencies:

- Backend API
- PostgreSQL
- Redis

---

# 10. Voice Worker

Responsibilities:

- LiveKit integration
- Voice sessions
- STT
- LLM interaction
- TTS
- Audio streaming

Dependencies:

- LiveKit
- Backend API

---

# 11. Background Worker

Handles asynchronous jobs such as:

- Notifications
- Scheduled tasks
- Cleanup
- Analytics processing
- Report generation

---

# 12. PostgreSQL

Development database.

Provides:

- Multi-tenant storage
- Application data
- Vector storage (pgvector)
- Migration support

Persistent storage is provided through Docker volumes.

---

# 13. Redis

Redis provides:

- Cache
- Session storage
- Queues
- Pub/Sub
- Distributed locks

Persistent storage is optional for local development.

---

# 14. LiveKit

The local LiveKit instance provides:

- WebRTC signaling
- Room management
- Audio routing
- Local voice testing

Configuration is mounted from external files.

---

# 15. Optional Monitoring Stack

Developers may enable monitoring services.

Optional components include:

- Prometheus
- Grafana
- Loki
- Tempo
- OpenTelemetry Collector

These services are not required for daily development.

---

# 16. Networks

Compose creates isolated Docker networks.

Recommended layout:

```
frontend-network

backend-network

database-network

monitoring-network
```

Internal services communicate using service names.

---

# 17. Volumes

Persistent volumes include:

```
postgres-data

redis-data

livekit-data

uploads

cache
```

Application containers remain stateless.

---

# 18. Environment Variables

Configuration is loaded from:

```
.env

.env.local

compose overrides
```

Common variables include:

- Database URL
- Redis URL
- API secrets
- LiveKit keys
- Twilio credentials
- OpenAI API key
- Feature flags

Secrets must never be committed to source control.

---

# 19. Service Dependencies

Typical startup order:

```
PostgreSQL
      │
      ▼
Redis
      │
      ▼
Backend API
      │
      ▼
Workers
      │
      ▼
Frontend
```

Compose `depends_on` may be used for startup sequencing, but application-level health checks remain necessary.

---

# 20. Health Checks

Services should expose health endpoints.

Examples:

- API readiness
- Database connectivity
- Redis availability
- Worker health
- LiveKit status

Compose can restart unhealthy services automatically.

---

# 21. Logging

All containers log to standard output.

Requirements:

- Structured logs
- Request IDs
- Timestamps
- Log levels

Logs may be viewed using:

```
docker compose logs
```

---

# 22. Development Workflow

Typical workflow:

```
Clone Repository

        │

Configure .env

        │

docker compose up

        │

Development

        │

Testing

        │

docker compose down
```

Developers should not manually configure dependencies outside Docker unless required.

---

# 23. Scaling

Docker Compose supports limited local scaling.

Example:

```
docker compose up --scale ai-worker=3
```

Compose scaling is intended for development and testing only.

---

# 24. Best Practices

The platform follows these Docker Compose practices:

- Single responsibility per service
- Named volumes
- Environment-based configuration
- Health checks
- Service isolation
- Consistent networking
- Externalized secrets
- Production-like topology
- Minimal developer setup

---

# 25. Relationship to Kubernetes

Docker Compose and Kubernetes serve different purposes.

| Docker Compose | Kubernetes |
|----------------|------------|
| Local development | Production orchestration |
| Single host | Multi-node clusters |
| Developer workflow | Production deployments |
| Lightweight | Highly scalable |
| Rapid iteration | High availability |

Compose configurations should closely mirror production architecture without duplicating Kubernetes-specific features.

---

# 26. Summary

Docker Compose provides a consistent and repeatable local development environment for the Voice Agent SaaS Platform.

Its architecture ensures:

- Fast onboarding
- Consistent local environments
- Production-like service topology
- Simplified testing
- Reliable developer workflows
- Seamless transition to Kubernetes deployments
# Development Containers

**Version:** 2.0  
**Status:** Production Approved

---

# 1. Overview

Development Containers (Dev Containers) provide a standardized, isolated, and reproducible development environment for the Voice Agent SaaS Platform.

Every developer works inside the same containerized environment regardless of their host operating system, eliminating configuration drift and reducing onboarding time.

Development Containers are based on Docker and integrate with modern IDEs such as Visual Studio Code.

---

# 2. Objectives

The Development Container strategy aims to:

- Standardize developer environments
- Eliminate "works on my machine" issues
- Simplify onboarding
- Ensure dependency consistency
- Improve reproducibility
- Support cross-platform development
- Enable secure local development

---

# 3. Architecture

```
Developer Workstation
        │
        ▼
Development Container
        │
 ┌─────────────────────────────┐
 │ Ubuntu Base Image           │
 │ Python                      │
 │ Node.js                     │
 │ pnpm / npm                  │
 │ Docker CLI                  │
 │ Git                         │
 │ Development Tools           │
 │ VS Code Extensions          │
 └─────────────────────────────┘
        │
        ▼
Docker Compose Services
        │
        ▼
Application Stack
```

---

# 4. Directory Structure

Recommended layout:

```
.devcontainer/

├── devcontainer.json
├── Dockerfile
├── post-create.sh
├── post-start.sh
├── features.json
└── README.md
```

---

# 5. Dev Container Components

The development container includes:

- Ubuntu LTS base image
- Python
- Node.js LTS
- pnpm
- Git
- Docker CLI
- Docker Compose
- PostgreSQL client
- Redis CLI
- curl
- wget
- jq
- build-essential

Additional tools may be installed as required.

---

# 6. Supported IDE

Primary IDE:

- Visual Studio Code

Supported extensions include:

- Python
- Pylance
- Docker
- GitHub Copilot
- ESLint
- Prettier
- Tailwind CSS
- YAML
- Markdown
- Kubernetes

---

# 7. Language Runtimes

The development container standardizes runtime versions.

Current standards:

| Component | Version |
|-----------|---------|
| Python | 3.13+ |
| Node.js | 22 LTS |
| pnpm | Latest supported |
| Git | Current stable |

Runtime versions should remain synchronized with CI/CD.

---

# 8. Development Tools

The container provides common development utilities.

Examples:

- pip
- uv
- npm
- pnpm
- git
- make
- bash
- curl
- jq
- openssl

---

# 9. Source Code Mounting

Application source code is mounted into the container.

```
Host Repository
        │
        ▼
Development Container
        │
        ▼
Workspace
```

Changes on the host are immediately visible inside the container.

---

# 10. Environment Variables

Development configuration is supplied through:

- `.env`
- `.env.local`
- Docker Compose
- Dev Container configuration

Sensitive credentials should not be committed to source control.

---

# 11. Docker Integration

The development container communicates with the local Docker engine.

This allows developers to:

- Build images
- Run Docker Compose
- View logs
- Inspect containers
- Execute commands

The Docker daemon runs on the host machine.

---

# 12. Networking

The development container shares Docker networking with the application stack.

Typical communication includes:

- Backend API
- PostgreSQL
- Redis
- LiveKit
- AI Workers

Service discovery uses Docker service names.

---

# 13. Persistent Storage

Developer data persists outside the container.

Examples:

- Source code
- Git configuration
- SSH keys
- Package caches
- Docker volumes

Containers remain disposable.

---

# 14. Development Workflow

Typical workflow:

```
Clone Repository

        │

Open in VS Code

        │

Reopen in Container

        │

Container Builds

        │

Dependencies Installed

        │

Start Docker Compose

        │

Begin Development
```

---

# 15. Dependency Management

Dependencies are installed during container initialization.

Examples:

- Python packages
- Node packages
- Development tools
- Linters
- Formatters

Dependency installation should be automated.

---

# 16. Security

Development containers follow security best practices.

Requirements:

- Non-root user
- Least privilege
- No embedded secrets
- Updated base images
- Minimal installed packages

Production credentials must never be used in local environments.

---

# 17. Performance

To improve performance:

- Use cached package managers
- Minimize image layers
- Reuse Docker volumes
- Enable incremental builds
- Avoid unnecessary rebuilds

---

# 18. CI/CD Alignment

The development environment should closely resemble CI.

Consistency includes:

- Runtime versions
- Build tools
- Dependency versions
- Linting
- Formatting
- Testing

This reduces integration failures.

---

# 19. Common Tasks

Developers typically perform:

- Build applications
- Run unit tests
- Execute integration tests
- Run linters
- Format code
- Debug services
- View logs
- Build Docker images

All tasks should execute successfully within the container.

---

# 20. Maintenance

Development container images should be updated regularly.

Updates include:

- Security patches
- Runtime upgrades
- Dependency updates
- Tooling improvements

Changes should be documented and version controlled.

---

# 21. Best Practices

The platform follows these Development Container practices:

- Consistent runtime versions
- Disposable containers
- Externalized configuration
- Automated setup
- Non-root execution
- Shared development standards
- Minimal host dependencies
- Version-controlled configuration

---

# 22. Summary

Development Containers provide a consistent, secure, and reproducible development environment for the Voice Agent SaaS Platform.

The strategy ensures:

- Faster onboarding
- Reliable development environments
- Cross-platform compatibility
- Reduced configuration issues
- Consistent tooling
- Alignment with CI/CD
- Improved developer productivity
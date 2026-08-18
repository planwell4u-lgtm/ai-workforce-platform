# 03 Helm Chart Example
# Helm Chart Example

**Version:** 2.0

---

# 1. Overview

This document demonstrates a production-ready Helm Chart deployment example for the Voice Agent SaaS platform.

Helm provides package management capabilities for Kubernetes, allowing complex application deployments to be versioned, configured, upgraded, and managed consistently across multiple environments.

Helm simplifies:

- Kubernetes configuration management
- Application packaging
- Environment customization
- Release management
- Rollbacks
- Deployment automation

---

# 2. Objectives

The Helm deployment strategy should:

- Package Kubernetes resources
- Support multiple environments
- Enable configuration overrides
- Manage application versions
- Simplify upgrades
- Provide repeatable deployments

---

# 3. Helm Architecture

```
                 Helm Chart

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

   Templates    Values Files   Charts

        │            │            │

        └────────────┼────────────┘

                     ▼

            Kubernetes Resources

                     │

                     ▼

              Running Platform
```

---

# 4. Chart Structure

Example:

```
voice-agent-platform/

├── Chart.yaml

├── values.yaml

├── templates/

│   ├── deployment.yaml

│   ├── service.yaml

│   ├── ingress.yaml

│   ├── configmap.yaml

│   ├── secret.yaml

│   └── hpa.yaml

└── charts/
```

---

# 5. Chart Definition

`Chart.yaml`

```yaml
apiVersion: v2

name: voice-agent-platform

description: AI Voice Agent SaaS Platform

type: application

version: 2.0.0

appVersion: "2.0"
```

---

# 6. Values Configuration

`values.yaml`

```yaml
replicaCount: 3


image:

  repository: voice-agent/backend

  tag: "v2"


service:

  type: ClusterIP

  port: 8000


resources:

  requests:

    cpu: 500m

    memory: 512Mi

  limits:

    cpu: 2

    memory: 2Gi
```

---

# 7. Deployment Template

Example:

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:

  name: {{ include "app.fullname" . }}


spec:

  replicas: {{ .Values.replicaCount }}


  template:

    spec:

      containers:

      - name: backend

        image:

          "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

Templates allow dynamic configuration.

---

# 8. Environment Values

Recommended structure:

```
values/

├── development.yaml

├── staging.yaml

└── production.yaml
```

Example:

Development:

```yaml
replicaCount: 1
```

Production:

```yaml
replicaCount: 5
```

---

# 9. Helm Release Lifecycle

```
Create Chart

      │

Package Chart

      │

Install Release

      │

Upgrade Release

      │

Monitor

      │

Rollback if Needed
```

---

# 10. Installation

Install example:

```bash
helm install voice-agent ./voice-agent-platform
```

---

# 11. Upgrade

Example:

```bash
helm upgrade voice-agent ./voice-agent-platform
```

Helm updates only changed resources.

---

# 12. Rollback

Example:

```bash
helm rollback voice-agent 1
```

Rollback restores a previous release version.

---

# 13. Secrets Management

Sensitive values should not be stored directly.

Use:

- Kubernetes Secrets
- External Secrets Operator
- Cloud secret managers
- Vault integration

Example:

```
Application

     │

Secret Reference

     │

Secret Manager

```

---

# 14. Dependency Management

Helm supports dependencies:

Example:

```
voice-agent-platform

        │

        ├── PostgreSQL

        ├── Redis

        ├── Monitoring

        └── Message Queue
```

Dependencies should be version pinned.

---

# 15. Deployment Environments

Example:

```
Development

      │

Staging

      │

Production
```

Each environment may override:

- Replicas
- Resources
- Features
- External integrations
- Logging levels

---

# 16. CI/CD Integration

Pipeline:

```
Code Commit

      │

Build Container

      │

Package Helm Chart

      │

Security Scan

      │

Deploy Environment

      │

Validate Release
```

---

# 17. Security

Helm deployments should:

- Validate templates
- Scan container images
- Protect secrets
- Use least privilege RBAC
- Restrict chart permissions
- Review changes before deployment

---

# 18. Observability

Monitor:

- Helm releases
- Deployment status
- Upgrade failures
- Rollback events
- Kubernetes resources
- Application health

---

# 19. Testing

Validate:

- Template rendering
- Chart installation
- Upgrade process
- Rollback process
- Environment overrides
- Dependency resolution
- Resource configuration

Useful commands:

```bash
helm lint ./chart
```

```bash
helm template ./chart
```

---

# 20. Best Practices

Always:

- Version charts
- Keep values organized
- Separate environments
- Validate templates
- Pin dependencies
- Automate deployments
- Document configuration options

Avoid:

- Hardcoding values
- Storing secrets in charts
- Large unmaintainable templates
- Manual production changes
- Unversioned releases

---

# 21. Example Deployment Flow

```
Developer Update

        │

Modify Helm Values

        │

Package Chart

        │

CI Validation

        │

Deploy Release

        │

Monitor Health

        │

Promote Environment
```

---

# 22. Future Enhancements

Potential improvements:

- GitOps-based Helm deployment
- Automated chart testing
- Helm security scanning
- Progressive delivery
- Canary releases
- Multi-cluster deployment
- Automated rollback policies

---

# 23. Summary

Helm provides a consistent deployment packaging layer for the Voice Agent SaaS platform. By combining reusable templates, environment-specific configuration, versioned releases, and automated lifecycle management, Helm enables reliable Kubernetes deployments across development, staging, and production environments.
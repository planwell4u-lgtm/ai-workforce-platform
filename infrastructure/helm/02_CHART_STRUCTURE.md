# Chart Structure

**Version:** 2.0  
**Status:** Production Approved

---

# 1. Overview

This document defines the standard structure for Helm charts used throughout the Voice Agent SaaS Platform.

A consistent chart structure improves maintainability, simplifies deployments, enables code reuse, and ensures predictable Kubernetes resource generation.

All application and infrastructure charts must follow this standard.

---

# 2. Objectives

The Helm chart structure aims to:

- Standardize deployments
- Improve maintainability
- Reduce duplication
- Simplify onboarding
- Support reusable templates
- Enable automated CI/CD
- Ensure production consistency

---

# 3. Chart Organization

Each deployable component has its own chart.

Example:

```text
helm/

├── backend/
├── frontend/
├── ai-runtime/
├── voice-worker/
├── scheduler/
├── monitoring/
├── ingress/
└── shared/
```

Each chart is independently versioned and deployable.

---

# 4. Standard Chart Layout

Every Helm chart should follow the same directory structure.

```text
backend/

├── Chart.yaml
├── values.yaml
├── values-development.yaml
├── values-staging.yaml
├── values-production.yaml
├── .helmignore
│
├── charts/
│
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   ├── networkpolicy.yaml
│   ├── pdb.yaml
│   └── NOTES.txt
│
└── README.md
```

---

# 5. Chart.yaml

`Chart.yaml` contains chart metadata.

Typical metadata includes:

- Chart name
- Description
- Version
- Application version
- Type
- Dependencies
- Maintainers

It should not contain deployment configuration.

---

# 6. values.yaml

`values.yaml` provides default configuration.

Typical settings include:

- Image repository
- Image tag
- Replica count
- Resources
- Ports
- Service type
- Feature flags

Environment-specific values override these defaults.

---

# 7. Environment Values

Separate values files are maintained for each environment.

```text
values-development.yaml

values-staging.yaml

values-production.yaml
```

Only environment-specific settings should differ.

---

# 8. Templates Directory

The `templates/` directory contains Kubernetes resource definitions.

Common templates include:

- Deployment
- StatefulSet
- Service
- Ingress
- ConfigMap
- Secret
- HorizontalPodAutoscaler
- ServiceAccount
- NetworkPolicy
- PodDisruptionBudget

Each template should manage a single resource type.

---

# 9. Helper Templates

`_helpers.tpl` contains reusable template logic.

Typical helpers include:

- Resource names
- Labels
- Selector labels
- Image references
- Common annotations
- Full names

Reusable helpers reduce duplication across templates.

---

# 10. Dependencies

Dependent charts are declared in `Chart.yaml`.

Examples:

- PostgreSQL
- Redis
- Common library charts

Dependencies should use explicit versions to ensure reproducible deployments.

---

# 11. Resource Naming

Resources should follow a consistent naming convention.

Example:

```text
<release>-<component>
```

Examples:

```text
voice-api

voice-frontend

voice-worker
```

Names should be predictable and unique within a namespace.

---

# 12. Labels and Annotations

Every resource should include standard Kubernetes labels.

Recommended labels:

- app.kubernetes.io/name
- app.kubernetes.io/component
- app.kubernetes.io/version
- app.kubernetes.io/instance
- app.kubernetes.io/managed-by

Additional annotations may be used for operational tooling.

---

# 13. Configuration

Application configuration should be managed through:

- ConfigMaps
- Kubernetes Secrets
- Environment variables

Configuration should never be hardcoded into templates.

---

# 14. Image Configuration

Container configuration typically includes:

- Repository
- Tag
- Pull policy
- Image pull secrets

Images should use immutable version tags in production.

---

# 15. Resource Configuration

Each chart should define configurable resources.

Examples:

- CPU requests
- CPU limits
- Memory requests
- Memory limits

Resource settings are managed through values files.

---

# 16. Health Checks

Application charts should support:

- Startup probes
- Readiness probes
- Liveness probes

Health check configuration should be configurable through values files.

---

# 17. Security Configuration

Security-related templates may include:

- ServiceAccount
- RBAC
- NetworkPolicy
- SecurityContext
- PodSecurityContext

Security should follow the principle of least privilege.

---

# 18. Documentation

Every chart should include a `README.md` describing:

- Purpose
- Installation
- Configuration
- Values
- Dependencies
- Upgrade notes
- Troubleshooting

Documentation should remain synchronized with the chart.

---

# 19. Validation

Charts should be validated before deployment using:

- Helm lint
- Template rendering
- Kubernetes schema validation
- CI/CD checks

Invalid charts must not be released.

---

# 20. Best Practices

The platform follows these Helm chart principles:

- One chart per deployable component
- Minimal template logic
- Reusable helper templates
- Environment-specific values
- Version-controlled charts
- Immutable image references
- Standard labels
- Secure defaults
- Comprehensive documentation

---

# 21. Summary

A standardized Helm chart structure provides a consistent foundation for deploying the Voice Agent SaaS Platform.

It ensures:

- Maintainable charts
- Reusable templates
- Consistent deployments
- Simplified operations
- Reliable CI/CD integration
- Production-ready Kubernetes deployments
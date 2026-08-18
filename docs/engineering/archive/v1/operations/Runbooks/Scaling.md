# Scaling & Resource Allocation Runbook

Procedures for dynamically scaling application workloads under high traffic volumes.

## Manual Scaling

To manually scale the Kubernetes deployments:

```bash
kubectl scale deployment/prod-api --replicas=6
```

## Autoscaling Configuration

Autoscaling is managed via Horizontal Pod Autoscaler (HPA):

- **Target Metric:** 75% CPU Utilization
- **Minimum Replicas:** 3
- **Maximum Replicas:** 10

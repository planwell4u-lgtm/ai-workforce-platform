# Load Testing

Procedures and metrics for testing performance limits under heavy load.

## Tooling

- **k6:** Principal tool for scripting load and performance scenarios.
- **Locust:** Python-based alternative for developer-defined agent behavior.

## Standard Scenarios

1. **Smoke Test:** Validate response times and error rates under nominal (low) traffic.
2. **Stress Test:** Scale up virtual users (VUs) gradually until system bottlenecks or crashes occur.
3. **Soak Test:** Run sustained medium-high traffic over 8-24 hours to monitor memory leaks or resource exhaustion.

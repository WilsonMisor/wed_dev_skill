# Infrastructure Environment Strategy

Define production and non production environments with explicit isolation and promotion rules.

## For each environment record

1. Purpose.
2. Hosting and region.
3. Network exposure.
4. Data classification.
5. Identity and access.
6. Secrets source.
7. External integrations.
8. Feature flags.
9. Deployment method.
10. Observability.
11. Backup and reset policy.
12. Cost ownership.

Production must not depend on undocumented local machine state.

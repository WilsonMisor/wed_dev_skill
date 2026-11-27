# Deployment Governance

Deployment must be reproducible, observable, and reversible or have a documented mitigation when true rollback is impossible.

## Release preparation

1. Identify exact build or commit.
2. Verify required tests and approvals.
3. Review configuration and secrets.
4. Review database and data migration order.
5. Confirm backups where needed.
6. Define rollout method and health checks.
7. Define rollback or forward fix criteria.
8. Define monitoring and owner during release.
9. Record release notes and known limitations.

## Verification

After deployment verify health, critical journeys, migrations, jobs, integrations, metrics, logs, alerts, and user visible version where applicable.

Do not infer production success solely from a deployment command returning zero.

# Containers

Use containers when they improve reproducibility, deployment, isolation, or platform compatibility.

## Controls

1. Pin appropriate base image versions.
2. Use minimal runtime images where practical.
3. Run as non root where supported and appropriate.
4. Keep secrets out of image layers.
5. Use deterministic dependency installation.
6. Add health checks when useful.
7. Separate build and runtime dependencies.
8. Scan dependencies and images when tooling exists.
9. Define resource limits in orchestrated environments.
10. Log to the platform rather than ephemeral local files unless intentionally persisted.

Containers do not replace application authorization or host security.

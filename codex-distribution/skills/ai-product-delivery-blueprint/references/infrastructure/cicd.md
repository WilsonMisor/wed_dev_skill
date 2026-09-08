# CI and CD

CI and CD should make verification and release reproducible.

## Pipeline stages as applicable

1. Dependency restore.
2. Formatting and linting.
3. Static analysis.
4. Unit and integration tests.
5. Build.
6. Security and dependency checks.
7. Contract tests.
8. Artifact creation.
9. Deployment to non production.
10. QA or approval gate.
11. Production deployment.
12. Post deployment verification.

Protect production environments and secrets. Do not allow untrusted pull request code to access production credentials.

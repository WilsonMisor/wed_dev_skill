# Secrets Management

Secrets include passwords, API keys, signing keys, tokens, private certificates, encryption keys, and privileged connection strings.

## Requirements

1. Store secrets in an approved secret manager or protected environment mechanism.
2. Keep secrets out of Git history, logs, screenshots, analytics, and generated documentation.
3. Grant least privilege access.
4. Separate environments.
5. Rotate when exposed or according to policy.
6. Define ownership and recovery.
7. Protect CI and deployment access.
8. Prefer short lived credentials where practical.
9. Scan for accidental secret commits where tooling permits.

If a secret is committed, removing the current line is not enough. Treat it as exposed and rotate it.

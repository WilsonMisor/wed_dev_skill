# Security Governance

Security is a design and implementation requirement.

## Minimum process

1. Identify assets, actors, trust boundaries, entry points, sensitive operations, and abuse cases.
2. Create a threat model and Security Control Matrix.
3. Map controls to authentication, authorization, input handling, output encoding, database access, files, APIs, webhooks, background jobs, secrets, dependencies, infrastructure, logging, and recovery.
4. Apply least privilege.
5. Protect secrets and credentials outside source control.
6. Validate untrusted input and encode output for its context.
7. Protect state changing requests and sensitive actions from forgery and replay where relevant.
8. Log security significant events without leaking sensitive values.
9. Keep dependencies and runtime components within supported and patched versions.
10. Test security controls and negative paths.

Unresolved critical or high findings block release unless an accountable human records accepted risk, mitigation, owner, and expiry.

# Tenant Isolation

Tenant isolation is a hard security boundary.

## Isolation surfaces

1. Database queries and writes.
2. Row level security when used.
3. ORM scopes and repositories.
4. Caches and cache keys.
5. File and object storage paths and policies.
6. Search indexes.
7. Background and scheduled jobs.
8. Queue messages.
9. Webhooks.
10. Analytics and reporting.
11. Logs and support tooling.
12. Exports and imports.
13. Administrative impersonation or support access.

## Verification

Create positive and negative tests that attempt access using resources from another tenant. Include guessed identifiers, stale membership, removed roles, background jobs, cached data, downloads, and privileged support paths.

Any unintended cross tenant read or write is a release blocking defect.

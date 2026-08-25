# SaaS API Design

Apply the API profile with SaaS context.

## SaaS additions

1. Tenant context must be derived and verified securely.
2. Permissions and entitlements are enforced per operation.
3. Resource identifiers do not imply authorization.
4. Plan limits and quotas return predictable errors.
5. Administrative endpoints are isolated and strongly authorized.
6. Pagination and filtering cannot bypass tenant restrictions.
7. API keys or service accounts have scoped permissions and revocation.
8. Audit high privilege or financial operations.
9. Document rate limits and retry semantics.
10. Version externally consumed contracts deliberately.

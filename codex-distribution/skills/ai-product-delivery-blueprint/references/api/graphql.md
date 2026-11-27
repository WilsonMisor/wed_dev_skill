# GraphQL Profile

Use GraphQL only when its flexible graph query model solves a real product or integration need.

## Controls

1. Schema ownership and evolution policy.
2. Resolver authorization at appropriate resource boundaries.
3. Tenant isolation.
4. Query depth, complexity, size, or cost controls.
5. N plus one prevention and batching where required.
6. Pagination for large connections.
7. Error handling without sensitive leakage.
8. Mutation idempotency where consequential retries can occur.
9. Introspection policy based on exposure and risk.
10. Persisted operations or allow lists when warranted.
11. Observability by operation.
12. Schema and resolver tests.

Do not rely on a hidden field in the client as an authorization control.

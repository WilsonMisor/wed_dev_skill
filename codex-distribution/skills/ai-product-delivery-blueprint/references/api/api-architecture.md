# API Architecture

Define APIs as stable system boundaries, not incidental controller methods.

## Required decisions

1. Consumers and use cases.
2. Protocol and interaction style.
3. Resource, command, query, or operation model.
4. Authentication and authorization.
5. Request and response schemas.
6. Error contract.
7. Validation.
8. Pagination, filtering, sorting, and limits.
9. Idempotency and concurrency.
10. Versioning and compatibility.
11. Rate limiting and abuse protection.
12. Observability and audit.
13. Documentation and contract testing.
14. Deprecation and retirement.

External and multi client APIs require stronger compatibility discipline than private single consumer interfaces.

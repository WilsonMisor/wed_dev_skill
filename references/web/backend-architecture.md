# Web Backend Architecture

Apply when the web product includes server side application logic.

## Define

1. Request handling boundaries.
2. Domain and service responsibilities.
3. Authentication and authorization enforcement.
4. Validation and serialization.
5. Database transaction boundaries.
6. File and object storage handling.
7. Background jobs and scheduled work.
8. Caching and invalidation.
9. External service timeouts, retries, and circuit behaviour where needed.
10. Logging, metrics, tracing, and audit events.
11. Configuration and secrets.
12. Deployment topology and scaling assumptions.

Server side authorization is mandatory for protected resources even when the UI hides unavailable actions.

# REST API Profile

## Design rules

1. Use stable resource or operation semantics.
2. Select HTTP methods according to behaviour and idempotency expectations.
3. Return meaningful status codes.
4. Use consistent request and response envelopes only when they add clear value.
5. Separate transport concerns from domain behaviour.
6. Define partial update semantics explicitly.
7. Use conditional requests or version fields when lost updates are a risk.
8. Provide predictable pagination and filtering.
9. Document cacheability.
10. Avoid leaking internal stack traces or database details.

Use OpenAPI or equivalent machine readable contracts when multiple consumers, generated clients, or strong contract verification justify it.

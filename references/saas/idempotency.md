# Idempotency

Use idempotency where retries could create duplicate financial, provisioning, notification, booking, or other consequential effects.

## Define

1. Operation scope.
2. Idempotency key source.
3. Tenant or user binding.
4. Request fingerprint if needed.
5. Storage and expiry.
6. In progress behaviour.
7. Success replay behaviour.
8. Failure and retry behaviour.
9. Concurrency handling.
10. Observability.

An idempotency key must not allow one tenant or user to retrieve another caller's result.

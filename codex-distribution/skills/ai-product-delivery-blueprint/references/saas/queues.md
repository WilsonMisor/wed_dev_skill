# Queues

Use queues for work that benefits from asynchronous processing, buffering, or controlled retries.

## Define

1. Message contract and version.
2. Tenant context.
3. Producer and consumer ownership.
4. Delivery semantics.
5. Idempotency requirements.
6. Retry policy and backoff.
7. Maximum attempts.
8. Dead letter handling.
9. Ordering requirements.
10. Visibility timeout or lease behaviour.
11. Observability and alerting.
12. Poison message handling.

Never assume exactly once delivery unless the complete system genuinely guarantees it.

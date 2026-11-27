# Transactions and Consistency

Define business operations that must commit atomically.

## Consider

1. Transaction boundary.
2. Isolation level.
3. Concurrent updates.
4. Locking and deadlocks.
5. Unique constraint races.
6. External side effects that cannot participate in the database transaction.
7. Outbox or equivalent coordination when durable event publication is required.
8. Retry safety.
9. Idempotency.
10. Compensation for distributed operations.

Do not make external network calls inside long database transactions without understanding lock and failure consequences.

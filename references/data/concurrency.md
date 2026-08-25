# Data Concurrency

Concurrent users, workers, retries, and integrations can race even in small applications.

## Address

1. Lost updates.
2. Duplicate creation.
3. Inventory or capacity contention.
4. Financial balance changes.
5. State machine transitions.
6. Background job duplication.
7. Webhook and user action races.
8. Optimistic or pessimistic locking.
9. Unique constraints.
10. Transaction isolation.

Write tests that reproduce critical races where feasible. A happy path sequential test does not prove concurrency safety.

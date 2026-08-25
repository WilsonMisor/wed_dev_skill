# Offline Synchronization

Synchronization is a distributed data problem and needs explicit semantics.

## Define

1. Sync direction.
2. Entity version or change tracking.
3. Pending operation queue.
4. Ordering dependencies.
5. Idempotency.
6. Retry and backoff.
7. Network and battery constraints.
8. Conflict detection.
9. Deletion semantics and tombstones where needed.
10. Partial failure handling.
11. Observability and user feedback.
12. Recovery after app termination mid sync.

Test duplicate delivery, reordering, concurrent edits, long offline periods, token expiry, and schema upgrades.

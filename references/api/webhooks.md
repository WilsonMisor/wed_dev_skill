# API Webhooks

## Incoming webhooks

Verify authenticity, handle replay, deduplicate, process idempotently, tolerate out of order events, and reconcile missed delivery.

## Outgoing webhooks

1. Define event catalogue and schema versions.
2. Sign payloads.
3. Use unique event IDs.
4. Retry with bounded backoff.
5. Provide delivery history where product scope requires it.
6. Protect destination secrets.
7. Allow endpoint rotation and disabling.
8. Prevent one tenant destination from receiving another tenant's events.
9. Define timeout and response expectations.
10. Provide replay tooling only with strong authorization and audit controls.

# Background Jobs

Background work must preserve authorization, tenant scope, idempotency, and observability outside the request path.

## Each job defines

1. Trigger.
2. Input contract.
3. Tenant and actor context where needed.
4. Idempotency behaviour.
5. Concurrency controls.
6. Retry and timeout policy.
7. Failure escalation.
8. Cancellation where needed.
9. Audit and logs.
10. Safe replay behaviour.

Scheduled jobs that scan many tenants must prevent one tenant failure from corrupting another tenant's work.

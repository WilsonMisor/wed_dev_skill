# SaaS Authorization

Authorization must be explicit, server side, and testable.

## Model

For every protected resource or operation define:

1. Actor.
2. Tenant context.
3. Resource ownership or relationship.
4. Required permission or policy.
5. Conditions such as subscription entitlement or account status.
6. Allowed result.
7. Denial result.
8. Audit requirement.

Avoid scattered permission logic with inconsistent semantics. Centralize policy decisions where practical while keeping domain rules understandable.

Test horizontal privilege escalation, vertical privilege escalation, removed membership, stale tokens, disabled users, and direct API access.

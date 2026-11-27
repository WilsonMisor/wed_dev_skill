# Mobile API Integration

Treat the API as a versioned remote dependency that may be slow, unavailable, or newer than the installed client.

## Requirements

1. Generated or hand maintained client contract must map to the canonical API schema.
2. Define timeouts.
3. Retry only safe or idempotent operations.
4. Handle authentication renewal without retry loops.
5. Normalize API errors into user appropriate states.
6. Support cancellation when screens or operations end.
7. Handle connectivity changes.
8. Avoid logging secrets or sensitive payloads.
9. Support API version compatibility policy.
10. Add contract and integration tests for critical operations.

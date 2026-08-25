# SaaS Webhooks

Webhooks are untrusted network inputs even when sent by a trusted provider.

## Requirements

1. Authenticate or verify signature using the provider mechanism.
2. Preserve the raw payload when signature verification requires it.
3. Enforce replay or timestamp protections where available.
4. Parse only after verification when required by the signature scheme.
5. Deduplicate events.
6. Make handlers idempotent.
7. Handle out of order delivery.
8. Return promptly and move expensive work to controlled background processing when appropriate.
9. Record event ID, type, result, and retry status without leaking secrets.
10. Provide reconciliation for missed events.

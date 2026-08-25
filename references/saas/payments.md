# SaaS Payments

Use payment providers and tokenized methods so raw sensitive payment credentials are not handled unnecessarily.

## Controls

1. Define payment intent and order identifiers.
2. Verify provider responses server side.
3. Use idempotency for retryable payment creation and capture where supported.
4. Never mark an order paid from a client callback alone.
5. Reconcile provider and internal states.
6. Handle partial, failed, reversed, refunded, disputed, and duplicated payments.
7. Protect webhook verification secrets.
8. Restrict access to financial records.
9. Audit consequential state changes.
10. Test timeout and retry scenarios.

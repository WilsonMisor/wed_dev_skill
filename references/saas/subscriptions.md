# Subscription Lifecycle

Model subscriptions as explicit states rather than a single boolean.

## Consider

Trialing, active, payment due, past due, grace period, suspended, cancellation scheduled, cancelled, expired, and provider specific intermediate states as applicable.

For every state define entitlements, login, API usage, jobs, notifications, billing attempts, cancellation rights, reactivation, and data retention behaviour.

Provider webhook events are inputs to the internal state machine, not automatically the sole source of business truth. Handle out of order and duplicate events.

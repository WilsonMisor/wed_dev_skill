# API Idempotency

Use idempotency for state changing operations that clients may safely retry but must not execute twice.

Bind keys to the authenticated caller or tenant and operation. Define request fingerprint, storage duration, in progress behaviour, response replay, concurrency, and mismatch handling.

Payment creation, booking, provisioning, invitations, and external side effects are common candidates. Do not use idempotency as a substitute for database uniqueness or transaction integrity.

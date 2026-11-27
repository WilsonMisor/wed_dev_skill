# Account Lifecycle

Define account state as a controlled state machine.

## Typical states

Pending, active, restricted, suspended, cancellation scheduled, cancelled, retention, deleted, and compromised may apply.

For each state define login, API access, data visibility, writes, billing, jobs, integrations, exports, support access, notifications, retention, and recovery transitions.

Deletion must address primary records, derived data, files, search indexes, analytics identifiers, backups according to policy, and external processors where applicable.

Do not equate cancelling billing with immediately deleting product data unless the approved policy says so.

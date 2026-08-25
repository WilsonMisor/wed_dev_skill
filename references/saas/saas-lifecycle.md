# SaaS Delivery Lifecycle

Use this profile for hosted software with account, tenant, plan, entitlement, or recurring service responsibilities.

## SaaS lifecycle

1. Visitor or invited user.
2. Registration or identity federation.
3. Verification when required.
4. Account or organisation creation.
5. Tenant establishment.
6. Team invitations and membership.
7. Role and permission assignment.
8. Trial or initial entitlement.
9. Subscription or plan activation where applicable.
10. Normal usage and metering where applicable.
11. Upgrade, downgrade, add on, or entitlement changes.
12. Payment failure and recovery where billing exists.
13. Suspension and reactivation.
14. Cancellation.
15. Data export or portability where required.
16. Retention period.
17. Deletion or anonymisation.

For every state define permissions, data access, billing behaviour, jobs, notifications, API access, integrations, audit events, and transitions as applicable.

## Hard rule

Tenant isolation, authorization, billing state, and account lifecycle must be enforced server side. UI state is not an authority boundary.

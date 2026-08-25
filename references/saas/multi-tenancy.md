# Multi Tenancy

Define the tenancy model before data schema and authorization are frozen.

## Decide

1. What constitutes a tenant.
2. Whether a user can belong to one or multiple tenants.
3. Whether resources may be global, tenant scoped, user scoped, or shared by explicit relationship.
4. Tenant provisioning and deletion.
5. Tenant identifiers and immutable ownership fields.
6. Tenant context establishment for browser, mobile, API, jobs, webhooks, caches, files, search, analytics, and administrative tools.
7. Shared database, schema per tenant, database per tenant, or hybrid storage strategy.
8. Cross tenant administrative operations and safeguards.
9. Tenant migration, merge, export, and deletion policy.
10. Testing strategy for isolation.

Do not rely on client supplied tenant IDs without verifying the caller is authorized for that tenant.

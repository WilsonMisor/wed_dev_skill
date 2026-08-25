# Project Classification

Create a Project Classification Record before architecture or implementation.

## Required fields

1. Product name and problem statement.
2. Business model and delivery model.
3. User groups, privileged roles, operators, and external actors.
4. Delivery surfaces, including public web, authenticated web, WordPress, mobile, API, workers, scheduled jobs, integrations, admin tools, and data pipelines.
5. Persistent data stores and data sensitivity.
6. Tenant model. State single tenant, multi tenant, hybrid, or not applicable.
7. Identity providers and authentication methods.
8. Authorization model.
9. Payment, billing, subscription, escrow, or financial flows.
10. External APIs, webhooks, email, messaging, storage, search, analytics, and device services.
11. Hosting, CI and CD, environment, and operational constraints.
12. Regulatory, privacy, accessibility, security, data residency, or contractual triggers.
13. Required profiles.
14. Excluded profiles and why.
15. Unknowns that block a confident classification.

## Profile triggers

Activate `web` for browser delivered application or website behaviour.

Activate `wordpress` only when WordPress is a runtime or content management dependency. WordPress also activates `web`.

Activate `saas` when the product delivers recurring hosted software, tenant or account lifecycle, shared service infrastructure, plans or entitlements, or SaaS style operational responsibilities.

Activate `mobile` for installable Android or iOS applications. Load Flutter guidance when Flutter is selected.

Activate `api` when a programmatic service contract exists between components or external consumers.

Activate `data` when application state, business records, analytics data, or durable event data is persisted.

Activate `infrastructure` for production environments, hosting, networking, CI and CD, secrets, monitoring, backups, or disaster recovery.

## Output

Record a table with profile, status, trigger, required references, owner, and rationale. Do not infer that a profile is irrelevant merely because it is not visible to an end user.

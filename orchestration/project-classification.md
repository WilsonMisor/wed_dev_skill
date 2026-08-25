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
13. Production intent and expected blast radius.
14. PREOS production-assurance level: inactive, lightweight, standard, or high-assurance.
15. PREOS maturity stage: Stage 0 Prototype, Stage 1 Early Production, Stage 2 Product Traction, Stage 3 Scaling Product, Stage 4 Large Platform, or Stage 5 High Assurance / Global.
16. Required profiles.
17. Excluded profiles and why.
18. Unknowns that block a confident classification.

## Profile triggers

Activate `web` for browser delivered application or website behaviour.

Activate `wordpress` only when WordPress is a runtime or content management dependency. WordPress also activates `web`.

Activate `saas` when the product delivers recurring hosted software, tenant or account lifecycle, shared service infrastructure, plans or entitlements, or SaaS style operational responsibilities.

Activate `mobile` for installable Android or iOS applications. Load Flutter guidance when Flutter is selected.

Activate `api` when a programmatic service contract exists between components or external consumers.

Activate `data` when application state, business records, analytics data, or durable event data is persisted.

Activate `infrastructure` for production environments, hosting, networking, CI and CD, secrets, monitoring, backups, or disaster recovery.

## PREOS production-assurance trigger

PREOS is an assurance overlay rather than a delivery profile. Classify it separately by reading `orchestration/preos-routing.md`.

Use `inactive` only for genuinely disposable work with no production users, durable business dependency, sensitive data, consequential action, meaningful external exposure, or production release intent.

Use at least `lightweight` when an early pilot or internal system can affect real users, real data, operations, or business decisions.

Use `standard` for normal production software.

Strong signals for `high-assurance` include:

1. multi-tenancy or cross-customer isolation requirements;
2. money movement, billing, escrow, subscriptions, financial balances, or other financial correctness obligations;
3. sensitive/personal data or material privacy consequences;
4. privileged administration, identity, authorization, trust, reputation, or security-sensitive behaviour;
5. regulatory, contractual, legal-evidence, accessibility, residency, or retention obligations;
6. critical operational workflows or high blast radius;
7. consequential automated or AI-assisted decisions;
8. material vendor concentration or external dependency risk;
9. safety, fraud, abuse, economic-abuse, or hostile-user exposure;
10. production scale where recovery, reliability, capacity, or cost failure has significant consequence.

A lower assurance classification never makes a structurally necessary hard control optional. It changes assessment depth and evidence burden, not reality.

## Output

Record a table with profile or assurance layer, status, trigger, required references, owner, and rationale. Do not infer that a profile or PREOS concern is irrelevant merely because it is not visible to an end user.

For PREOS-active projects also record the maturity stage, accountable risk/production owner, known role gaps, and the source artifacts that will be bound into the PREOS Project Contract.
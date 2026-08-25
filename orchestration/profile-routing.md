# Profile Routing

Use the Project Classification Record to load only the guidance needed for the current work.

## Baseline routing

1. All substantial projects load the relevant files from `references/core/`.
2. Browser work loads `references/web/`.
3. WordPress work loads `references/web/` and `references/wordpress/`, plus the preserved root WordPress references named by the WordPress profile.
4. SaaS web products normally load core, web, SaaS, API, data, and infrastructure.
5. SaaS with mobile normally loads core, web if a browser client exists, SaaS, mobile, API, data, and infrastructure.
6. Mobile applications with remote services load core, mobile, API, and the data or infrastructure modules relevant to the remote service.
7. API only products load core, API, data when persistent state exists, and infrastructure for production operation.

## Bounded loading rule

Do not recursively read every file in an active profile. Select files by phase and task. For example, a billing task may require subscriptions, payments, webhooks, idempotency, security, API, data transactions, tests, and observability, but it does not automatically require mobile permissions or WordPress SEO.

## Conflict precedence

1. Explicit approved project requirement.
2. Applicable law, contract, or mandatory compliance requirement interpreted by an accountable human specialist.
3. Approved project architecture and security decisions.
4. Active profile rules.
5. Core defaults.
6. Tool or specialist recommendation.

Never use this order to silently override a conflict. Record the conflict and resolution.

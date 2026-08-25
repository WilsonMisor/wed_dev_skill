---
name: ai-product-delivery-blueprint
description: End to end AI assisted product delivery governance for web applications, WordPress, SaaS, APIs, data, infrastructure, Flutter mobile products, and PREOS production assurance. Classifies the project, loads only applicable delivery profiles, enforces PRD, SRS and SRD baselines, architecture and domain contracts, security and privacy controls, UX and design evidence, testing and QA, traceability, human approval gates, bounded AI task packets, production risk/economics/evidence assurance, deployment, operations, and gstack specialist routing. WordPress remains a specialised profile and retains the existing deep WordPress delivery framework.
---

# AI Product Delivery Blueprint

## Authority

Use this skill as the governing delivery layer for substantial AI assisted software and digital product work. It decides what must exist, what profiles apply, what evidence is required, which gates must pass, when PREOS production assurance applies, and when implementation may advance.

The skill does not replace specialist engineering judgment. It coordinates PREOS production assurance, Codex implementation, and gstack specialist review while keeping human owners responsible for risk acceptance and consequential approvals.

## Core operating rules

1. Classify the project before loading specialist references.
2. Load `references/core/*` for every substantial project.
3. Load only the applicable delivery profiles from `references/web`, `references/wordpress`, `references/saas`, `references/mobile`, `references/api`, `references/data`, and `references/infrastructure`.
4. Classify PREOS separately as a production-assurance overlay: inactive, lightweight, standard, or high-assurance. PREOS is not a delivery profile and does not replace the active product profiles.
5. Treat WordPress as a specialised web profile. Do not apply WordPress rules to general web, SaaS, API, or mobile work unless WordPress is actually in scope.
6. Treat SaaS, web, mobile, API, data, and infrastructure as composable profiles. A project may require several at once.
7. Establish canonical domain language and cross platform contracts before independent clients implement the same concepts.
8. Require approved product requirements before architecture is frozen, and require approved architecture and applicable design evidence before main implementation begins.
9. Convert implementation into bounded AI Task Packets. Each packet must state goal, non goals, requirement IDs, allowed files or systems, prohibited actions, acceptance criteria, tests, evidence, reviewer, approver, and rollback or handoff notes. When PREOS is active, enrich the same packet with applicable risk, control, economics, evidence-freshness, monitoring, recovery/reconciliation, change-impact, and production-gate requirements.
10. Preserve traceability from product requirement to architecture decision, design, code, test, security control, release evidence, and operations documentation. When PREOS is active, extend this chain through production risk, control, monitoring, recovery/reconciliation, and production-gate evidence as applicable.
11. Treat security, privacy, accessibility, reliability, backup, recovery, observability, production economics, hostile-user behavior, and operational readiness as build concerns when applicable, not post release advice.
12. Do not silently skip a required gate. A Blueprint gate outcome is pass, rework, approved exception, escalate, or stop. PREOS assurance states are GREEN, AMBER, RED, HUMAN REVIEW, and UNKNOWN. UNKNOWN never silently becomes GREEN.
13. AI may recommend. Human accountable owners approve major scope, legal and compliance interpretation, security or privacy risk acceptance, destructive operations, production deployment, payments, external spending, user communications, and final launch.
14. Do not broaden an approved implementation packet into adjacent cleanup, speculative hardening, new features, or architecture changes without a new approved packet.
15. Require independent review and applicable QA before launch scope work is treated as complete.
16. If source artifacts conflict, stop the affected work and surface the conflict rather than inventing a resolution.
17. Do not duplicate PREOS canonical risk/control/readiness corpora in this repository. Their authoritative implementation lives in `WilsonMisor/PREOS`; this repository stores only the integration contract and routing.

## Project classification

Before planning or coding, read `orchestration/project-classification.md` and create a Project Classification Record. At minimum identify:

1. Product type and business model.
2. User groups and privileged roles.
3. Delivery surfaces, including browser, WordPress, mobile, API, background workers, data pipelines, and administrative tools.
4. Data sensitivity and compliance triggers.
5. Tenant model if SaaS is present.
6. Identity and authorization model.
7. External integrations and payment dependencies.
8. Hosting and deployment constraints.
9. Production intent and expected blast radius.
10. Required profiles.
11. Explicitly excluded profiles.
12. PREOS assurance level and maturity stage.
13. Accountable production/risk owner and known role gaps when PREOS is active.

Then apply `orchestration/profile-routing.md` and `orchestration/preos-routing.md` when PREOS is active.

## Profile inheritance and assurance overlay

Use this default inheritance model.

```text
Core
  Web
    WordPress
  SaaS
    Web when browser UI exists
    API when programmatic services exist
    Data when persistent application data exists
    Infrastructure for production operation
  Mobile
    API when remote services exist
    Data contracts when shared entities exist
    Infrastructure for production services
  API
    Data when persistence exists
    Infrastructure for production operation

PREOS production assurance overlays any applicable combination above.
```

Profile inheritance does not mean load every file. Load the minimum references needed for the current phase and task. PREOS likewise selects only relevant risks and readiness questions rather than loading its entire catalogue into every Codex context.

## Lifecycle

Use `references/core/lifecycle.md` as the master state machine and `orchestration/preos-routing.md` for production-assurance transitions.

The normal integrated sequence is:

1. Discovery and problem definition.
2. Product definition and scope.
3. PRD baseline.
4. Project classification, profile activation, and PREOS assurance classification.
5. When PREOS is active, create/refresh the PREOS Project Contract and perform the first product/classification risk pass.
6. Architecture, data, API, threat, privacy, environment, and architecture-economics planning as applicable.
7. Perform the architecture-dependent PREOS risk pass and update the Deferred Complexity Registry where applicable.
8. UX and design strategy and approval for user facing work.
9. SRS and SRD baseline.
10. Traceability and test planning.
11. For each substantial change, run PREOS change-impact/risk delta when active and create one bounded AI Task Packet enriched by PREOS requirements.
12. Implementation by Codex under the approved packet.
13. Self review and independent review.
14. Security and specialist review where triggered, including gstack specialists routed by the Blueprint/PREOS evidence need.
15. Automated, integration, device, browser, contract, accessibility, performance, failure, recovery, reconciliation, and capacity testing as applicable.
16. UAT and launch readiness.
17. When PREOS is active, evaluate G0-G11 production assurance and evidence/authority state.
18. Accountable human production approval.
19. Deployment and verification, including canary/staged verification when selected.
20. Hypercare, monitoring, incident handling, maintenance, cost/reliability review, PREOS production learning, gstack retrospective, and Blueprint change control.

## Mandatory core artifacts

For a substantial project, create or verify the applicable artifacts below. Mark an artifact not applicable only with a reason.

1. Project Charter or Discovery Record.
2. Project Classification Record.
3. Approved PRD.
4. SRS where system requirements need formal separation from product intent.
5. SRD with build level requirements.
6. Architecture Decision Records.
7. Canonical Domain Model and contract map when data crosses components or clients.
8. Threat Model and Security Control Matrix.
9. Privacy and data handling record when personal or sensitive data exists.
10. UX and design evidence for user facing scope.
11. Environment and deployment plan.
12. Test Strategy and Test Plan.
13. Traceability Matrix.
14. AI Task Packets.
15. AI Run or Change Evidence for consequential work.
16. Release Checklist and rollback plan.
17. Operations and handoff documentation.
18. When PREOS is active: hash-bound Project Contract, relevant risk/control assessments, architecture-economics/deferred-complexity evidence, evidence-freshness state, risk acceptances if any, and applicable G0-G11 gate evidence.

Templates live in `templates/`. PREOS-specific canonical schemas/templates remain in the PREOS repository; do not create drifting duplicate sources here.

## Cross platform contract rule

When web, mobile, API, workers, integrations, or data services share a business entity or action, define one canonical contract before separate implementations proceed. Follow `orchestration/cross-platform-routing.md`.

Canonical contracts must cover, as applicable:

1. Entity names and field semantics.
2. Identifiers and ownership.
3. Date, time, timezone, money, currency, enumeration, and nullability semantics.
4. Validation rules.
5. Authorization requirements.
6. API request and response contracts.
7. Event and webhook contracts.
8. Error contracts.
9. Versioning and compatibility.
10. Audit and observability requirements.

Do not allow clients to invent conflicting representations without an explicit Architecture Decision Record.

## PREOS production assurance

When PREOS is active, read `orchestration/preos-routing.md` and `references/production-assurance/preos-integration.md`.

PREOS is responsible for production-assurance analysis and evidence, including:

1. deterministic baseline controls;
2. contextual and catalogue production risks;
3. production-readiness questions;
4. architecture economics and complexity tax;
5. Deferred Complexity activation triggers;
6. control dependencies;
7. evidence freshness and invalidation;
8. change impact;
9. risk aggregation and risk acceptance;
10. G0-G11 production assurance;
11. post-production learning.

The PREOS Project Contract is a compiled hash/version-bound snapshot of approved governing artifacts. It does not become a second PRD/SRS/SRD or architecture source of truth.

PREOS runtime/recovery state belongs under `PREOS_STATE_ROOT`. Project-specific version-controlled assurance artifacts belong under `.ai-product-delivery/preos/` in the application repository. Do not place PREOS authoritative state under `.gstack` or `GSTACK_STATE_ROOT`.

PREOS cannot authorize production by itself and cannot impersonate a missing accountable human role. Missing authority becomes a role gap and HUMAN REVIEW.

## WordPress preservation rule

The existing WordPress blueprint and its references are authoritative for deep WordPress delivery. The new WordPress profile points to those files and adds profile wrappers for classic themes, custom plugins, third party plugins, CPTs, custom fields, media, security, SEO, performance, QA, and deployment.

Never weaken the existing requirements for:

1. Classic theme and code first delivery where the project requires it.
2. Owner approved design baseline before main theme or template coding.
3. Human Design Governance and anti generic AI design review.
4. Purpose built CPT administration instead of default block editing where required.
5. Cybersecurity by design.
6. Full site SEO crawl and remediation.
7. Traceability, task packets, human approvals, QA, and launch evidence.

## SaaS hard gates

When SaaS is active, read `references/saas/saas-lifecycle.md` and the relevant SaaS references. Treat these as hard concerns when triggered:

1. Tenant definition and tenant context propagation.
2. Tenant isolation across database, cache, files, jobs, search, logs, analytics, and administrative tooling.
3. Authentication, authorization, RBAC or ABAC, and row level security where selected.
4. Organisation, team, invitation, account, suspension, deletion, and retention lifecycles.
5. Plans, entitlements, billing, subscriptions, payments, webhooks, retries, and idempotency.
6. Rate limiting, abuse protection, feature flags, notifications, background jobs, queues, and dead letter handling.
7. Audit logging, backups, restore testing, observability, scaling, and disaster recovery.

Cross tenant data exposure is a hard failure unless the access is an explicitly designed privileged administrative operation with authorization and audit controls.

## Mobile hard gates

When mobile is active, read `references/mobile/mobile-lifecycle.md` and the relevant mobile references. Address:

1. Mobile architecture and Flutter conventions when Flutter is used.
2. State, navigation, API integration, authentication, secure storage, and local persistence.
3. Offline behaviour, synchronization, conflict handling, network loss, and retries.
4. Permissions, deep links, notifications, background execution, and device capabilities.
5. Accessibility, performance, crash reporting, analytics, and device testing.
6. Signing, build variants, Android and iOS release, staged rollout, store compliance, upgrade policy, and rollback or mitigation.

## gstack routing

Read `orchestration/gstack-routing.md` when gstack is available. When PREOS is active, PREOS identifies assurance needs and the Blueprint routes those needs to the appropriate specialist; gstack does not become the assurance authority.

Default specialist routing is:

1. Discovery and problem reframing, gstack office hours.
2. Product scope challenge, gstack CEO review.
3. Architecture and failure mode review, gstack engineering review.
4. Design planning and design quality review, gstack design specialists.
5. Security review, gstack CSO.
6. Implementation, Codex under an approved AI Task Packet.
7. Code review, gstack review plus Blueprint/PREOS acceptance criteria.
8. Root cause debugging, gstack investigate.
9. QA, gstack QA plus Blueprint/PREOS test/evidence requirements.
10. Performance evidence, gstack benchmark when required.
11. Release, Blueprint release gate plus PREOS assurance plus gstack ship.
12. Deployment/canary execution, gstack land-and-deploy/canary only after accountable authorization.
13. Post release reflection, PREOS production learning plus gstack retro plus Blueprint change control.

A gstack recommendation does not override a hard Blueprint or PREOS requirement. Conflicts require explicit human resolution.

## Stop conditions

Stop or escalate the affected work when any of the following is unresolved:

1. Conflicting or missing governing requirements.
2. Missing required project classification, profile decision, or PREOS assurance classification.
3. Missing approval for a hard gate.
4. Unresolved critical or high security finding.
5. Broken authentication, authorization, tenant isolation, or secret handling.
6. Unsafe destructive migration or data operation.
7. Unapproved design baseline for launch scope UI when design approval is required.
8. Missing test evidence for a critical path.
9. Failed migration, rollback, restore, recovery, or reconciliation test where required.
10. Unknown legal, privacy, accessibility, payment, tax, or regulatory interpretation that materially changes implementation.
11. Production access or deployment without the required accountable approval.
12. Unsupported factual claims or invented external system behaviour.
13. PREOS source-integrity failure, stale Project Contract, invalid risk acceptance, or required RED/HUMAN REVIEW/UNKNOWN assurance condition.
14. Required evidence that became stale after a material source/code/configuration/environment change.
15. Missing accountable human authority for a consequential risk decision.

## Reference loading

Start with `references/INDEX.md`, `orchestration/project-classification.md`, and `orchestration/profile-routing.md`. When PREOS is active, also load `orchestration/preos-routing.md` and `references/production-assurance/preos-integration.md`.

Read core modules for the current phase. Then read only active profile modules. Use `templates/` when producing project artifacts. Use the existing root WordPress references when the WordPress profile points to them. Use PREOS selective risk/readiness tooling rather than loading its entire source corpus into every task.

The goal is complete governance with bounded context, not maximum context loading.
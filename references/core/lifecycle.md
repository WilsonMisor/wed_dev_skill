# Core Product Delivery Lifecycle

This is the master state machine for substantial projects. When PREOS production assurance is active, apply `orchestration/preos-routing.md` as an assurance overlay on this lifecycle rather than creating a separate competing delivery lifecycle.

When project truth arrives as a mixed document package, ZIP, existing repository, brownfield codebase, or ambiguous set of historical/current sources, run `orchestration/source-intake.md` before discovery. Do not force a separate intake artifact when approved source authority is already unambiguous.

## States

1. Governed source intake when required: safe inspection, source inventory/hashes, source authority, duplicate/supersession/conflict detection, and source requirement/architecture/stack extraction.
2. Discovery.
3. Product definition.
4. PRD baseline.
5. Project classification, including PREOS assurance level and maturity stage.
6. PREOS Project Contract and early risk pass when PREOS is active.
7. Architecture and risk design, including architecture economics and deferred-complexity decisions when applicable.
8. Architecture-dependent PREOS risk pass when active.
9. UX and design baseline when user facing scope exists.
10. SRS and SRD baseline.
11. Traceability and test planning.
12. PREOS change-impact/risk-delta assessment for the planned change when active.
13. AI Task Packet preparation, enriched by PREOS rather than replaced by a second implementation-unit artifact.
14. Implementation.
15. Review.
16. Verification and QA, including failure, recovery, reconciliation, performance/capacity, and evidence-freshness checks when required.
17. UAT and launch readiness.
18. PREOS G0-G11 production-assurance evaluation when active.
19. Accountable human production approval.
20. Deployment and verification.
21. Hypercare.
22. Operations and maintenance.
23. PREOS production learning and gstack retrospective when applicable.
24. Blueprint controlled change.

## Transition rule

Each state records required inputs, work allowed, evidence, accountable owner, gate result, and next state. Blueprint gate results are pass, rework, approved exception, escalate, or stop.

PREOS assurance states are GREEN, AMBER, RED, HUMAN REVIEW, and UNKNOWN. UNKNOWN never silently becomes GREEN, and absence of evidence does not count as evidence of safety.

Do not move forward with unresolved hard failures. Rework returns to the earliest affected baseline rather than patching downstream artifacts only.

A required PREOS RED, unresolved HUMAN REVIEW, or material UNKNOWN prevents a production pass unless an allowed, documented risk-acceptance path is approved by an accountable human authority.

## AI-session interruption rule

Read `references/core/session-continuity.md` for interrupted AI-assisted implementation. Conversation memory is never authoritative execution state. If a production-relevant implementation session is interrupted, do not continue from chat recollection or gstack context alone. PREOS must reconcile its runtime state under `PREOS_STATE_ROOT` with the Project Contract, task packet, Git, source bindings, approvals, evidence, and actual verification state. Resume only from the first unverified action after `SAFE_TO_RESUME`; stop on `BLOCKED` or `RECOVERY_CONFLICT`.

## Change rule

A material requirement, architecture, code, configuration, dependency, schema, environment, authoritative source, or operational change after baseline must trigger impact analysis across design, data, API, clients, tests, security, deployment, documentation, PREOS risks/controls, evidence freshness, monitoring, recovery/reconciliation, and affected production gates before implementation continues.

Accepted production learning returns through this same controlled-change mechanism rather than silently mutating requirements or architecture.

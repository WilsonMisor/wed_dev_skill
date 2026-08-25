# Core Product Delivery Lifecycle

This is the master state machine for substantial projects. When PREOS production assurance is active, apply `orchestration/preos-routing.md` as an assurance overlay on this lifecycle rather than creating a separate competing delivery lifecycle.

## States

1. Intake.
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

## Change rule

A material requirement, architecture, code, configuration, dependency, schema, environment, or operational change after baseline must trigger impact analysis across design, data, API, clients, tests, security, deployment, documentation, PREOS risks/controls, evidence freshness, monitoring, recovery/reconciliation, and affected production gates before implementation continues.

Accepted production learning returns through this same controlled-change mechanism rather than silently mutating requirements or architecture.
# Core Product Delivery Lifecycle

This is the master state machine for substantial projects.

## States

1. Intake.
2. Discovery.
3. Product definition.
4. PRD baseline.
5. Project classification.
6. Architecture and risk design.
7. UX and design baseline when user facing scope exists.
8. SRS and SRD baseline.
9. Traceability and test planning.
10. AI task packet preparation.
11. Implementation.
12. Review.
13. Verification and QA.
14. UAT and launch readiness.
15. Deployment.
16. Hypercare.
17. Operations and maintenance.
18. Retrospective and controlled change.

## Transition rule

Each state records required inputs, work allowed, evidence, accountable owner, gate result, and next state. Gate results are pass, rework, approved exception, escalate, or stop.

Do not move forward with unresolved hard failures. Rework returns to the earliest affected baseline rather than patching downstream artifacts only.

## Change rule

A material requirement or architecture change after baseline must trigger impact analysis across design, data, API, clients, tests, security, deployment, and documentation before implementation continues.

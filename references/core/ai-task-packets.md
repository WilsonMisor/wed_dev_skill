# AI Task Packets

Use an AI Task Packet to bound non trivial implementation and consequential AI work.

The integrated system has one implementation work unit: the Blueprint AI Task Packet. PREOS may enrich the packet with production-assurance fields, but it must not create a competing implementation-unit truth.

## Required fields

1. Packet ID.
2. Owner.
3. Goal.
4. Non goals.
5. Source artifacts and baseline versions/hashes.
6. Requirement IDs.
7. Architecture and design constraints.
8. Data, API, security, privacy, and accessibility constraints as applicable.
9. Allowed files, directories, systems, tools, and environments.
10. Prohibited actions.
11. Data handling restrictions.
12. Acceptance criteria.
13. Required automated and manual checks.
14. Required evidence.
15. Reviewer.
16. Approver.
17. Rollback, migration, or handoff notes.

## PREOS extension when production assurance is active

Add the following fields when applicable:

1. PREOS assurance level and maturity stage.
2. PREOS Project Contract version/hash.
3. Relevant PREOS risk IDs.
4. Relevant deterministic baseline/control IDs.
5. Control dependencies that affect this packet.
6. Applicable G0-G11 production gates.
7. Required success-path tests and explicit failure tests.
8. Evidence bindings and freshness/invalidation conditions.
9. Required monitoring and operational signals.
10. Recovery, rollback, repair, and reconciliation requirements.
11. Economic impact, cost driver, or economic-abuse concerns.
12. Deferred Complexity Registry entries or activation triggers affected by the change.
13. Change-impact results, including existing evidence that becomes stale.
14. Accountable human risk owner where consequential risk exists.
15. Risk acceptance reference when an approved exception exists.

Not every PREOS field applies to every packet. Omit only with an applicability rationale when the concern would otherwise reasonably be expected.

## Traceability expectation

For critical production behaviour, preserve the applicable chain from requirement to risk, control, ADR, packet, code/configuration, tests, evidence, monitoring, recovery/reconciliation, and production gate.

## Execution discipline

If a packet is internally inconsistent, missing a hard prerequisite, contains stale governing sources, requires work outside allowed scope, or conflicts with a PREOS RED/UNKNOWN/HUMAN REVIEW condition that blocks the task, stop and surface the issue. Do not silently expand the packet or convert missing evidence into approval.
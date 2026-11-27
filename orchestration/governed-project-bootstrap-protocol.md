# Governed Codex Project Bootstrap Protocol

This is an entry protocol into implemented governance. It is not permission to invent missing framework state.

## Phase A. Repository and instruction discovery

1. Establish repository root, current branch, HEAD, working tree and remotes. Do not modify files.
2. Enumerate applicable `AGENTS.md` or overrides in Codex precedence order.
3. Locate the governing Blueprint skill through Codex skill discovery. Do not guess a path.
4. Read the pinned integration manifest and verify Blueprint, PREOS, gstack, virtual-team registry and schema versions.
5. On mismatch return `COMPATIBILITY_FAILURE`.

## Phase B. State recovery and source authority

6. Locate authoritative project state. If existing state cannot be reconciled with Git and PREOS runtime state, run deterministic recovery and do not resume coding.
7. Inventory authoritative project sources and hashes. Resolve precedence using Blueprint rules. Conflicts become `SOURCE_CONFLICT`.
8. Determine project classification and activate only applicable delivery profiles.
9. Determine PREOS assurance level and risk corpus version from the Project Contract.

## Phase C. Virtual-team and assurance routing

10. Use the deterministic role router. Do not manually invent roles.
11. Load only the selected canonical role cards. Noncanonical labels must resolve through `role-reference-resolution.json`; unresolved labels become `ROLE_GAP`.
12. Use PREOS selectors to load bounded applicable risks and readiness checks. Never load all 4,337 risks for ordinary implementation.
13. Evaluate PREOS G0-G11 super-gates and applicable R0-R17 readiness sub-gates.

## Phase D. Task authorization

14. Identify the exact lifecycle state and next permissible transition.
15. Create or validate a bounded AI Task Packet with requirement IDs, ADR IDs, allowed files, prohibited actions, applicable roles, risk IDs, acceptance criteria, tests, evidence, rollback, reviewer and approver.
16. Missing required fields block implementation.
17. Verify recorded approval when approval is required. Never infer approval from document existence or successful tests.

## Phase E. Implementation and evidence

18. Use an isolated branch or worktree for substantial changes.
19. A single controlled writer implements only the approved packet. Parallel agents should generally remain read-heavy unless file ownership is explicitly disjoint.
20. Run self-review, independent specialist review, required tests and PREOS evidence capture.
21. Reevaluate gates after implementation. `UNKNOWN` never becomes `GREEN` without evidence.

## Phase F. Release boundary

22. Shipping, mergeability, deployment tooling and green tests do not equal production authority.
23. Without required accountable human approval, the maximum state is `READY_FOR_HUMAN_PRODUCTION_DECISION`.
24. After authorized release, execute health checks, canary/staged verification where required, rollback readiness and production learning.

## Mandatory initialization report

Before substantial implementation, report repository identity, active instructions, pinned framework versions, compatibility result, project classification, profiles, lifecycle state, Project Contract, selected roles, selected PREOS risks, current gates, current Task Packet, approval state, evidence freshness, blockers and next permissible action. Every consequential claim must cite an authoritative repository artifact.

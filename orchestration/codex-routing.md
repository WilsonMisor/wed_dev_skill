# Codex Routing

Codex is the primary implementation engine under this blueprint.

## Responsibility boundary

The application repository is the execution surface for product code and project specific artifacts. The AI Product Delivery Blueprint remains the governance source, and gstack remains a specialist tool or skill installation when used.

Do not merge or vendor the blueprint repository or gstack repository into an application repository merely to make the layers cooperate. Prefer installed skill invocation, namespaced gstack commands, approved project artifacts, AI Task Packets, and explicit handoffs. Copy or vendor another layer only when an approved architecture decision gives a concrete reason, owner, versioning strategy, update strategy, and rollback plan.

Codex may read governance and specialist output, but it must implement inside the intended target repository and preserve that repository's architecture and conventions.

## Source control safety

For substantial AI generated changes:

1. Do not perform the work directly on a protected baseline branch such as `main` when an isolated branch, worktree, or fork is available.
2. Create or use an isolated branch, worktree, or fork from the intended baseline.
3. Keep unrelated changes out of the implementation scope.
4. Run required checks before integration.
5. Prefer a pull request or equivalent review boundary before merging into the protected baseline.
6. Do not treat merge approval as production deployment approval.
7. Never force update a protected branch or bypass required review unless an accountable human explicitly authorises the exceptional action and its risk.

## Before implementation

Require an approved AI Task Packet for non trivial work. The packet must identify source requirements, architecture constraints, allowed scope, prohibited scope, acceptance criteria, tests, evidence, reviewer, approver, and rollback or handoff expectations.

## During implementation

1. Read only the references needed for the packet.
2. Inspect existing code and contracts before editing.
3. Preserve naming, folder, schema, API, and environment conventions unless the packet explicitly changes them.
4. Make the smallest coherent change that satisfies the packet.
5. Do not introduce packages, services, tables, endpoints, permissions, environment variables, or architectural layers without a requirement or documented engineering reason.
6. Update tests and documentation required by the change.
7. Record deviations and unresolved risks.

## After implementation

Run applicable automated checks, self review against acceptance criteria, then route to independent review and QA. Do not mark launch scope work complete because code compiles or a local happy path works.
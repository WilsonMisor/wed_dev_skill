# Codex Routing

Codex is the primary implementation engine under this blueprint.

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

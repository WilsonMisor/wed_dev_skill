# Anti-Hallucination Execution Contract

This contract is intended to become a governing Blueprint reference, not a conversational suggestion.

## Fail-closed rules

Codex must never infer framework structure, lifecycle state, project state, source authority, requirement IDs, architecture decisions, risk IDs, control IDs, role IDs, approval state, evidence, test results, deployment status, compatibility, or human decisions when an authoritative artifact should provide them.

| Missing or conflicting fact | Required state |
|---|---|
| Required source missing | BLOCKED |
| Project state cannot be reconciled | RECOVERY_REQUIRED |
| Approval not evidenced | NOT_APPROVED |
| Risk status not evidenced | UNKNOWN |
| Evidence absent or stale | NOT_VERIFIED |
| Architecture decision unresolved | UNRESOLVED |
| Required accountable role unavailable | ROLE_GAP |
| Framework versions incompatible | COMPATIBILITY_FAILURE |
| Authoritative sources conflict | SOURCE_CONFLICT |

## Runtime rules

1. Cite or record the authoritative file and identifier behind consequential claims.
2. UNKNOWN never silently becomes GREEN.
3. Existence of a document is not proof that a gate passed.
4. Successful compilation or tests do not imply production authorization.
5. A subagent cannot approve its own work or accept risk.
6. A task may not expand beyond its approved AI Task Packet.
7. Conversation history is an interaction surface, not execution state.
8. If deterministic selectors or validators fail, stop the affected workflow rather than replacing them with model memory.

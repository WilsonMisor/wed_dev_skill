# Reconciled Production-Engine Upgrade Ownership and Traceability

This is the Phase 1/2 reconciliation register for the abandoned gstack `project-init` / `production-implement` design and the current three-repository architecture. It prevents a useful requirement from disappearing merely because ownership changed.

Disposition vocabulary: `KEEP`, `ALREADY_IMPLEMENTED`, `MOVE_TO_BLUEPRINT`, `MOVE_TO_PREOS`, `KEEP_IN_GSTACK`, `STRENGTHEN`, `REPLACE_WITH_CURRENT_ARCHITECTURE`, `RETIRE_AS_OBSOLETE`.

| Original requirement / capability | Original owner | Disposition | Final owner | Target module / artifact | Implementation status | Proving test / evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `project-init` | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | Blueprint + PREOS | Blueprint source intake -> `preos-project-init` | Implemented split | `tests/test_source_intake.py`; PREOS integration validator |
| Folder input | gstack | MOVE_TO_BLUEPRINT | Blueprint | `scripts/source_intake.py` | Implemented | directory inventory test |
| ZIP input | gstack | MOVE_TO_BLUEPRINT | Blueprint | `scripts/source_intake.py` | Implemented | ZIP tests |
| Repository input | gstack | MOVE_TO_BLUEPRINT | Blueprint | directory/repository intake | Implemented | brownfield evidence test |
| Greenfield/brownfield | gstack | MOVE_TO_BLUEPRINT | Blueprint | source-intake project mode | Implemented | greenfield/brownfield tests |
| Hybrid/migration/unknown mode | gstack | MOVE_TO_BLUEPRINT | Blueprint | governed `--project-mode` | Implemented | governed enum validation |
| SHA-256 inventory | gstack | MOVE_TO_BLUEPRINT | Blueprint | source manifest | Implemented | duplicate/hash tests |
| Never execute untrusted sources merely for intake | gstack | MOVE_TO_BLUEPRINT | Blueprint | `orchestration/source-intake.md` | Implemented | validator semantic anchors + code inspection |
| Safe archive extraction | gstack | MOVE_TO_BLUEPRINT | Blueprint | ZIP staging | Implemented | positive safe-ZIP/original-preservation test + traversal/absolute/symlink/reparse checks |
| Source authority map | gstack | MOVE_TO_BLUEPRINT | Blueprint | governed `source_decisions` | Implemented | authority tests |
| Duplicate detection | gstack | MOVE_TO_BLUEPRINT | Blueprint | SHA-256 duplicate groups | Implemented | duplicate test |
| Version detection | gstack | MOVE_TO_BLUEPRINT | Blueprint | non-authoritative version-candidate groups | Implemented | version-candidate test |
| Superseded-source detection | gstack | MOVE_TO_BLUEPRINT | Blueprint | explicit `supersedes` / `superseded_by` | Implemented | supersession test |
| Source conflicts | gstack | MOVE_TO_BLUEPRINT | Blueprint | conflict groups | Implemented | resolved + blocking conflict tests |
| Requirement extraction | gstack | MOVE_TO_BLUEPRINT | Blueprint | governed source requirements / `SRCREQ-*` | Implemented deterministic binding | stable requirement-ID test |
| Architecture extraction | gstack | MOVE_TO_BLUEPRINT | Blueprint | observed/declared/approved architecture | Implemented extraction contract | explicit observed/declared/approved architecture test + validator |
| Stack extraction | gstack | MOVE_TO_BLUEPRINT | Blueprint | observed/declared/approved stack | Implemented extraction contract | explicit observed/declared/approved stack test + validator |
| Intake unknowns/assumptions/role gaps | gstack | MOVE_TO_BLUEPRINT | Blueprint | intake record | Implemented | unknown-handling test |
| Project Contract | gstack | MOVE_TO_PREOS | PREOS | `preos-project-init` / Project Contract schema | Existing canonical owner preserved | PREOS Project Contract tests |
| Source drift | gstack | STRENGTHEN | Blueprint + PREOS | source hashes + change impact/evidence freshness | Implemented deterministic detection + PREOS change-impact contract | authoritative source-hash drift test + Blueprint validator + PREOS recovery drift test |
| Human source-resolution gate | gstack | MOVE_TO_BLUEPRINT | Blueprint / human authority | source conflict stop condition | Implemented | blocking conflict test |
| Application `AGENTS.md` continuity rule | new integrated requirement | MOVE_TO_BLUEPRINT | Blueprint | `templates/application-agents-continuity.md` | Implemented | Blueprint validator |
| `production-implement` | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | PREOS + Codex | `preos-production-plan` -> AI Task Packet -> Codex -> `preos-production-implement` | Implemented routing | PREOS/gstack integration validators |
| Approved contract required | gstack | MOVE_TO_PREOS | PREOS | Project Contract binding | Implemented | recovery binding tests |
| Approved plan required | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | Blueprint | canonical approved AI Task Packet | Existing + strengthened routing | Blueprint validator |
| Branch/repository verification | gstack | MOVE_TO_PREOS | PREOS | deterministic Git snapshot/recovery | Implemented | PREOS recovery tests |
| 75-control classification | gstack | MOVE_TO_PREOS | PREOS | canonical 75-control baseline | Existing canonical owner preserved | baseline validator/tests |
| Applicability semantics | gstack | MOVE_TO_PREOS | PREOS | APPLIES/CONDITIONAL/NOT_APPLICABLE/ESCALATE/FORBIDDEN | Governed by PREOS | PREOS semantic validation |
| WordPress overlay | gstack | MOVE_TO_PREOS | PREOS | `references/wordpress/wordpress-75-control-overlay.md` | Implemented | 75/75 overlay test |
| Non-WordPress handling | gstack | MOVE_TO_PREOS | PREOS | canonical controls selected by active Blueprint profiles | Existing + preserved | PREOS risk/control routing |
| Seven legacy implementation gates | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | PREOS | compatibility map to G0-G11 | Implemented | PREOS validator |
| Implementation Units | gstack | RETIRE_AS_OBSOLETE | Blueprint | canonical AI Task Packet | Folded into existing object | Blueprint task-packet validation |
| Change impact | gstack | MOVE_TO_PREOS | PREOS | change impact/risk delta | Existing + preserved | PREOS validation/tests |
| Human gates | gstack | MOVE_TO_PREOS | PREOS + human authority | approval state / G11 | Strengthened | approval/recovery tests |
| Small coherent coding | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | Codex under Blueprint packet | Codex routing | Existing | Blueprint Codex-routing validator |
| Tests with code | gstack | REPLACE_WITH_CURRENT_ARCHITECTURE | Codex + PREOS | packet acceptance/evidence | Existing + strengthened | repository suites |
| Incremental verification | gstack | MOVE_TO_PREOS | PREOS | checkpoints / evidence | Strengthened | checkpoint/recovery tests |
| Self-attack | gstack | KEEP_IN_GSTACK | gstack + Codex review | review/CSO/QA routes | Existing | gstack regression suite |
| Evidence package | gstack | MOVE_TO_PREOS | PREOS | evidence index/freshness | Strengthened | evidence freshness tests |
| No implementation self-production-approval | gstack | STRENGTHEN | PREOS + human authority | approval boundary | Strengthened | authority tests + gstack validator |
| Semantic context continuity | gstack | KEEP_IN_GSTACK | gstack | context-save/context-restore | Existing; integrated as supplementary only | gstack context tests + integration validator |
| Deterministic runtime continuity | gstack | MOVE_TO_PREOS | PREOS | `PREOS_STATE_ROOT` runtime engine | Implemented | PREOS recovery tests |
| Soft checkpoints | gstack | MOVE_TO_PREOS | PREOS | `checkpoint-state.py --kind soft` | Implemented | checkpoint tests |
| Hard checkpoints | gstack | MOVE_TO_PREOS | PREOS | `checkpoint-state.py --kind hard` | Implemented | hard-checkpoint tests |
| Event-based checkpointing | gstack | MOVE_TO_PREOS | PREOS | checkpoint event/ledger | Implemented | checkpoint tests |
| Atomic runtime writes | new integrated requirement | MOVE_TO_PREOS | PREOS | `runtime_state.py` | Implemented | atomic-write tests |
| Append-only implementation ledger | gstack | MOVE_TO_PREOS | PREOS | `implementation-ledger.jsonl` | Implemented / strengthening | ledger tests |
| Git reconciliation | gstack | MOVE_TO_PREOS | PREOS | repo/branch/HEAD/tree fingerprint | Implemented | recovery matrix |
| Source-hash reconciliation | gstack | MOVE_TO_PREOS | PREOS | Project Contract source bindings | Implemented | source-drift recovery test |
| Project Contract reconciliation | gstack | MOVE_TO_PREOS | PREOS | hash binding | Implemented | contract mismatch test |
| Task-packet reconciliation | gstack | MOVE_TO_PREOS | PREOS | task-packet hash binding | Implemented | task mismatch test |
| Evidence reconciliation | gstack | MOVE_TO_PREOS | PREOS | evidence index/freshness | Implemented | stale-evidence test |
| Pending approval survives restart | gstack | MOVE_TO_PREOS | PREOS | `approval-state.json` | Implemented | fresh-process restart test |
| Recovery conflict | gstack | MOVE_TO_PREOS | PREOS | `RECOVERY_CONFLICT` | Implemented | recovery matrix |
| First-unverified-action resume | gstack | MOVE_TO_PREOS | PREOS | `next_unverified_action` | Implemented | recovery matrix |
| Corrupt state/checkpoint handling | gstack | MOVE_TO_PREOS | PREOS | recovery parser | Implemented / strengthening | corruption tests |
| Interrupted test re-run | gstack | MOVE_TO_PREOS | PREOS | pending-test resume pointer | Implemented contract | interruption drill |
| Uncertain migration safety | gstack | MOVE_TO_PREOS | PREOS | recovery conflict / explicit verification | Strengthening in PREOS | interruption drill |
| Planning pipeline | gstack | KEEP_IN_GSTACK | gstack | office-hours / plan reviews / autoplan | Preserved | gstack existing suite |
| Structured plan handoff | gstack | KEEP_IN_GSTACK | gstack | `preos-handoff` + autoplan route | Implemented / integration hardening | gstack integration validator + coverage |
| Specialist request/output contracts | gstack | KEEP_IN_GSTACK | gstack | `PREOS-INTEGRATION.md` | Implemented | integration validator |
| Review | gstack | KEEP_IN_GSTACK | gstack | `review` | Preserved | gstack suite |
| Security review | gstack | KEEP_IN_GSTACK | gstack | `cso` | Preserved | gstack suite |
| QA | gstack | KEEP_IN_GSTACK | gstack | `qa` / `qa-only` | Preserved | gstack suite |
| Benchmark | gstack | KEEP_IN_GSTACK | gstack | `benchmark` | Preserved | gstack suite |
| Ship/deploy/canary | gstack | KEEP_IN_GSTACK | gstack after authority gate | ship / land-and-deploy / canary | Preserved | gstack suite + integration validator |
| Production learning | integrated architecture | MOVE_TO_PREOS | PREOS -> gstack -> Blueprint | production-learn -> retro -> change control | Existing integrated path | integration validators |
| Codex host generation | gstack | KEEP_IN_GSTACK | gstack | host generator | Preserved + new bridge generation | Skill Docs Freshness / host generation CI |
| Windows validation | gstack | KEEP_IN_GSTACK | gstack | Windows Free Tests | Preserved | GitHub Actions |
| Controlled fork/upstream strategy | gstack | KEEP_IN_GSTACK | gstack repository governance | fork/upstream relationship | Preserved | final repository audit |
| No direct main development | integrated architecture | STRENGTHEN | all repositories | protected main + isolated PRs | Enforced | branch/ruleset audit |
| Conversation memory not authoritative | integrated architecture | STRENGTHEN | Blueprint + PREOS + gstack | continuity contracts | Implemented invariant | three-repo semantic audit |

## Non-duplication invariants

There is **one canonical Project Contract**, **one canonical 75-control baseline**, **one canonical AI Task Packet**, **one PREOS production runtime-state authority**, and **one accountable human production-approval boundary**.

The application repository is the product execution surface. Framework repositories remain separate. gstack context is semantic context, not PREOS runtime truth. Conversation memory is never authoritative execution state.

## Release invariant

```text
Blueprint readiness
-> PREOS G0-G11
-> accountable human production approval
-> gstack-ship
-> gstack-land-and-deploy when selected
-> gstack-canary
-> production evidence
-> PREOS production learning
-> gstack-retro
-> Blueprint controlled change
```

No earlier planning, review, code-completion, merge, or deployment capability is production authorization.

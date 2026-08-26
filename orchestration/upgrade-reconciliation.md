# Reconciled Production-Engine Upgrade Ownership

This record prevents requirements from the abandoned gstack `project-init` / `production-implement` design from disappearing during the three-repository integration.

| Original capability | Final owner/disposition |
| --- | --- |
| Folder/ZIP/repository project intake | Blueprint source intake |
| Safe, non-executing inspection | Blueprint source intake |
| SHA-256 source inventory | Blueprint source intake; PREOS binds approved sources later |
| Source authority, duplicates, supersession, conflicts | Blueprint |
| Requirement/architecture/stack extraction | Blueprint |
| Project Contract | PREOS `preos-project-init` |
| Source drift/change impact | Blueprint + PREOS assurance impact |
| Canonical 75 controls | PREOS only |
| WordPress 75-control interpretation | PREOS overlay selected by Blueprint WordPress profile |
| Legacy seven implementation gates | Compatibility view mapped to PREOS G0-G11 |
| Implementation Units | Fold into canonical Blueprint AI Task Packet |
| Production planning | PREOS enriches the canonical AI Task Packet |
| Production coding | Codex under the approved packet |
| Implementation assurance | PREOS `preos-production-implement` |
| Specialist review/security/QA/benchmark | gstack |
| Deterministic runtime state/checkpoints/recovery | PREOS under `PREOS_STATE_ROOT` |
| Semantic session notes | gstack context-save/context-restore, supplementary only |
| Pending approval across restart | PREOS |
| Git/source/evidence reconciliation | PREOS |
| `RECOVERY_CONFLICT` and first-unverified-action resume | PREOS |
| Ship/deploy/canary | gstack after accountable production approval |
| Production learning | PREOS -> gstack retro -> Blueprint controlled change |

## Non-duplication invariants

There is one canonical Project Contract, one canonical 75-control baseline, one canonical AI Task Packet, one PREOS production runtime-state authority, and one accountable human production-approval boundary.

Conversation memory is never authoritative execution state.

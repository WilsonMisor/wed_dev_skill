# Governed Application Continuity Instructions

Use this content in an application's root `AGENTS.md` when the AI Product Delivery Blueprint and PREOS govern the project. Merge it into an existing `AGENTS.md` rather than creating duplicate or conflicting instruction files.

```markdown
## AI Product Delivery continuity

- The AI Product Delivery Blueprint governs lifecycle, source authority, approved application requirements, architecture, canonical AI Task Packets, and controlled change.
- PREOS governs the Project Contract, production assurance, runtime checkpoints, evidence freshness, and deterministic recovery.
- gstack supplies specialist engineering judgment and evidence; it does not own production truth or approval.
- Codex implements only bounded approved AI Task Packets.
- Accountable human authority owns consequential source/product/architecture/risk/legal/financial decisions and production authorization.

Conversation memory is never authoritative execution state.

If implementation was interrupted, do not simply continue from the last conversational topic. Reconcile PREOS runtime state with the application repository, Git branch/HEAD/working tree, Project Contract and source hashes, current AI Task Packet, persisted approvals, evidence freshness, and any uncertain test/build/migration state. Resume implementation only after PREOS returns `SAFE_TO_RESUME`, and resume from its first unverified action. `BLOCKED` preserves the pending prerequisite. `RECOVERY_CONFLICT` stops implementation until the conflict is reconciled.

Runtime recovery state belongs under `PREOS_STATE_ROOT`; version-controlled application truth belongs under `.ai-product-delivery/`; gstack context remains supplementary semantic context.
```

Do not put secrets, production credentials, private runtime state, or transient conversational summaries into `AGENTS.md`.
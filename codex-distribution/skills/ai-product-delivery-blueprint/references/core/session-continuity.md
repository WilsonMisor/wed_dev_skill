# AI Session Continuity and Recovery Contract

AI-assisted development must survive loss of the AI session itself.

## Governing doctrine

**Conversation memory is never authoritative execution state.**

A previous chat, Codex recollection, gstack context note, or unverified checkpoint may help explain intent but cannot by itself prove that implementation is safe to resume or that an approval occurred.

## Four continuity layers

1. **Blueprint project truth** — version-controlled approved source authority, requirements, architecture, lifecycle state, task packets, approvals, and change-control artifacts under `.ai-product-delivery/`.
2. **PREOS deterministic execution truth** — production implementation runtime/recovery state under `PREOS_STATE_ROOT`, including pipeline/current state, ledger, approvals, evidence index, checkpoints, and recovery events.
3. **External factual truth** — Git branch/HEAD/working tree, CI, deployment environment, database, monitoring, logs, billing and vendor systems.
4. **gstack semantic context** — useful working-session notes about what was discussed or reviewed, but never a replacement for PREOS/Git reconciliation.

## Interruption rule

Treat context-window exhaustion, Codex crash, terminal closure, network interruption, PC restart, deliberate stop, partial implementation, partial test, partial migration, or interruption while awaiting approval as an `INTERRUPTED` execution state.

Before production-relevant implementation resumes, PREOS must reconcile durable state with actual Git/project/evidence/approval reality. Valid recovery outcomes are `SAFE_TO_RESUME`, `BLOCKED`, or `RECOVERY_CONFLICT`.

A new session resumes from the **first unverified action**, not from the last conversational topic.

## Authority persistence

Pending human approvals remain pending across session loss. No model may infer approval from tone, prior conversation, a context summary, or the fact that code exists.

## Conflict precedence

When continuity sources disagree:

- approved Blueprint/Project Contract truth beats conversational recollection;
- actual Git/external state beats a stale checkpoint claim;
- PREOS recovery determines whether production implementation may resume;
- gstack context is explanatory only.

If reconciliation cannot establish a safe state, enter `RECOVERY_CONFLICT` and stop coding until the conflict is resolved.

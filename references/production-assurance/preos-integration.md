# PREOS Integration Contract

PREOS is the production assurance plane for the AI Product Delivery Blueprint. Its canonical implementation and source corpus live in the separate `WilsonMisor/PREOS` repository. This Blueprint repository contains only the governance contract and routing required to activate PREOS correctly.

## What remains authoritative here

The Blueprint remains authoritative for:

1. product and system baselines;
2. project classification and active profiles;
3. architecture governance and ADRs;
4. UX/design approval requirements;
5. bounded AI Task Packets;
6. human approval gates;
7. release and change-control decisions.

PREOS may identify a problem with these artifacts, but it does not silently replace them.

## What PREOS owns

PREOS owns the reusable production-assurance methodology and canonical source corpus for:

1. the deterministic 75-control baseline;
2. the atomic production-risk catalogue;
3. the production-readiness question bank;
4. risk generation and contextual risk selection;
5. architecture economics and deferred complexity;
6. G0-G11 production assurance gates;
7. control-dependency semantics;
8. evidence freshness and invalidation;
9. risk aggregation and release risk;
10. risk-acceptance lifecycle;
11. production learning and evolution.

Do not duplicate those canonical corpora inside this repository.

## Integrated runtime contract

When PREOS is activated, the expected relationship is:

```text
Human authority
      |
AI Product Delivery Blueprint
      |
    PREOS
      |
  +---+---+
  |       |
gstack  Codex
  |       |
  +---+---+
      |
Application repository
      |
Production runtime
      |
telemetry / incidents / cost / support
      |
PREOS learning
      |
Blueprint change control
```

## Installed skill contract

The expected PREOS skills are namespaced:

- `preos-project-init`;
- `preos-risk-model`;
- `preos-architecture-economics`;
- `preos-production-plan`;
- `preos-production-implement`;
- `preos-production-learn`.

If PREOS is unavailable, do not fabricate its risk/control/gate results. Mark the production-assurance dependency unavailable and route the applicable gate to UNKNOWN or HUMAN REVIEW.

## Project Contract semantics

The PREOS Project Contract is a compiled, version/hash-bound snapshot of approved governing truth. It references rather than replaces:

- Project Charter/Discovery Record;
- PRD;
- SRS when applicable;
- SRD;
- Project Classification Record;
- ADRs and architecture baseline;
- canonical domain/API/data contracts;
- threat/privacy records;
- environment/deployment assumptions;
- human authority assignments.

A source hash/version change makes affected assurance evidence subject to revalidation.

## Assurance activation

Use `orchestration/preos-routing.md` to classify PREOS as inactive, lightweight, standard, or high-assurance. Production intent, multi-tenancy, money movement, personal/sensitive data, privileged operations, consequential automation, major external exposure, and regulatory/contractual obligations are strong activation signals.

## Traceability extension

When PREOS is active, extend the normal Blueprint traceability chain toward:

```text
Product requirement
  -> system/build requirement
  -> risk
  -> control
  -> architecture decision
  -> AI Task Packet
  -> code/configuration
  -> test/failure test
  -> evidence
  -> monitor
  -> recovery/reconciliation/runbook
  -> production gate
```

Not every field applies to every requirement, but critical production behavior must not become untraceable merely because the implementation is AI-assisted.

## No duplicate implementation unit

PREOS may describe implementation-unit semantics, but the integrated system uses the Blueprint AI Task Packet as the single bounded implementation work unit. PREOS enriches that packet with risk, control, evidence, economics, monitoring, recovery, reconciliation, and gate requirements.

## State ownership

Project-specific, version-controlled state belongs in the application repository under `.ai-product-delivery/`.

PREOS runtime/recovery state belongs under `PREOS_STATE_ROOT`.

gstack runtime state remains gstack-owned. Do not place PREOS authoritative state under `.gstack` or `GSTACK_STATE_ROOT`.

## Production decision rule

PREOS can produce assurance status but cannot authorize production by itself. Final deployment remains subject to the Blueprint release gate and accountable human approval. A gstack ship/deploy command is execution after authorization, not the authorization itself.
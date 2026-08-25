# Recommendation Coverage Ledger

This ledger maps the recommendations that define the AI Product Delivery Blueprint and PREOS integration to repository evidence. It is a semantic completeness guard in addition to the structural manifest in `references/INDEX.md`.

## Governing rule

A recommendation is not considered covered merely because a similarly named file exists. Its governing behaviour must appear in the parent skill, orchestration, profile references, validation, or preserved legacy framework. If a recommendation becomes only partially implemented, treat that as a rework condition before merge.

## Recommendation to implementation map

| ID | Recommendation | Implementation evidence | Status |
| --- | --- | --- | --- |
| R01 | Rename the governing skill to `ai-product-delivery-blueprint` | `SKILL.md`, `agents/openai.yaml` | Required |
| R02 | Make the blueprint the governance layer for requirements, gates, architecture, security, design, traceability, release, and operations | `SKILL.md`, `references/core/` | Required |
| R03 | Keep WordPress as a specialised web profile instead of the parent architecture | `SKILL.md`, `references/wordpress/wordpress-lifecycle.md` | Required |
| R04 | Preserve the original deep WordPress framework without weakening it | `references/wordpress/legacy-ai-web-delivery-blueprint.md` and the 14 preserved root WordPress references | Required |
| R05 | Classify the project before implementation | `orchestration/project-classification.md` | Required |
| R06 | Load only applicable profiles and task relevant references to avoid context explosion and conflicting rules | `orchestration/profile-routing.md`, `SKILL.md` | Required |
| R07 | Provide composable Core, Web, WordPress, SaaS, Mobile, API, Data, and Infrastructure profiles | `references/core/`, `references/web/`, `references/wordpress/`, `references/saas/`, `references/mobile/`, `references/api/`, `references/data/`, `references/infrastructure/` | Required |
| R08 | Use a master lifecycle with explicit gates, rework, escalation, stop conditions, and controlled change | `references/core/lifecycle.md`, `SKILL.md` | Required |
| R09 | Require PRD, SRS, SRD, architecture, threat, test, traceability, release, and handoff artifacts when applicable | `SKILL.md`, `references/core/`, `templates/` | Required |
| R10 | Treat SaaS tenant isolation as a hard security boundary | `references/saas/tenant-isolation.md`, `references/saas/saas-lifecycle.md`, `SKILL.md` | Required |
| R11 | Cover the full SaaS operating model, including identity, authorization, RLS, organisations, entitlements, billing, subscriptions, payments, webhooks, idempotency, jobs, queues, caching, storage, search, audit, flags, rate limits, observability, scaling, backup, and disaster recovery | `references/saas/` | Required |
| R12 | Treat mobile as a distinct lifecycle, including Flutter, offline behaviour, sync, conflict handling, device capabilities, permissions, notifications, signing, Android, iOS, store compliance, and installed version compatibility | `references/mobile/` | Required |
| R13 | Establish one canonical cross platform domain and contract model before independent clients implement shared concepts | `orchestration/cross-platform-routing.md`, `SKILL.md` | Required |
| R14 | Provide dedicated API, data, and infrastructure governance | `references/api/`, `references/data/`, `references/infrastructure/` | Required |
| R15 | Use Codex as the implementation engine under bounded AI Task Packets | `orchestration/codex-routing.md`, `references/core/ai-task-packets.md`, `templates/ai-task-packet.md` | Required |
| R16 | Use gstack as the specialist engineering review workforce with exact namespaced commands | `orchestration/gstack-routing.md` | Required |
| R17 | Keep the blueprint, gstack, Codex, and the application repository as separate responsibility layers rather than merging repositories or vendoring tools by default | `orchestration/gstack-routing.md`, `orchestration/codex-routing.md` | Required |
| R18 | Make the application repository the execution surface for product code and project specific artifacts | `orchestration/codex-routing.md` | Required |
| R19 | Require human approval for consequential decisions | `orchestration/approval-routing.md`, `references/core/human-approval-gates.md`, `SKILL.md` | Required |
| R20 | Prevent gstack recommendations or Codex implementation from silently overriding approved blueprint baselines | `orchestration/gstack-routing.md`, `orchestration/profile-routing.md`, `SKILL.md` | Required |
| R21 | Preserve naming, folder, schema, API, and environment conventions and prevent speculative scope expansion | `orchestration/codex-routing.md`, `references/core/change-control.md` | Required |
| R22 | Require independent review, QA, security review when triggered, and evidence before launch | `SKILL.md`, `references/core/testing.md`, `references/core/qa.md`, profile QA modules | Required |
| R23 | Use branches, worktrees, forks, pull requests, CI, and review to isolate substantial AI changes from the protected baseline | `orchestration/codex-routing.md`, repository upgrade branch and draft pull request | Required |
| R24 | Maintain reusable templates instead of recreating governance artifacts ad hoc | `templates/` | Required |
| R25 | Maintain a complete manifest and machine validation so missing architecture is detected before merge | `references/INDEX.md`, `scripts/validate_blueprint.py`, `.github/workflows/validate-blueprint.yml` | Required |
| R26 | Preserve the original WordPress skill text byte identically as a backward traceability source | `references/wordpress/legacy-ai-web-delivery-blueprint.md`, `scripts/validate_blueprint.py` | Required |
| R27 | Integrate PREOS as a production-assurance overlay governed by the Blueprint rather than as a competing delivery profile or standalone product workflow | `SKILL.md`, `orchestration/preos-routing.md`, `references/production-assurance/preos-integration.md` | Required |
| R28 | Keep PREOS canonical corpora and executable methodology in the independent `WilsonMisor/PREOS` repository while integrating through explicit contracts instead of vendoring or copying the corpora here | `references/production-assurance/preos-integration.md`, `SKILL.md` | Required |
| R29 | Classify PREOS assurance level and maturity stage during project classification, with production consequence determining depth rather than convenience | `orchestration/project-classification.md`, `orchestration/preos-routing.md` | Required |
| R30 | Treat the PREOS Project Contract as a hash/version-bound compiled snapshot of approved PRD/SRS/SRD/classification/architecture truth, not a competing requirements source | `orchestration/preos-routing.md`, `references/production-assurance/preos-integration.md` | Required |
| R31 | Run PREOS risk analysis repeatedly: early product/classification pass, architecture pass, per-change risk delta/change impact, release assurance, and production-learning pass; select relevant risks/readiness questions rather than loading the entire corpus | `orchestration/preos-routing.md`, `SKILL.md` | Required |
| R32 | Add architecture economics, complexity tax, measurable activation triggers, migration paths, review triggers, and a Deferred Complexity Registry to prevent speculative over-engineering | `orchestration/preos-routing.md`, `references/core/lifecycle.md`, `templates/ai-task-packet.md` | Required |
| R33 | Use one canonical AI Task Packet and enrich it with PREOS risk IDs, control IDs, failure tests, evidence freshness, monitoring, recovery/reconciliation, economics, change impact, gates, and accountable risk ownership | `references/core/ai-task-packets.md`, `templates/ai-task-packet.md`, `references/production-assurance/preos-integration.md` | Required |
| R34 | Preserve PREOS G0-G11, GREEN/AMBER/RED/HUMAN REVIEW/UNKNOWN semantics, control dependency propagation, evidence freshness, and the rule that UNKNOWN never silently becomes GREEN | `orchestration/preos-routing.md`, `references/core/lifecycle.md`, `SKILL.md` | Required |
| R35 | Keep consequential risk acceptance and production authority human; missing accountable roles become role gaps/HUMAN REVIEW rather than AI personas | `orchestration/preos-routing.md`, `references/production-assurance/preos-integration.md`, `SKILL.md` | Required |
| R36 | Store project-specific assurance state under `.ai-product-delivery/preos/` and runtime/recovery state under independent `PREOS_STATE_ROOT`, never under `.gstack` or `GSTACK_STATE_ROOT` | `orchestration/preos-routing.md`, `references/production-assurance/preos-integration.md`, `SKILL.md` | Required |
| R37 | Close the production loop by routing incidents, near misses, support findings, cost/reliability anomalies, and security findings through PREOS learning and then Blueprint change control | `orchestration/preos-routing.md`, `references/core/lifecycle.md`, `SKILL.md` | Required |
| R38 | Route PREOS assurance needs to gstack specialists while preserving separation of responsibility: PREOS determines required assurance, gstack performs specialist review, Codex implements, Blueprint governs, and humans authorize | `orchestration/preos-routing.md`, `references/production-assurance/preos-integration.md`, `orchestration/gstack-routing.md`, `SKILL.md` | Required |

## Integrated layer model

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
Application Repository
      |
Production
      |
telemetry / incidents / cost / support
      |
PREOS learning
      |
Blueprint change control
```

These are integrated responsibility layers, not one combined repository. Do not merge or vendor the Blueprint, PREOS, gstack, and application repositories merely to make them cooperate. Prefer namespaced skill invocation, approved task packets, versioned contracts, project artifacts, risk/control/evidence IDs, and explicit handoffs.

## Source control safety

For substantial AI generated changes, work on an isolated branch, worktree, or fork. Keep the protected baseline unchanged until review and automated checks pass. Use a pull request or equivalent review boundary before integration. Do not treat a local implementation success as permission to merge, deploy, or alter production.

## Audit rule

Before the Blueprint/PREOS integration is accepted, verify every R item above against current repository content. Any missing or partial item is a stop or rework condition, not an accepted omission.
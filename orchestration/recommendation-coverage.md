# Recommendation Coverage Ledger

This ledger maps the recommendations that defined the AI Product Delivery Blueprint upgrade to the repository evidence that implements them. It is a semantic completeness guard in addition to the structural manifest in `references/INDEX.md`.

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

## Layer model

The intended separation is:

```text
AI Product Delivery Blueprint
  governs requirements, architecture, gates, evidence, and approvals

        |
        +--------------------+
        |                    |
        v                    v
      gstack               Codex
  specialist review     implementation engine
        |                    |
        +---------+----------+
                  |
                  v
          Application Repository
       product code and project artifacts
```

These are integration layers, not one combined repository. Do not merge the blueprint repository, gstack repository, and application repository merely to make them cooperate. Prefer namespaced tool invocation, approved task packets, project artifacts, and explicit handoffs.

## Source control safety

For substantial AI generated changes, work on an isolated branch, worktree, or fork. Keep the protected baseline unchanged until review and automated checks pass. Use a pull request or equivalent review boundary before integration. Do not treat a local implementation success as permission to merge, deploy, or alter production.

## Audit rule

Before the blueprint upgrade is accepted, verify every R item above against current repository content. Any missing or partial item is a stop or rework condition, not an accepted omission.
# PAS v2 Suite Advanced Guide

This guide describes the integrated Blueprint, PREOS, gstack, and Codex operating model. It is implementation guidance, not production-release authority.

## PREOS Only

Use PREOS directly only for production assurance tasks against an already approved Blueprint baseline, such as risk selection, evidence review, gate evaluation, architecture economics, recovery, or production learning. PREOS must bind to a Project Contract and must keep legacy-v1 as the default risk model unless Model2 activation has the required human approval.

## PREOS Stage

The normal PREOS stages are project-init, risk-model, architecture-economics, production-plan, production-implement, and production-learn. Each stage consumes bounded approved project truth and produces risk IDs, control IDs, evidence requirements, gate state, recovery notes, or learning proposals.

## gstack Router

gstack is routed as a specialist workforce. Blueprint and PREOS decide when gstack is needed, pass bounded context, and receive gstack output as challenge, review, QA, security, benchmark, release, canary, or retrospective evidence.

## gstack Specialist

A gstack specialist receives the minimum applicable context: Project Classification Record, active profiles, requirement IDs, risk/control/evidence IDs, ADRs, task-packet scope, known risks, and expected output. A specialist cannot change approved baselines, waive controls, accept risk, or authorize production.

## Task Packet

The AI Task Packet is the implementation unit. A PREOS-enriched packet includes requirement IDs, affected files/components, risk IDs, controls, gates, failure tests, monitoring, recovery, reconciliation, evidence, economics/deferred-complexity impacts, gstack routes, and named human approver when required.

## Recovery

Recovery starts from version-controlled project truth and PREOS runtime state, not conversation memory. After interruption, reconcile Project Contract hashes, task packet binding, Git branch/HEAD/worktree, approvals, gate state, evidence freshness, and the first unverified action before resuming.

## Risk Model

The original 75 controls and legacy risk corpus remain historical invariants. PAS v2 Model2 adds RiskDefinition, RiskAssessment, RiskEconomics, RiskEvolution, RiskEvidence, and RiskAcceptance separation, bounded retrieval, contextual variants, relationship queries, and semantic-review gates. Generated or incident-derived risks enter the candidate-risk workflow before canonical promotion.

## Gate Evaluation

PREOS evaluates G0-G11 as applicable. UNKNOWN, RED, stale evidence, expired acceptance, missing qualified authority, or unresolved HUMAN REVIEW fails closed for the affected production path. AI may recommend and implement approved scope, but it cannot accept material risk or grant release authority.

## Suite Diagnostics

Run `install-suite.ps1 -Mode verify` on Windows or `bash install-suite.sh --mode verify` on POSIX from the Blueprint repository. Suite doctor validates the suite lock, manifest-derived skill inventory, installed owned skills, Virtual Team agents, Blueprint validation, PREOS validation, and gstack integration checks.

## Install, Update, Repair, Uninstall

Install uses the common skill root selected by `CODEX_HOME/skills` or explicit `CODEX_SKILL_ROOT`. Update and repair require explicit update permission and refuse dirty repositories. Uninstall removes only manifest-owned suite skills and Virtual Team agent metadata while preserving unrelated user skills and files.

## Rollback

Rollback uses the previous SUITE-LOCK component commits or Git bundles from the audit package. Restore each repository to the recorded commit, reinstall the suite into an isolated `CODEX_HOME`, run suite doctor, and keep production gates closed until the restored evidence passes.

## Physical Separation vs Logical Suite

Blueprint, PREOS, gstack, and the application repository stay physically separate. The logical suite connects them through installed skills, SUITE-LOCK, Project Contracts, AI Task Packets, risk/control/evidence IDs, gstack handoffs, and deterministic validators. Do not merge or vendor the repositories merely to make them cooperate.
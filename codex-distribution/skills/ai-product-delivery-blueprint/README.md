# AI Product Delivery Blueprint

This repository contains a Codex skill for governed AI assisted product delivery across general web applications, WordPress, SaaS, APIs, data, infrastructure, and Flutter mobile applications.

The original WordPress delivery framework is preserved. It now operates as the WordPress profile inside the broader `ai-product-delivery-blueprint` architecture.

## Safety

Development of the upgrade is isolated on `upgrade/ai-product-delivery-blueprint` before merge to `main`.

## Structure

1. `SKILL.md` is the parent governance and routing skill.
2. `references/core/` contains rules shared by all substantial projects.
3. `references/web/`, `references/wordpress/`, `references/saas/`, `references/mobile/`, `references/api/`, `references/data/`, and `references/infrastructure/` contain selectively loaded profiles.
4. `orchestration/` controls classification, profile loading, cross platform contracts, approvals, Codex execution, and gstack routing.
5. `templates/` contains reusable governed artifact formats.
6. `references/virtual-team/` contains deterministic advisory role registry, router, and role cards.
7. Existing root level WordPress references remain intact for deep WordPress guidance and backward traceability.

Read `references/INDEX.md` for the complete manifest.

## Integrated Suite Quick Start

1. Install the suite with `install-suite.ps1 -Mode install` on Windows or `bash install-suite.sh --mode install` on POSIX.
2. Open the governed application repository.
3. Invoke `$ai-product-delivery-blueprint`.
4. Describe the product objective, constraints, users, data, jurisdictions, architecture, and release target.
5. Let Blueprint classify the project and route PREOS/gstack only where the Project Contract, risk profile, or task packet requires them.
6. Approve only genuine human gates: risk acceptance, qualified legal/security/financial authority, Model2 activation, and production release.

See `docs/pasv2-suite-advanced.md` for PREOS-only use, stage routing, gstack specialist handoffs, task packets, recovery, risk model behavior, gate evaluation, suite diagnostics, lifecycle commands, rollback, and physical separation vs logical suite boundaries.
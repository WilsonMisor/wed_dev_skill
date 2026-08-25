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
6. Existing root level WordPress references remain intact for deep WordPress guidance and backward traceability.

Read `references/INDEX.md` for the complete manifest.

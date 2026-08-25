# Architecture Coverage Matrix

Use this file as a structural completeness guard for the repository architecture. Use `orchestration/recommendation-coverage.md` as the semantic recommendation completeness guard.

## Required top level components

1. `SKILL.md`.
2. `agents/openai.yaml`.
3. `references/core/`.
4. `references/web/`.
5. `references/wordpress/`.
6. `references/saas/`.
7. `references/mobile/`.
8. `references/api/`.
9. `references/data/`.
10. `references/infrastructure/`.
11. `references/production-assurance/`.
12. `orchestration/project-classification.md`.
13. `orchestration/profile-routing.md`.
14. `orchestration/preos-routing.md`.
15. `orchestration/gstack-routing.md`.
16. `orchestration/codex-routing.md`.
17. `orchestration/approval-routing.md`.
18. `orchestration/cross-platform-routing.md`.
19. `orchestration/recommendation-coverage.md`.
20. `templates/`.
21. `references/INDEX.md`.

## Recommendation coverage checks

The architecture is not complete unless all of the following are represented in governing content and mapped in `orchestration/recommendation-coverage.md`.

1. Parent `ai-product-delivery-blueprint` identity.
2. Core governance and lifecycle.
3. General web profile.
4. Specialised WordPress profile.
5. Exact preservation of the original WordPress framework.
6. SaaS profile with tenant isolation as a hard boundary.
7. Mobile and Flutter lifecycle.
8. API profile.
9. Data profile.
10. Infrastructure profile.
11. Project classification before implementation.
12. Selective profile and reference loading.
13. Canonical cross platform contracts.
14. Bounded Codex task packets.
15. Exact namespaced gstack specialist routing.
16. Human approval gates.
17. Blueprint, PREOS, gstack, Codex, and application repository responsibility separation.
18. Application repository as the product execution surface.
19. No repository merging or vendoring merely for integration.
20. Source control isolation for substantial AI changes.
21. Independent review and QA.
22. Stop and rework semantics for unresolved hard failures.
23. Reusable governed artifact templates.
24. Manifest based completeness validation.
25. CI validation before merge.
26. Byte identical legacy WordPress skill preservation.
27. PREOS as a production-assurance overlay rather than a competing delivery profile.
28. PREOS canonical implementation/corpora remain in `WilsonMisor/PREOS`.
29. PREOS assurance level and maturity classification.
30. Hash/version-bound Project Contract semantics.
31. Repeated PREOS risk passes plus selective risk/readiness loading.
32. Architecture economics and Deferred Complexity Registry.
33. One AI Task Packet enriched by PREOS rather than duplicate implementation units.
34. G0-G11 and deterministic GREEN/AMBER/RED/HUMAN REVIEW/UNKNOWN semantics.
35. Control-dependency propagation and evidence freshness/invalidation.
36. Human-only consequential risk acceptance and role-gap handling.
37. `.ai-product-delivery/preos/` project state plus independent `PREOS_STATE_ROOT` runtime state.
38. Production-learning feedback through Blueprint change control.
39. PREOS assurance needs route to gstack specialists without transferring assurance authority to gstack.
40. Codex remains implementation engine under the approved enriched packet.

## Validation rule

Validation must compare the branch tree against `references/INDEX.md`, verify the recommendation coverage ledger is present through R38, verify PREOS routing and integration contracts remain explicit, verify repository/tool/state boundaries remain explicit, and verify preserved WordPress content still matches `main` before merge.
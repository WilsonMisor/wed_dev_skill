# gstack Routing

gstack is the specialist engineering workforce. The AI Product Delivery Blueprint remains the governance authority. Codex remains the implementation engine unless an approved task deliberately assigns another executor.

## Installation assumption

When gstack is installed beside this skill in Codex, prefer the gstack namespaced installation so its commands do not collide with other skills. The expected forms below therefore use the `gstack-` prefix. If the local installation uses short names, map the same specialist to its unprefixed equivalent.

## Repository and tool boundary

Keep the blueprint, gstack, Codex, and the application repository as separate responsibility layers.

1. The AI Product Delivery Blueprint repository owns governance, lifecycle rules, profiles, templates, routing, and validation.
2. gstack remains an independently installed specialist tool or skill. Do not copy or merge the gstack repository into this blueprint merely to integrate it.
3. Codex is the execution engine. It consumes approved requirements, task packets, and specialist findings rather than becoming a replacement source of truth.
4. The application repository owns product source code and project specific artifacts.
5. Do not merge the blueprint repository, gstack repository, and application repository merely to make them cooperate.
6. Integrate through namespaced skill invocation, bounded task packets, approved artifacts, review findings, and explicit handoff contracts.
7. Vendor or copy another layer only when an approved Architecture Decision Record documents the concrete need, ownership, version pinning, update process, security impact, and rollback path.

## Mandatory lifecycle routing for substantial work

1. Discovery and problem reframing, use `gstack-office-hours`.
2. Product value, scope, and strategic challenge, use `gstack-plan-ceo-review`.
3. Architecture, data flow, state, edge cases, failure modes, and test planning, use `gstack-plan-eng-review`.
4. Planned UX and UI quality, use `gstack-plan-design-review` when a user facing design is in scope.
5. Design system or direction from scratch, use `gstack-design-consultation` when the project needs a design foundation.
6. Alternative visual directions, use `gstack-design-shotgun` when deliberate exploration is approved.
7. Production HTML from an approved design artifact, use `gstack-design-html` only when HTML generation fits the active web architecture and does not conflict with WordPress or framework constraints.
8. Developer experience planning for public APIs, SDKs, CLIs, onboarding, or developer products, use `gstack-plan-devex-review` when applicable.
9. Security and threat review, use `gstack-cso` when the threat model, profile, or change risk triggers security review.
10. Implementation, use Codex under an approved AI Task Packet.
11. Code review, use `gstack-review` and supply requirement IDs, architecture decisions, acceptance criteria, changed files, tests, and known risks.
12. Root cause debugging, use `gstack-investigate` before speculative fixes.
13. Integrated browser QA with remediation, use `gstack-qa` when authorised to fix discovered defects.
14. Report only browser QA, use `gstack-qa-only` when the reviewer must not modify code.
15. Live design audit and approved remediation, use `gstack-design-review` when the implemented UI needs design QA.
16. Live developer experience audit, use `gstack-devex-review` for developer facing products when applicable.
17. Browser based research or inspection, use `gstack-browse` when gstack browser tooling is the approved browsing path.
18. Release preparation and pull request shipping, use `gstack-ship` only after the blueprint release gate passes.
19. Production landing and deployment, use `gstack-land-and-deploy` only when deployment is explicitly approved and the environment profile permits it.
20. Canary validation, use `gstack-canary` when the deployment strategy includes a canary stage.
21. Benchmarks, use `gstack-benchmark` when performance or comparative measurements are requirements and the benchmark method has been defined.
22. Release documentation, use `gstack-document-release` when release notes and operational evidence are required.
23. General governed documentation generation, use `gstack-document-generate` when it supports an approved artifact and does not replace accountable review.
24. Post release retrospective, use `gstack-retro` and feed accepted findings into risks, ADRs, tests, maintenance, and future task packets.

## Optional workflow accelerators

`gstack-autoplan` may be used to accelerate planning, but its output remains subject to the same PRD, profile, architecture, security, design, and human approval gates.

`gstack-careful`, `gstack-freeze`, `gstack-guard`, and `gstack-unfreeze` may be used as additional execution safety controls when available. They do not replace repository permissions, branch protection, task packet boundaries, or human approval.

`gstack-learn` may capture reusable lessons after accepted work. Do not allow learned preferences to override project requirements or security rules.

`gstack-gstack-upgrade` is maintenance of the gstack tool itself and is not part of an application release unless explicitly requested.

## Separation of responsibility

1. gstack may challenge requirements and architecture. It may not silently change an approved baseline.
2. Codex may implement an approved packet. It may not expand scope without approval.
3. The blueprint evaluates whether required artifacts, controls, evidence, and approvals exist.
4. Human owners make consequential acceptance and release decisions.
5. If gstack advice conflicts with a hard blueprint rule or an approved project baseline, record the conflict and obtain human resolution.

## Handoff contract to every specialist

Provide the specialist only the context it needs, including:

1. Project Classification Record.
2. Active profiles.
3. Relevant approved requirement IDs.
4. Applicable ADRs and domain contracts.
5. Design baseline where relevant.
6. Threat and control IDs where relevant.
7. Current task packet or review scope.
8. Known risks and accepted exceptions.
9. Required evidence and expected output.

Do not ask a specialist to infer the entire product from the repository when an approved governing artifact exists.
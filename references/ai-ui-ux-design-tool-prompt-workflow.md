# AI UI/UX Design Tool Prompt Workflow

Use this when a WordPress project uses AI-powered design, wireframing, prototyping, JSON design specifications, coded mockups, or page/template mockup generation through Figma Make, Claude Design, Codex, Claude Code, or an equivalent AI-assisted design workflow.

## Core Rule

Before main WordPress/theme/template/CPT-template coding begins, prove the UX/UI design and obtain owner approval for the launch-scope page/template baseline. Low-fidelity wireframes are optional as a separate artifact; design proof is not optional.

Always create a Design Artifact Strategy and UX/UI Framework Compliance Matrix before generating AI design prompts or mockups. The strategy must state which artifact path each page/template group will use: Figma Make, Claude Design, JSON low-fidelity wireframe specification, JSON high-fidelity wireframe/UI specification, coded HTML/CSS mockup, clickable prototype, static screenshots, or a hybrid of these. The chosen path must still prove structure, hierarchy, user flows, states, responsive behavior, accessibility, WordPress/CPT/admin mapping, SEO/security/privacy UX, implementation feasibility, and owner-review readiness.

The AI Design Tool Prompt Package remains the source of truth for generated outputs. It must synthesize the approved PRD, sitemap/page briefs, Conversion/SEO/Security Applicability Matrix, SEO architecture, cybersecurity threat model/control matrix, content model, brand assets, WordPress CPT/admin model, forms, integrations, analytics/conversion goals, domain workflows, target users, accessibility/privacy requirements, device/browser targets, technical constraints, the selected Design Artifact Strategy, and the UX/UI Framework Compliance Matrix. Do not rely on a short creative prompt for launch-scope design work.

AI may draft and revise the strategy, UX/UI Framework Compliance Matrix, prompt package, JSON specifications, coded mockups, and design-tool prompts, but it cannot be the sole approver of strategy completeness, prompt completeness, owner mockup acceptance, accessibility/security/privacy risk acceptance, or build release. A named human must approve the strategy, UX/UI Framework Compliance Matrix, and prompt package; the website owner must approve the generated page/template mockups or design baseline before SRD final baseline and main WordPress/theme/template coding.

## Framework Loading Guidance

Use `references/workplace-ux-ui-design-and-wireframing-framework.txt` as the detailed UX/UI lifecycle source when creating or auditing design strategy, wireframes, high-fidelity UI, prototypes, handoff, design QA, or post-launch UX measurement.

Use `references/ux-laws-and-ui-dos-donts.md` as the tactical UX law and UI dos/don'ts source when creating or auditing AI design prompts, UX/UI Framework Compliance Matrix rows, generated mockups, coded mockups, form UX, mobile/touch layouts, onboarding, search, loading/success/error states, spacing/hierarchy, button copy, color semantics, gradients, nested radius, progress indicators, or design QA evidence.

Use `references/human-design-governance.md` as the deliberate design governance source when defining design intent, design rationale, rule classes, human design hard guardrails, content-driven composition, brand specificity, responsive recomposition, and acceptance questions.

Use `references/ai-visual-antipatterns-and-audit.md` when selecting layouts/components, identifying project-specific AI visual cliches, setting a pattern budget, running the pattern convergence audit, applying brand specificity/swap-the-logo/restraint tests, or reviewing component justification.

Use `references/human-design-scorecard.md` before accepting major page/template mockups, coded mockups, or implemented UI.

Use `references/content-resilience-and-wordpress-visual-qa.md` before final design acceptance, visual QA, frontend QA, UAT, launch readiness, or audits of secondary WordPress templates/states.

For targeted loading in the workplace framework, search these headings first:

- `PART 1. COMPLETE WORKPLACE DESIGN LIFECYCLE`
- `Gate 4. Low fidelity wireframing`
- `Gate 5. Visual system and high fidelity design`
- `Gate 6. Prototype validation`
- `Gate 7. Developer handoff`
- `Gate 8. Implementation QA`
- `PART 5. INFORMATION ARCHITECTURE AND CONTENT STRATEGY`
- `PART 6. JOURNEYS, TASK FLOWS, AND USER FLOWS`
- `PART 7. RESPONSIVE AND ADAPTIVE PRODUCT DESIGN`
- `PART 13. LOW FIDELITY WIREFRAMING`
- `PART 15. HIGH FIDELITY UX/UI DESIGN`
- `PART 18. USABILITY, ACCESSIBILITY, AND CROSS-DEVICE TESTING`
- `PART 19. DEVELOPER HANDOFF AND SPECIFICATIONS`
- `PART 21. WORKPLACE TEMPLATES`
- `PART 22. QUALITY BAR`
- `PART 23. COMMON ANTI-PATTERNS`
- `ADDENDUM. ADVANCED UX/UI BEST PRACTICES`

## UX/UI Framework Compliance Matrix Rules

Create a UX/UI Framework Compliance Matrix after the Design Artifact Strategy and before the AI Design Tool Prompt Package. This matrix proves the workplace UX/UI framework was applied, not merely copied into the skill.

Each major framework gate, part, checklist, quality rule, and advanced best-practice area must be classified as one of: applied now, applied later, contextual mandatory, not applicable, approved exception, or blocked. Do not mark an item not applicable just to reduce work; every not-applicable or exception row needs a rationale, owner, approver, risk, mitigation, and review/expiry date where risk remains.

The matrix must cover at minimum:

- Lifecycle gates: Gate 0 intake/scope through Gate 9 production measurement and improvement.
- UX/UI foundations: UX, UI, low-fidelity proof, high-fidelity proof, prototyping, testing, developer handoff, production measurement.
- Product strategy/discovery: problem framing, user groups, business goals, success metrics, constraints, risks, open questions.
- Requirements/rules/states: functional requirements, nonfunctional requirements, business rules, data objects, roles/permissions, content needs, state inventory, edge cases, analytics events.
- Information architecture/content strategy: sitemap, navigation, object relationships, taxonomy, page table, URL/route map, copy quality, labels, errors, success messages, consent/legal text.
- Journeys/flows: user journeys, task flows, decision branches, errors, permissions, cancellations, recovery paths, analytics.
- Responsive/adaptive design: compact, medium, expanded, large, extra-large layouts; mobile, tablet, desktop, input method, density, tables, overlays, text wrapping, safe areas.
- Interaction and product patterns: navigation, forms, search/filter, tables, modals, alerts, dashboards, portals, commerce, admin systems, account/auth, destructive actions, confirmations.
- Visual UI foundations: hierarchy, grid, spacing, typography, color semantics, iconography, imagery, motion, density, data visualization, design tokens.
- Accessibility and inclusive design: headings, reading/focus order, accessible names, labels, error association, contrast, keyboard, target sizes, motion, text scaling, reflow, assistive technology assumptions.
- Design system/component governance: components, variants, states, tokens, naming, reuse, alignment with WordPress templates and code components.
- Low-fidelity and high-fidelity craft: structure proof, alternatives for risky screens, realistic content, component states, responsive variants, annotations, accessibility.
- Prototyping/testing/handoff/QA: critical workflows, usability findings, accessibility findings, developer handoff specs, implementation QA, design defect severity, post-launch measurement.
- File organization and governance: versioning, approved vs work-in-progress separation, archive rules, decision logs, owner approvals.
- Quality bar and anti-patterns: product clarity, UX architecture, low-fidelity quality, interaction quality, visual quality, responsive quality, accessibility, content quality, handoff quality, evidence, common anti-pattern avoidance.
- Advanced best practices: color psychology, form hierarchy, cognitive load, visual perception/Gestalt, affordance/signifiers/discoverability, microcopy/trust, heuristic review, design critique, wireframing craft, design-tool best practices, additional anti-patterns.
- UX laws and UI dos/don'ts: Jakob's Law, Hick's Law, Fitts's Law, Miller's Law, Proximity Law, Von Restorff Effect, Serial Position Effect, Tesler's Law, Doherty Threshold, Peak-End Rule, and the 20 dos/don'ts for primary-action emphasis, skeleton loading, gradients, color meaning, field errors, softened neutrals, search hints, radio/checkbox choice rules, touch controls, grouping, nested radius, long-form steps, minimalism, button text, full-width mobile buttons, structured inputs, progress/milestones, small-choice display, onboarding skip, and spacing hierarchy.
- Human Design Governance: hard guardrails, design principles, AI pattern warnings, design intent, design decision rationale, content-driven composition, brand specificity, systematic consistency, controlled variation, purposeful restraint, semantic components, realistic content, responsive recomposition, accessibility as design, and acceptance questions.
- Anti-AI visual audit: pattern catalogue, pattern convergence audit, pattern budget, brand specificity test, swap-the-logo test, restraint test, component justification rules, project-specific anti-pattern risks, layout/typography/color/imagery/icon/motion checks, and reasoning examples.
- Content resilience and WordPress visual completeness: realistic content variation, secondary WordPress templates/states, component differentiation, and rendered visual QA where tools are available.
- Human Design Scorecard: weighted 100-point score, pass/revise/fail thresholds, and hard failure conditions.

Minimum pass rule: unresolved critical issues in product clarity, task completion, accessibility, responsive behavior, WordPress implementation feasibility, security/privacy UX, or owner approval block SRD final baseline and WordPress coding unless an accountable human records an explicit exception with mitigation and expiry.
## Required Sequence

1. Confirm the design tool and artifact strategy: Figma Make, Claude Design, JSON low/high-fidelity wireframe specs by Codex or Claude Code, coded HTML/CSS mockups, clickable prototypes, static screenshots, or a hybrid. Record tool limits, export format, fidelity target, collaboration method, version links/screenshots, and evidence capture.
2. Decide whether low-fidelity wireframes are required for each page/template group. Require them when structure, navigation, form complexity, permissions, responsive behavior, domain workflow, or stakeholder uncertainty is high. Allow them to be skipped when another artifact path proves the same structure and review needs.
3. Read and reconcile source artifacts: PRD, page briefs, sitemap, URL inventory, content plan, applicability matrix, SEO architecture, cybersecurity control matrix, WordPress CPT/content model, admin/editor needs, forms, integrations, analytics, brand/style inputs, accessibility/privacy constraints, device/browser support, prior approved templates, relevant framework sections, Human Design Governance references, anti-AI visual audit rules, content resilience/WordPress visual QA rules, Human Design Scorecard, and UX laws/UI dos/don'ts source. Create the UX/UI Framework Compliance Matrix before prompt execution.
4. Build inventories before writing prompts or JSON specs: pages/templates, user flows, admin/editor flows, actions, menus, widgets, components, content modules, CPT fields/media needs, custom/page-specific forms, above-the-fold CTAs, thank-you/success states, breadcrumbs, FAQs, case studies, reviews, maps/directions, sticky mobile CTAs, privacy links, analytics events, integrations, states, roles, permissions, responsive breakpoints, design intent needs, content model, project-specific anti-pattern risks, WordPress visual completeness scope, content resilience cases, and evidence needed for approval.
5. Create or verify the Human Design Governance record and design intent before high-fidelity prompt execution. Define visual character, emotional tone, information density, brand expression, type/color/image/composition/motion/interaction direction, restraint level, project-specific visual cliches to avoid, major design decision rationale, and anti-AI pattern risks.
6. Generate the AI Design Tool Prompt Package with tool-specific instructions plus reusable page-by-page, workflow-by-workflow, state-by-state, artifact-path, Human Design Governance, anti-pattern audit, content resilience, WordPress visual completeness, and scorecard sections.
7. Run a strategy, Human Design Governance, UX/UI Framework Compliance Matrix, prompt completeness, anti-AI audit, content resilience, WordPress visual completeness, and scorecard-readiness gate. If a page, workflow, component, state, content dependency, SEO/security/accessibility/privacy need, WordPress/CPT/admin requirement, UX law/UI dos-don'ts rule, human design guardrail, design intent, anti-pattern risk, responsive rule, visual QA evidence rule, or artifact evidence rule is missing, revise before execution.
8. Execute the approved artifact path. If the tool has prompt-size limits, split the package into a project brief, design system prompt, component prompt, page batch prompts, JSON spec prompts, coded mockup prompts, workflow/state prompts, human design audit prompt, and revision prompts while preserving one versioned source-of-truth package.
9. Audit generated outputs against the prompt package, artifact strategy, Human Design Governance record, anti-AI pattern audit, content resilience rules, WordPress visual completeness scope, and scorecard before owner review. Missing pages, weak states, generic layouts, unjustified pattern convergence, weak brand specificity, design intent mismatch, domain inaccuracies, inaccessible controls, SEO-unsafe hierarchy, privacy/security UX gaps, responsive failures, content overflow, or mismatched WordPress/CPT/admin behavior return to the prompt/artifact/mockup loop.
10. Package generated mockups or equivalent design baseline artifacts for website-owner review, record page-level feedback, rework through the selected tools, and freeze only owner-approved versions that pass Human Design Governance gates or carry approved exceptions.

## Design Artifact Strategy Must Cover

- Artifact path per page/template group: Figma Make, Claude Design, JSON low-fidelity specification, JSON high-fidelity specification, coded HTML/CSS mockup, clickable prototype, static screenshot set, or hybrid.
- Low-fidelity decision: required, optional, skipped, deferred, or not applicable, with rationale and approver.
- Design proof method: how the chosen artifacts prove information architecture, content hierarchy, primary actions, flows, states, responsive behavior, accessibility, SEO/security/privacy UX, and WordPress implementation feasibility.
- UX/UI Framework Compliance Matrix scope, required framework sections, Human Design Governance rows, anti-AI pattern audit rows, content resilience/WordPress visual QA rows, scorecard/hard-failure expectations, and unresolved exceptions.
- Tool execution plan: prompts, inputs, batching, exports, screenshots, prototype links, file naming, versioning, and review method.
- Review gates: strategy approval, Human Design Governance/design intent approval, prompt completeness, structure proof, anti-AI pattern audit, Human Design Scorecard, content resilience and WordPress visual completeness review, high-fidelity/design baseline audit, owner approval, developer handoff, rendered visual QA where tools are available, and design QA.
- Exception rules: skipped wireframes, missing tablet variants, unprototyped flows, unavailable tool exports, or deferred pages require accountable approval, risk, mitigation, and expiry/review date.

## JSON Wireframe and UI Specification Rules

JSON low/high-fidelity specs generated by Codex or Claude Code are valid design artifacts when they are structured enough to drive review, AI design-tool generation, or coded mockup creation.

JSON specs must define:

- Project metadata, source artifact IDs, page/template IDs, and approval status.
- Responsive model for compact, medium, expanded, large, and extra-large layouts where applicable.
- Page regions, content hierarchy, navigation, menus, breadcrumbs, CTAs, forms, widgets, media, internal links, trust elements, and footer behavior.
- Component inventory with variants, states, semantic roles, accessible names, focus behavior, validation, loading/empty/error/success behavior, and responsive rules.
- WordPress mapping: template hierarchy, CPT archives/singles, taxonomies, metabox/admin/editor needs, custom metadata fields, media/photo uploads, editable regions, and block-builder exception status.
- SEO/security/privacy notes: headings, crawlable content, schema opportunities, alt-text needs, consent, safe upload messaging, account/session cues, no sensitive data exposure, and analytics events.
- Review evidence: generated previews/screenshots, reviewer notes, owner feedback, approved version, and unresolved exceptions.

## Coded Mockup Rules

Coded HTML/CSS mockups generated by Codex or Claude Code are valid review artifacts when they are explicitly scoped as design proof or implementation starter artifacts. They must:

- Use realistic content and stable responsive layouts.
- Demonstrate primary workflows, states, forms, navigation, CPT template behavior, accessibility, SEO hierarchy, and security/privacy UX.
- Avoid pretending to be production-ready WordPress code unless released through an approved build task packet.
- Include review screenshots or a local/staging URL, version notes, owner feedback, and accepted exceptions.

## Prompt Package Must Cover

- Project objective, business model, success metrics, target users, excluded users, domain vocabulary, trust signals, regulatory/privacy/security expectations, and owner priorities.
- UX/UI Framework Compliance Matrix summary: applied framework sections, Human Design Governance rows, anti-AI pattern audit rows, contextual mandatory rows, approved exceptions, blocked rows, and quality-bar risks.
- Human Design Governance: design intent, hard guardrails, design principles, AI pattern warnings, design rationale, project-specific cliches to avoid, brand specificity goals, content-driven composition rules, responsive recomposition expectations, and human design acceptance questions.
- Anti-AI visual audit: pattern convergence risks, pattern budget, brand specificity test, swap-the-logo test, restraint test, component justification, project-specific risk list, and accepted/common patterns with rationale.
- Human Design Scorecard and hard failures: expected pass threshold, category risks, hard failure conditions, remediation rules, and human exception requirements.
- Content resilience and WordPress visual completeness: realistic content cases, secondary templates/states, component differentiation, rendered visual QA expectations, and evidence requirements.
- Information architecture: sitemap, navigation, menus, breadcrumbs, footer, search/filter behavior, URL/page-template mapping, CPT archives/singles, taxonomies, and internal-link intent.
- One coherent responsive product model: one user model, one terminology system, one interaction model, one accessibility standard, and one design system adapted across compact, medium, expanded, large, and extra-large layouts.
- Design system: visual direction, color semantics, typography, spacing, radius, elevation, grid, icons, imagery, motion, responsive rules, component naming, and reuse across all selected designs/templates.
- UX laws and UI dos/don'ts constraints: familiar patterns, focused choices, reachable targets, chunking, grouping/proximity, primary-action contrast, first/last placement, safe complexity reduction, fast feedback, strong peak/end moments, skeleton loading, smooth gradients, color semantics, precise errors, softened neutrals where appropriate, search hints, radio/checkbox choice rules, touch controls, nested radius, long-form progress, clear button labels, full-width mobile buttons where useful, structured inputs, visible progress, direct display for 2-3 choices, optional onboarding skip, and spacing hierarchy.
- Page-by-page specs: purpose, target user intent, content hierarchy, H1/section headings, above-the-fold CTAs, sticky mobile CTA where applicable, media, custom/page-specific forms, thank-you/success states, widgets, cards/tables, related content/internal links, case studies, FAQs, real reviews, team photos, maps/directions, social proof, trust/compliance cues, privacy links, analytics events, SEO metadata needs, responsive behavior, and acceptance notes.
- Workflow specs: first-time, returning, lead/contact, search/filter, account/auth, checkout/payment, booking/request, download/resource, support/legal, admin/editor, and domain-specific flows where applicable.
- Action and state specs: hover, focus, active, disabled, loading, empty, no-results, validation error, success, failure, permission denied, expired session, maintenance/offline, 404/403/500, form abandonment, duplicate submission, rate-limit/spam protection, and privacy consent states.
- WordPress/CMS specs: template hierarchy, editable regions, reusable blocks/patterns if allowed, CPT admin screens, custom metadata fields, media/photo upload fields, taxonomy selectors, preview behavior, content author guidance, and the policy that project CPTs must not open the block builder by default unless explicitly approved.
- SEO, accessibility, security, and privacy UX: crawlable content hierarchy, unique titles/meta descriptions/social images, breadcrumbs, headings/internal links/schema opportunities, local schema only where truthful, alt-text needs, keyboard/focus order, labels/errors, contrast/motion/touch targets, consent, secure form behavior, safe file-upload messaging, account/session cues, privacy policy links where required, and no exposure of secrets or sensitive data.
- Developer handoff and QA: tokens, components, variants, states, responsive rules, validation rules, content rules, accessibility notes, analytics events, WordPress template mapping, implementation constraints, screenshot/prototype evidence, and design QA checklist.
- Deliverables: design artifact strategy, desktop/tablet/mobile frames or equivalent responsive specs, JSON specs if used, coded mockups if used, clickable prototype flows where needed, component/state sheet, design-system sheet, page inventory, revision log, owner-review package, export naming, version links, screenshots, and handoff notes.

## AI Design Tool Prompt Skeleton

Use this structure when generating final prompt text or JSON/coded mockup instructions:

1. Role and objective: Tell the tool or coding agent it is designing a complete WordPress website/system, not a landing-page concept.
2. Source context: Summarize approved artifacts, IDs, assumptions, gaps, non-negotiables, UX/UI Framework Compliance Matrix results, Human Design Governance constraints, anti-AI pattern risks, UX laws/UI dos-don'ts constraints, content resilience/WordPress visual QA requirements, scorecard expectations, and framework-derived quality gates.
3. Design Artifact Strategy: State the selected artifact path, low-fidelity decision, deliverables, review evidence, and exception rules.
4. Output contract: List exact pages/templates, breakpoints, flows, states, component sheets, JSON specs, coded mockups, design-system sheets, prototype links, screenshots, and handoff notes to produce.
5. Design system: Define art direction, tokens, icon style, components, responsive grid, motion, accessibility, and reuse rules.
6. Page instructions: Provide one section per page/template with intent, content, CTAs, components, states, SEO/security/accessibility notes, and WordPress template mapping.
7. Workflow instructions: Provide one section per user/admin flow with steps, decisions, errors, edge cases, and success criteria.
8. WordPress/CMS instructions: Specify CPT/admin/editor behavior, metadata/media fields, content author controls, reusable template constraints, and block-builder policy.
9. QA pass: Instruct the tool or coding agent to self-audit for missing pages, generic UI, unjustified AI pattern convergence, weak brand specificity, weak design intent, arbitrary inconsistency, inaccessible states, content overflow, mobile/tablet/desktop recomposition issues, WordPress visual incompleteness, SEO hierarchy problems, security/privacy UX gaps, and WordPress implementation mismatch.
10. Revision protocol: Require the tool or coding agent to preserve approved structure, change only requested areas, and update version notes after every review round.

## Approval Gates

- Design Artifact Strategy gate: human reviewer confirms the selected artifact path is sufficient or records exceptions before prompt/mockup execution.
- UX/UI Framework Compliance Matrix gate: human reviewer confirms every major workplace framework section, Human Design Governance row, anti-AI audit row, UX law/UI dos-don'ts row, content resilience/WordPress visual completeness row, and scorecard expectation is classified, evidenced, not applicable with rationale, or exception-approved before prompt/mockup execution.
- Human Design Governance gate: human reviewer confirms design intent, major decision rationale, content-driven composition, brand specificity, systematic consistency, responsive recomposition, and accessibility-as-design expectations before high-fidelity prompt/mockup execution.
- Prompt completeness gate: human reviewer confirms the package is detailed enough to send to Figma Make, Claude Design, Codex, Claude Code, or another execution tool, or records gaps/exceptions.
- Structure proof gate: reviewers confirm low-fidelity wireframes or equivalent JSON/coded/design artifacts prove structure, hierarchy, flows, states, and responsive behavior, or record why the separate wireframe step was skipped.
- Generated-output audit gate: AI/UX/SEO/security/accessibility reviewers compare mockups or equivalent artifacts to the prompt package, Human Design Governance record, anti-AI visual audit, UX laws/UI dos/don'ts constraints, content resilience/WordPress visual completeness expectations, and route gaps back to revision.
- Human Design Scorecard gate: major page/template mockups, coded mockups, and implemented UI must clear hard failures and score 90+ or be revised; scores from 80-89 require weak-area revision before final acceptance; below 80 fails unless scope changes and accountable exceptions are approved.
- Visual QA gate: where rendering tools are available, reviewers inspect desktop/tablet/mobile/high-zoom and relevant WordPress templates/states before final acceptance.
- Website-owner approval gate: owner reviews every launch-scope page/template or approved template group, requests rework where needed, and explicitly approves the final mockup/design baseline.
- Developer handoff gate: frontend/CMS reviewers confirm tokens, components, responsive rules, states, WordPress template/CPT mapping, and acceptance notes are buildable without guesswork.
- Build release gate: no main WordPress/theme/template/CPT-template coding starts until the relevant strategy, prompt package, generated artifacts, owner approval, and design baseline freeze are linked in the AI task packet.
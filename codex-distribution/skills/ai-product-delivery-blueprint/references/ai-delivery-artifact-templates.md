# AI Delivery Artifact Templates

Use these formats with the full blueprint reference. Keep IDs stable once approved.


## WordPress AI Flow State Checkpoint

Use this at the start of every planning, build, audit, rescue, launch, or handoff session for a WordPress/CMS project. The AI must identify the current state before proposing or executing work.

- Project/site name:
- Current flow state: F0 intake/governance, F1 discovery, F2 PRD, F3 sitemap/page briefs/applicability/SEO/security architecture, F4 design artifact strategy, UX/UI framework compliance, prompt, and mockup loop, F5 SRD/SRS, F6 task packets, F7 WordPress/CPT build, F8 template/content/SEO implementation, F9 QA/SEO crawl, F10 UAT, F11 launch readiness, F12 deploy/stabilize, or F13 hypercare/operations:
- Last completed gate:
- Next gate or decision node:
- Active loop, if any:
- Missing inputs or conflicting artifacts:
- AI actions allowed now:
- Human-only decisions required now:
- Evidence required before next state:
- Approved exceptions or accepted risks:
- Next branch after decision: proceed, rework loop, approved exception, escalate, or stop:

## WordPress AI Flow Gate Evidence Register

| Gate/state | Required artifact/evidence | Owner | Reviewer | Approver | Status | Exception/risk |
|---|---|---|---|---|---|---|
| F0 Governance/AI controls | Charter, RACI, AI policy, permission matrix, task packet template | PM/AI | SP/SA/SEC | SP | | |
| F1 Discovery | Discovery findings, current-site audit, requirements inventory | BA/UX-R/SEO | PO/PDM | SP/PO | | |
| F2 PRD | Approved PRD baseline and requirement IDs | PDM/PO | SA/QA/SEO/ACC/SEC/PRIV | PDM/SP | | |
| F3 Sitemap/page briefs/applicability/SEO/security | Sitemap, page briefs, URL inventory, Conversion/SEO/Security Applicability Matrix, SEO architecture plan, cybersecurity threat model/control matrix | IA/CS/SEO/SEC | PO/UX-D/CMS/SEC | PO/SEO/SEC | | |
| F4 design artifact strategy/framework compliance/prompt/mockups | Design Artifact Strategy, Human Design Governance record, UX/UI Framework Compliance Matrix, AI design-tool prompt package, selected design artifacts, anti-AI visual audit, Human Design Scorecard, content resilience/WordPress visual QA evidence, owner-approved page/template mockups or equivalent baseline, and frozen design baseline | UX-D/UI/AI | WO/ACC/FE/CMS/SEO/SEC | WO/PO | | |
| F5 SRD/SRS | Approved SRD/SRS, architecture, CPT/data/integration/security specs | SA/CMS/SEC | FE/BE/QA/SEC/PRIV/ACC/SEO | SA/PO/SEC | | |
| F6 Task packets | AI task packets with source artifacts, allowed tools, checks, reviewers, approvers | PM/AI | Technical owner | PO/SA/PM | | |
| F7 WordPress/CPT build | Theme/plugin/env evidence; CPT block builder disabled and metadata/media UI evidence | CMS/FE | QA/SA | Technical owner | | |
| F8 Implementation | Templates, content, SEO output, analytics, accessibility/security implementation evidence | FE/CMS/CS/SEO | QA/ACC/SEC/DATA | Technical owner | | |
| F9 QA/SEO/security | QA reports, cybersecurity evidence package, full-site SEO crawl, 90%+ audit score or exception, remediation log | QA/SEO/SEC/AI | FE/CMS/ACC/SEC | QA/SEO/SEC/PO | | |
| F10 UAT | UAT scenarios, defect triage, owner/product acceptance | PO/PM | WO/CX/OPS/CS | PO/WO | | |
| F11 Launch readiness | Launch plan, rollback test, monitoring, support, AI evidence package | PM/DEVOPS/SRE | QA/SEC/PRIV/SEO/DATA | SP/PO | | |
| F12 Deploy/stabilize | Production smoke, indexability, redirects, analytics, monitoring, hotfix/rollback record | DEVOPS/SRE | QA/SEO/DATA | SP/DEVOPS | | |
| F13 Hypercare/ops | Hypercare reports, issue backlog, operations handoff, improvement/change-control record | PM/OPS/SRE | PO/CX/SEO/DATA | OPS/SP | | |


## Cybersecurity Threat Model and Control Matrix

Use this before SRD/SRS baseline and update it before coding security-sensitive work. Map controls to project risk and approved standards such as OWASP Top 10, OWASP ASVS, OWASP WSTG, WordPress hardening guidance, and NIST CSF 2.0.

- Project/site name:
- Security owner:
- Risk level:
- Standards/control baseline used:
- Data classification: public, internal, personal data, sensitive personal data, payment data, credentials/secrets, business confidential:
- Assets to protect:
- Users/roles/privileged accounts:
- Entry points: pages, forms, login/reset, admin screens, CPT save handlers, REST/AJAX endpoints, webhooks, uploads, search/filter URLs, payment/CRM/email integrations, cron/jobs:
- Trust boundaries and data flows:
- Abuse cases:
- Control matrix:
  - Control ID, asset/entry point, threat, required control, implementation owner, verification method, evidence, status, exception/approver.
- Required controls: SQL injection prevention, input validation, output escaping, XSS defense, CSRF/nonces, authentication, authorization, session protection, form abuse protection, upload security, encryption, secrets, database least privilege, backup/restore, web/network protection, dependency scanning, logging/monitoring, incident response.
- Open risks and accepted exceptions:
- Approval record:

## Secure Coding Task Addendum

Attach this to any AI task packet that touches WordPress code, forms, endpoints, database queries, CPT save handlers, uploads, auth, integrations, secrets, infrastructure, or security-sensitive configuration.

- Threat-model/control IDs:
- Protected assets/data:
- Entry points changed:
- Required validation/sanitization/escaping:
- SQL/database rule: prepared statements/parameterized queries, `$wpdb->prepare()` where applicable, no unsafe string-concatenated SQL, least-privilege database user:
- CSRF/nonce rule:
- Authorization/capability checks:
- Authentication/session impact:
- Upload/media restrictions:
- Encryption/secrets impact:
- Logging/monitoring impact:
- Rate limiting/form-abuse controls:
- Security tests to run:
- Security evidence to attach:
- Human security review required: yes/no and reviewer:

## WordPress Cybersecurity Evidence Package

Use this before launch, before major release approval, and after security-sensitive changes. Launch is blocked by unresolved critical/high findings unless an accountable human records an accepted risk with mitigation and expiry.

- Project/site name:
- Environment audited:
- Date/time:
- Auditor/AI run ID:
- Source artifacts: PRD, SRD/SRS, threat model, task packets, Conversion/SEO/Security Applicability Matrix, AI design-tool prompt package, approved mockups, CPT specs, hosting/network plan, database plan, plugin/theme inventory:
- Standards/control baseline used:
- Dependency/plugin/theme vulnerability scan results:
- Secret scan results:
- Static analysis/code review results:
- Dynamic security test results:
- SQL injection prevention evidence:
- Input validation/output escaping/XSS evidence:
- CSRF/nonce evidence:
- Authentication/session/MFA evidence:
- Authorization/capability evidence:
- Form protection evidence: spam/bot/rate limit/consent/duplicate/idempotency/email/CRM controls:
- File upload/media evidence:
- Web protection evidence: headers, CSP where feasible, TLS, HSTS where appropriate, public debug disabled, safe errors:
- Network protection evidence: WAF/CDN/firewall/admin restrictions/staging protection/XML-RPC or REST exposure rules:
- Database protection evidence: least privilege, backups, restore, retention, migration rollback, encrypted backup or exception:
- Encryption/secrets evidence: TLS, at-rest/backups where required, secret storage/rotation, no secrets in code/logs/frontend bundles:
- Logging/monitoring evidence:
- Incident response and rollback evidence:
- Open findings:
- Remediation log:
- Accepted risks/exceptions: issue, severity, reason, compensating control, approver, expiry/review date:
- Security release decision:

## Cybersecurity Evidence Matrix

| Area | Control/evidence | Tool/manual check | Result | Severity | Owner | Status | Exception/expiry |
|---|---|---|---|---|---|---|---|


## Conversion, SEO, and Security Applicability Matrix

Use this before AI design prompt generation, SRD/SRS finalization, build tickets, QA, and launch. Classify each item as compulsory default, contextual mandatory, not applicable, or approved exception.

- Project/site name:
- Matrix version/date:
- Source artifacts: PRD, sitemap, page briefs, content model, SEO architecture, cybersecurity threat model/control matrix, analytics plan, privacy/legal notes, design prompt package:
- Classification rules used: `references/conversion-seo-security-applicability-matrix.md`
- Matrix:
  - Item, classification, applies yes/no, trigger/evidence, page/template/CPT, PRD/SRD/control ID, owner, implementation evidence, QA evidence, status, exception approver/expiry.
- Compulsory default checklist:
  - Internal links on indexable pages, robots.txt/index rules, unique page titles, meta descriptions, social share image fallback, meaningful image alt text, API key/secret protection, Git secret prevention, server-side auth, field-tampering protection, parameterized queries, input validation, output escaping, file-upload restrictions where uploads exist, security headers, HTTPS, dependency scanning.
- Contextual trigger checklist:
  - Custom/page-specific forms, above-the-fold CTA, thank-you/success pages, breadcrumbs, case studies, FAQs, response-time promise, sticky mobile CTA, maps/directions, real reviews, local schema, privacy policy page, analytics, team photo, row-level security/equivalent row ownership, sensitive-data encryption, record-access logging, secure session cookies, password hashing, login rate limiting, bot protection, trimmed API responses.
- Truthfulness/trust review:
  - Reviews, ratings, local business data, case studies, team photos, credentials, maps, directions, and response promises are real, approved, and evidenced.
- Open exceptions:
  - Item, page/template, reason, risk, compensating control, approver, expiry/review date.
## AI Execution Posture Checklist

Attach this to AI task packets, self-reviews, implementation handoffs, documentation work, QA plans, and launch readiness checks when AI performs launch-scope work.

- Plan with intention:
  - Define the site architecture.
  - Map pages and components.
  - Choose the stack and tools.
  - Outline the user flow.
- Build with speed:
  - Generate page structure.
  - Draft reusable components.
  - Create boilerplate faster while respecting project conventions and approved constraints.
- Communicate with clarity:
  - Write clearer UI copy.
  - Explain error messages clearly.
  - Write better README files.
  - Draft cleaner documentation.
- Refine with judgment:
  - Spot bugs and edge cases.
  - Refactor messy logic.
  - Improve readability and structure.
- Verify and ship with clarity:
  - Create testing checklists.
  - Prepare deployment steps.
  - Record checks, evidence, release notes, rollback notes, and handoff status.
## AI Task Packet

- Task ID:
- Accountable human owner:
- Reviewer:
- Approver:
- Goal:
- Non-goals:
- Source artifacts:
- Conversion/SEO/Security Applicability Matrix entries, if relevant:
- Current flowchart state, previous gate, next gate/branch, and active loop if any:
- PRD/SRD requirement IDs:
- Design Artifact Strategy and selected artifact path, if generating/reworking UI/UX artifacts, JSON specs, coded mockups, prototypes, or mockups:
- UX/UI Framework Compliance Matrix entries, if design-sensitive work:
- UX laws/UI dos-don'ts entries, if design-sensitive work:
- Human Design Governance record/design intent/decision rationale, if design-sensitive work:
- Anti-AI visual audit, pattern budget, brand specificity, swap-the-logo, restraint, and component-justification entries, if design-sensitive work:
- Human Design Scorecard and hard-failure status, if accepting visual work:
- Content resilience and WordPress visual completeness/visual QA evidence, if implementing or accepting UI/templates:
- AI design-tool prompt package link, if generating/reworking AI-powered wireframes, prototypes, or mockups:
- Approved page mockup/design baseline links, if user-facing UI or WordPress template work:
- SEO crawl scope, target score, and SEO requirement IDs, if SEO-sensitive work:
- Cybersecurity control IDs, threat-model entries, protected assets/entry points, and security checks, if security-sensitive work:
- Allowed files/systems/tools/environments:
- Prohibited actions:
- Data handling limits:
- Assumptions:
- Acceptance criteria:
- Required checks:
- AI execution posture checklist status, if AI performs launch-scope work:
- Evidence to attach:
- Stop/escalation triggers:
- Rollback or cleanup notes:
- Handoff notes:

## PRD Skeleton

- Version/date:
- Accountable owner:
- Approvers:
- Problem statement:
- Target users and excluded users:
- Evidence/source findings:
- Product vision:
- Outcomes and KPIs:
- User journeys/jobs:
- MVP scope:
- Non-MVP/deferred scope:
- Explicit exclusions:
- Product requirements table:
  - ID, requirement, priority, owner, source, acceptance criteria, status.
- Content/SEO/analytics/support/operations requirements:
- Cybersecurity, form protection, data classification, encryption, abuse prevention, and security evidence requirements:
- SEO architecture and crawl/compliance requirements:
- Assumptions:
- Dependencies:
- Risks:
- Change-control status:

## SRD/SRS Skeleton

- Version/date:
- Accountable owner:
- Approvers:
- PRD baseline referenced:
- System context and boundaries:
- Functional requirements table:
  - ID, source PRD ID, behavior, actor/system, inputs, outputs, states/errors, priority, verification method.
- Non-functional requirements table:
  - ID, source PRD/control ID, category, measurable requirement, owner, verification method.
- Roles and permissions:
- Data model and retention rules:
- API/integration contracts:
- Security/privacy/accessibility/performance/reliability requirements:
- Threat-model/control IDs and cybersecurity verification requirements:
- Observability, backup, rollback, and operations requirements:
- Exclusions and accepted risks:
- PRD-to-SRD traceability matrix:
- Change-control status:


## Design Artifact Strategy

Use this before AI-powered wireframing, JSON wireframe/spec generation, coded mockups, prototyping, or page mockup creation. Low-fidelity wireframes are optional as a separate artifact; the design proof and owner-approved baseline are mandatory.

- Project/site name:
- Strategy version/date:
- Accountable owner:
- Strategy reviewer:
- Strategy approver:
- Source artifact versions: PRD, sitemap/page briefs, URL inventory, content model, Conversion/SEO/Security Applicability Matrix, Human Design Governance references/record, UX/UI Framework Compliance Matrix, SEO architecture, cybersecurity control matrix, WordPress CPT/admin model, forms/integrations, brand assets, accessibility/privacy requirements, analytics/conversion goals, technical constraints, relevant workplace UX/UI framework sections, and UX laws/UI dos/don'ts source:
- Design artifact path table:
  - Page/template group, selected path: Figma Make, Claude Design, JSON low-fidelity spec, JSON high-fidelity spec, coded HTML/CSS mockup, clickable prototype, static screenshot set, or hybrid; low-fidelity decision: required/optional/skipped/deferred/not applicable; reason; review evidence; owner approval requirement; exception/expiry.
- Human Design Governance summary:
  - Design intent, brand specificity goals, content-driven composition rationale, project-specific AI visual cliches to avoid, common patterns deliberately used with rationale, visual restraint level, responsive recomposition approach, and major decision rationale links.
- Structure proof method:
  - How the chosen path proves information architecture, content hierarchy, primary actions, flows, states, responsive behavior, accessibility, SEO/security/privacy UX, WordPress/CPT/admin mapping, Human Design Governance requirements, and implementation feasibility before build.
- JSON specification contract, if used:
  - Pages/templates, layout regions, components, content hierarchy, responsive breakpoints, states, interactions, forms, menus, CTAs, WordPress CPT/template mapping, accessibility notes, SEO notes, security/privacy UX notes, analytics events, owner-review acceptance criteria, and evidence links.
- Coded mockup contract, if used:
  - Local/staging URL or screenshot set, responsive coverage, realistic content, states, accessibility notes, SEO hierarchy, security/privacy UX, WordPress feasibility notes, version notes, and production-code caveat.
- Tool execution and prompt-splitting plan:
- Review gates:
  - Strategy approval, prompt completeness, structure proof, high-fidelity/design baseline audit, owner approval, developer handoff, design QA.
- Exceptions:
  - Missing artifact, skipped wireframe, deferred breakpoint, unprototyped flow, reason, risk, compensating control, approver, expiry/review date.
- Approval record:
## UX/UI Framework Compliance Matrix

Use this after the Design Artifact Strategy and before the AI Design Tool Prompt Package. Update it after generated artifacts, owner review, developer handoff, implementation design QA, and launch readiness. The matrix proves the workplace UX/UI framework, Human Design Governance, 10 UX laws, and 20 UX/UI dos/don'ts were actively applied to the WordPress project.

- Project/site name:
- Matrix version/date:
- Accountable UX/design owner:
- Reviewer:
- Approver:
- Source framework file/version/hash:
- Source UX laws/UI dos-don'ts file/version/hash:
- Source Human Design Governance file/version/hash:
- Source anti-AI visual audit file/version/hash:
- Source Human Design Scorecard file/version/hash:
- Source content resilience/WordPress visual QA file/version/hash:
- Source artifact versions: PRD, sitemap/page briefs, URL inventory, content model, Conversion/SEO/Security Applicability Matrix, Design Artifact Strategy, UX/UI Framework Compliance Matrix, SEO architecture, cybersecurity control matrix, WordPress CPT/admin model, forms/integrations, brand assets, accessibility/privacy requirements, analytics/conversion goals, and technical constraints:
- Classification values: applied now, applied later, contextual mandatory, not applicable, approved exception, blocked.
- Matrix rows:
  - Framework ID/source section, requirement/checklist item, classification, rationale, affected page/template/CPT/admin screen/workflow, required artifact/evidence, owner, reviewer, approver, status, exception/risk/mitigation/expiry.
- Required framework coverage inventory:
  - Gate 0 intake/scope.
  - Gate 1 discovery/product understanding.
  - Gate 2 requirements/rules.
  - Gate 3 UX architecture.
  - Gate 4 low-fidelity wireframing, if required by strategy.
  - Gate 5 visual system/high-fidelity design.
  - Gate 6 prototype validation, where needed.
  - Gate 7 developer handoff.
  - Gate 8 implementation QA.
  - Gate 9 production measurement/improvement.
  - Part 2 UX/UI foundations.
  - Part 3 product strategy/discovery.
  - Part 4 requirements/rules/states.
  - Part 5 information architecture/content strategy.
  - Part 6 journeys/task flows/user flows.
  - Part 7 responsive/adaptive product design.
  - Part 8 interaction design.
  - Part 9 core product patterns.
  - Part 10 visual UI design foundation.
  - Part 11 accessibility/inclusive design.
  - Part 12 design system/component governance.
  - Part 13 low-fidelity wireframing.
  - Part 14 low-fidelity wireframing by viewport.
  - Part 15 high-fidelity UX/UI design.
  - Part 16 high-fidelity responsive design.
  - Part 17 prototyping.
  - Part 18 usability/accessibility/cross-device testing.
  - Part 19 developer handoff/specifications.
  - Part 20 design file organization.
  - Part 21 workplace templates.
  - Part 22 quality bar.
  - Part 23 common anti-patterns.
  - Part 24 final operating model.
  - Addendum advanced UX/UI best practices: color psychology, form hierarchy, cognitive load, visual perception/Gestalt, affordance/signifiers/discoverability, microcopy/trust, heuristic review, design critique, wireframing craft, design-tool best practices, additional anti-patterns.
  - UX laws reference: Jakob's Law, Hick's Law, Fitts's Law, Miller's Law, Proximity Law, Von Restorff Effect, Serial Position Effect, Tesler's Law, Doherty Threshold, and Peak-End Rule.
  - UX/UI dos/don'ts reference: primary-action emphasis, skeleton loading, smooth gradients, color psychology/semantic color, field-specific errors, softened neutrals, search placeholders, radio/checkbox choice rules, touch controls, grouping, nested corner radius, long-form steps/progress, avoiding harmful minimalism, actionable button text, full-width mobile buttons where useful, structured inputs, progress bars/milestones, direct display for 2-3 choices, optional onboarding skip, and spacing hierarchy.
  - Human Design Governance reference: hard guardrails, design principles, AI pattern warnings, mandatory design workflow, design intent, decision rationale, intentional hierarchy, content-driven composition, brand specificity, systematic consistency, controlled variation, purposeful restraint, semantic components, realistic content, responsive recomposition, accessibility as design, and acceptance questions.
  - Anti-AI visual audit reference: pattern catalogue, pattern convergence audit, pattern budget, brand specificity test, swap-the-logo test, restraint test, component justification, layout/type/color/imagery/icon/motion guidance, project-specific warning selection, and reasoning examples.
  - Content resilience and WordPress visual QA reference: realistic content variation, WordPress visual completeness, component differentiation, rendered visual QA, secondary templates/states, and evidence record.
  - Human Design Scorecard reference: weighted score categories, pass/revise/fail thresholds, and hard failure conditions.
- Minimum pass checks:
  - No required framework section is unclassified.
  - No applicable UX law or UI dos/don'ts row is unclassified.
  - No applicable Human Design Governance, anti-AI visual audit, content resilience/WordPress visual QA, or Human Design Scorecard row is unclassified.
  - All contextual mandatory rows have artifact evidence or approved exceptions.
  - Not-applicable rows have project-specific rationale.
  - Critical product clarity, task completion, accessibility, responsive behavior, WordPress feasibility, security/privacy UX, and owner-approval issues are resolved or explicitly accepted by accountable humans.
  - The AI Design Tool Prompt Package and owner mockup/design baseline cite the relevant matrix rows.
- Open exceptions:
  - Framework item, affected artifact/page/template, reason, risk, mitigation, approver, expiry/review date.
- Approval record:
## AI Design Tool Prompt Package

Use this after the Design Artifact Strategy and before AI-powered wireframing, JSON spec generation, coded mockup generation, prototyping, or page mockup generation. The package is the source of truth for Figma Make, Claude Design, Codex, Claude Code, or equivalent AI-assisted design execution, and must be linked from the page mockup approval package and relevant AI task packets.

- Project/site name:
- Prompt package version/date:
- Target execution path: Figma Make, Claude Design, JSON low/high-fidelity spec by Codex or Claude Code, coded HTML/CSS mockup, clickable prototype, static screenshots, or hybrid:
- Accountable owner:
- Prompt reviewer:
- Prompt approver:
- Source artifact versions: PRD, sitemap/page briefs, URL inventory, content model, Conversion/SEO/Security Applicability Matrix, Design Artifact Strategy, Human Design Governance record, UX/UI Framework Compliance Matrix, SEO architecture, cybersecurity control matrix, WordPress CPT/admin model, forms/integrations, brand assets, accessibility/privacy requirements, analytics/conversion goals, technical constraints, relevant workplace UX/UI framework sections, UX laws/UI dos/don'ts source, anti-AI audit source, content resilience/WordPress visual QA source, and Human Design Scorecard source:
- Assumptions/gaps/exceptions:
- Human Design Governance record:
  - Design intent, hard guardrails, design principles, AI pattern warnings, design decision rationale links, brand specificity goals, content-driven composition strategy, systematic consistency rules, controlled variation rules, visual restraint level, responsive recomposition strategy, accessibility-as-design notes, and owner/reviewer approval.
- Anti-AI visual audit plan:
  - Project-specific cliches to watch, pattern budget, known common patterns intentionally allowed, pattern convergence risks, brand specificity test notes, swap-the-logo risk, restraint test scope, component justification scope, and required evidence.
- Human Design Scorecard plan:
  - Pages/templates to score, expected threshold, hard failure checks, reviewer, approver, and exception rules.
- Content resilience and WordPress visual QA plan:
  - Content cases, secondary templates/states, component differentiation scope, rendered visual QA viewports/tools, and evidence requirements.
- Low-fidelity wireframe decision and rationale:
- Page/template inventory:
  - Page/template ID, page name, type, source page brief, PRD IDs, selected artifact path, low-fidelity decision, SEO/security/accessibility notes, required breakpoints, required states, WordPress template/CPT mapping.
- Workflow inventory:
  - Flow ID, actors, entry point, steps, decisions, success path, failure paths, edge states, owner approval need.
- Component/widget/menu inventory:
  - Component ID, usage, variants, states, icon/button/menu behavior, accessibility behavior, responsive behavior, WordPress/CMS dependency.
- Domain-specific feature inventory:
  - Feature, domain concept, user goal, data/content dependency, UI behavior, trust/compliance notes.
- UX laws and UI dos/don'ts constraints:
  - Relevant laws/rules, affected pages/templates/components/states, prompt instruction, expected evidence, exception/risk if not applied.
- WordPress/CMS/admin requirements:
  - CPT screens, custom metadata fields, media/photo upload fields, taxonomy selectors, preview behavior, content-author controls, block-builder exception status.
- SEO/accessibility/security/privacy/conversion/trust/local requirements to express in designs:
- Tool/agent execution instructions and prompt-splitting plan, if prompt limits apply:
- JSON specification instructions, if JSON wireframes/specs are used:
- Coded mockup instructions, if coded HTML/CSS mockups are used:
- Final AI design tool prompt text:
- Generated output audit checklist:
  - Every launch-scope page/template exists at desktop, tablet, and mobile, or an approved responsive exception exists.
  - If separate low-fidelity wireframes were skipped, the selected artifact path still proves structure, hierarchy, flows, states, and responsive behavior.
  - UX/UI Framework Compliance Matrix rows for the relevant pages/templates are classified and evidenced or exception-approved.
  - Human Design Governance rows are applied, evidenced, or exception-approved.
  - Anti-AI visual audit is complete, pattern convergence is justified or remediated, brand specificity/swap-the-logo/restraint/component tests pass or have approved exceptions.
  - Human Design Scorecard has no hard failures and scores 90+ or has approved revision/exception handling.
  - Content resilience and WordPress visual completeness cases are represented.
  - Relevant UX laws and UI dos/don'ts constraints are represented in hierarchy, choices, controls, spacing, feedback states, forms, mobile/touch behavior, onboarding, search, and completion moments.
  - Every listed workflow, action, behavior, state, widget, menu, icon, button, form, and domain-specific feature is represented.
  - Content hierarchy, CTAs, headings, internal links, and SEO intent are preserved.
  - Accessibility states, labels, focus order, contrast risks, target sizes, motion rules, and error handling are represented.
  - Security/privacy UX for forms, uploads, accounts, consent, rate limits, and safe error states is represented.
  - WordPress template, CPT, custom metadata, and admin/editor behavior are buildable.
- Owner review/rework log:
- Approved prompt version and approval record:
- Linked generated mockup package:
## Website Page Mockup Approval Package

Use this before main WordPress/theme/template coding begins. Every launch-scope page or reusable page template needs owner-approved mockup evidence unless the sponsor/product owner records an exception.

Sequence rule:
- Create this package after the PRD baseline, page briefs, sitemap, Design Artifact Strategy, UX/UI Framework Compliance Matrix, and AI design-tool prompt package exist, and before final SRD/SRS baseline and main WordPress/theme/template coding.
- Use early technical constraints where needed, but do not let a technical draft replace owner approval of the actual page mockups.

- Project/site name:
- PRD baseline/version:
- SRD/SRS baseline/version, if available; final SRD normally follows the approved mockup baseline:
- Sitemap/page inventory version:
- Website owner/client approver:
- Product owner:
- Design reviewer:
- Accessibility reviewer:
- Frontend/CMS feasibility reviewer:
- Mockup format: Figma Make output, Claude Design output, JSON low/high-fidelity wireframe spec, coded HTML/CSS mockup, clickable prototype, static screenshot set, or other reviewable artifact.
- Page/template mockup table:
  - Page/template ID, page name, page type, source page brief, PRD IDs, SRD IDs if known, selected layout, selected design direction, desktop mockup link, tablet mockup link, mobile mockup link, required states, content dependencies, owner feedback status, approval status, approved version, approved date.
- Required review rounds:
  - Initial owner review.
  - Rework round for owner feedback.
  - Accessibility/design feasibility review.
  - Final owner approval.
- Revision log:
  - Date, page/template ID, feedback source, requested change, action taken, decision, owner, status.
- Build-release rule:
  - No main WordPress theme, page-template, CPT-template, or frontend implementation ticket may start until the relevant page/template mockup is approved or an exception is recorded.
- Exception log:
  - Page/template ID, missing approval or deferred mockup, reason, risk, sponsor/product-owner approver, expiry/review date.
- Acceptance checklist:
  - Every launch-scope page/template has a mockup.
  - Desktop, tablet, and mobile behavior are reviewable, or an approved responsive exception is recorded.
  - Low-fidelity wireframes were produced where required, or explicitly skipped through the approved Design Artifact Strategy with equivalent structure proof.
  - UX/UI Framework Compliance Matrix rows for the page/template are applied, not applicable with rationale, or exception-approved.
  - Relevant UX laws and UI dos/don'ts rows are applied, not applicable with rationale, or exception-approved.
  - Human Design Governance hard guardrails, design principles, and AI pattern warnings are applied, not applicable with rationale, or exception-approved.
  - Anti-AI visual audit, brand specificity, swap-the-logo, restraint, and component justification tests pass or have approved remediation/exception.
  - Human Design Scorecard has no hard failures and meets pass threshold or has accountable approved exception.
  - Content resilience and WordPress visual completeness evidence covers relevant page/templates/states.
  - Required states are covered, including forms, errors, empty states, search/filter states, auth/account states, checkout/payment states, or admin/editor states where applicable.
  - Mockups or equivalent design baseline artifacts map to the Design Artifact Strategy, UX/UI Framework Compliance Matrix, AI design-tool prompt package, page briefs, PRD IDs, and planned WordPress templates.
  - Website owner feedback is captured page by page.
  - Rework is completed or formally rejected/deferred.
  - Website owner approval is explicit, dated, and linked to the approved version.
  - Design baseline is frozen and change control is active.

## Human Design Governance Record

Use this before high-fidelity design prompt execution, generated mockup approval, coded mockup acceptance, or frontend implementation.

- Project/site name:
- Record version/date:
- Accountable UX/UI/brand owner:
- Reviewer:
- Approver:
- Source artifacts: PRD, sitemap/page briefs, content model, brand assets, Design Artifact Strategy, UX/UI Framework Compliance Matrix, UX laws/UI dos-don'ts source, Human Design Governance source, anti-AI visual audit source, content resilience/WordPress visual QA source, and Human Design Scorecard source:
- Rule class coverage:
  - Hard guardrails, status, evidence, exceptions/mitigation/expiry.
  - Design principles, status, evidence, exceptions/rationale.
  - AI pattern warnings, status, rationale, mitigation.
- Design intent:
  - Visual character, emotional tone, information density, brand expression, typography direction, color direction, image direction, composition direction, motion direction, interaction tone, visual restraint level, and project-specific visual cliches to avoid.
- Design decision rationale:
  - Decision, reason, alternative rejected, reason rejected, affected page/template/component, evidence.
- Human design acceptance questions:
  - Weak answers, revisions required, owner/reviewer decision.
- Approval record:

## Anti-AI Visual Audit Package

Use this before final page/template mockup approval, coded mockup acceptance, and frontend launch-scope acceptance.

- Page/template/component:
- Reviewer:
- Pattern catalogue findings:
  - Pattern, location, justified yes/no, rationale, action.
- Pattern convergence audit:
  - Patterns accumulated, justified patterns, habitual patterns, redesign/removal actions, recheck status.
- Pattern budget notes:
- Brand specificity test result:
- Swap-the-logo test result:
- Restraint test result:
- Component justification results:
- Project-specific anti-pattern risks checked:
- Approved exceptions:
- Evidence links:

## Human Design Scorecard Record

Use this before accepting major page/template mockups, coded mockups, or implemented UI.

| Category | Max | Score | Evidence/notes |
|---|---:|---:|---|
| Brand specificity | 10 | | |
| Information hierarchy | 10 | | |
| Content-driven composition | 10 | | |
| Typography | 8 | | |
| Color rationale | 6 | | |
| Imagery and iconography | 8 | | |
| Component appropriateness | 8 | | |
| Layout rhythm and composition | 8 | | |
| Responsive recomposition | 10 | | |
| Accessibility | 10 | | |
| Content resilience | 5 | | |
| WordPress completeness | 4 | | |
| Interaction and motion | 3 | | |
| Total | 100 | | |

- Hard failures present: yes/no.
- Hard failure notes:
- Result: pass, revise, or fail.
- Required revisions:
- Accepted exceptions:
- Evidence links:
- Approver:

## Content Resilience and WordPress Visual QA Package

Use this before final design acceptance, frontend QA, UAT, and launch readiness.

- Page/template/component:
- Content resilience cases tested:
- WordPress templates/states checked:
- Component differentiation checks:
- Viewports/rendering tools used:
- Desktop/tablet/mobile/high-zoom evidence:
- Interaction/focus state evidence:
- Long content/missing media evidence:
- Visual defects found:
- Fixes made:
- Remaining exceptions:
- Reviewer:
- Approver:
## SEO Crawl and Compliance Audit Package

Use this before launch for WordPress/CMS projects and whenever AI is asked to improve SEO. The AI must crawl the full applicable website, remediate what is practical within the approved scope, and target 90%+ SEO audit scores or document approved exceptions.

- Project/site name:
- Environment audited: local, staging, production, or other:
- Base URL:
- Crawl date/time:
- Auditor/AI run ID:
- Source artifacts: PRD, SRD/SRS, sitemap, page briefs, Conversion/SEO/Security Applicability Matrix, AI design-tool prompt package, approved mockups, CPT model, URL map, redirect map:
- SEO reference used: references/seo-crawl-compliance-workflow.md and references/generic-ai-seo-compliance-prompt-for-any-website-architecture.txt:
- Target score: 90%+ Lighthouse/PageSpeed SEO or equivalent audit score, unless exception is approved:
- Browser/rendering coverage:
  - Chromium/Chrome/Edge result:
  - Firefox result, if available:
  - WebKit/Safari result, if available:
  - Unavailable browser engines and reason:
- Crawl scope:
  - XML sitemap URLs:
  - Homepage-discovered URLs:
  - Navigation/footer URLs:
  - Pages/posts:
  - CPT singles/archives:
  - Taxonomies/categories/tags:
  - Pagination:
  - Search/filter/faceted URL patterns:
  - Legacy redirect URLs:
  - Excluded/private/noindex URLs:
- URL audit matrix:
  - URL, template, content type, status code, index/noindex, canonical target, sitemap inclusion, title, meta description, H1, schema, internal links, image alt status, performance note, issue severity, fix status.
- Structured data validation:
  - Page/template, schema type, validation result, warnings, errors, misuse risk, fix status.
- Metadata/social preview validation:
  - Title, description, canonical, robots, Open Graph, social image, fallback behavior, fix status.
- Core Web Vitals/performance SEO checks:
  - LCP, INP, CLS, mobile performance, image sizing/compression, script/font/third-party risk, cache/CDN status.
- Remediation log:
  - Issue ID, URL/template, severity, change made, files/settings/content changed, check rerun, result, owner.
- Exceptions:
  - Issue, reason not fixed, risk, approver, review/expiry date.
- Final SEO Compliant Build Specification:
  - Exact SEO behavior the website now implements before launch.

## SEO Score and Browser Evidence Matrix

| URL/template group | Tool/browser | SEO score | Target met? | Critical issues | Evidence | Exception/owner |
|---|---|---:|---|---|---|---|


## WordPress CPT Admin UI Specification

Use this whenever creating or modifying WordPress project CPTs. The default policy is no Gutenberg/block builder for project CPT authoring.

- CPT name and slug:
- Business purpose:
- Public URLs/archive/single behavior:
- Admin menu label and icon:
- Block editor policy: disabled by default; exception approver/reason if enabled:
- Registration controls: `supports`, `show_in_rest`, `capability_type`, `map_meta_cap`, REST exposure, and `use_block_editor_for_post_type` behavior:
- Taxonomies:
- Metabox groups:
- Metadata fields table:
  - Field key, label, type, required, default, validation, sanitization, escaping, permissions, storage, display template, acceptance criteria.
- Photo/media upload fields:
  - Field key, allowed media type, single/multiple, attachment ID storage, preview behavior, replace/remove behavior, alt text/caption guidance, fallback behavior.
- Nonce and permission checks:
- Save/update/delete behavior:
- Admin list columns and filters:
- Preview/rendering behavior:
- QA checks:
  - Add screen opens custom metadata UI, not block builder.
  - Edit screen opens custom metadata UI, not block builder.
  - Required fields validate.
  - Media uploader opens, selects, previews, replaces, removes, and saves attachment IDs.
  - Metadata is sanitized, escaped, saved, rendered, and permission-protected.
  - Save handlers verify nonces, capabilities, autosave/revision handling, allowed uploads, and prepared queries where custom SQL exists.
  - Approved exceptions are documented.

## Human Supervision Matrix

| Work class | AI may draft | AI may execute | Human reviewer | Human approver | Human-only decision? | Notes |
|---|---:|---:|---|---|---:|---|
| Product scope | Yes | No | PDM/PO | PDM/SP | Yes | |
| AI design prompt package and page mockups/UI approval | Yes | Prompt execution/revision only | UX-D/UI/ACC/FE/CMS/SEO/SEC | Website owner/PO | Yes | Main WordPress/theme/template coding waits for approved prompt package and owner-approved mockups. |
| SEO architecture/crawl exceptions | Yes | Yes, within approved task packet | SEO/FE/CMS/QA | SEO/PO/SP | Yes for launch exceptions | Target 90%+ audit score or approved exception. |
| Cybersecurity architecture/coding exceptions | Yes | Yes, within approved task packet | SEC/SA/FE/BE/CMS/DEVOPS/QA | SEC/SA/PO/SP | Yes for critical/high risk | Critical/high findings, encryption gaps, exposed secrets, SQL injection, authz failures, unsafe uploads, or launch security exceptions need human risk acceptance. |
| Architecture | Yes | No | SA/SEC/SRE | SA | Yes | |
| Code/config | Yes | Yes | FE/BE/CMS/DEVOPS/QA | Technical owner | No, except sensitive areas | |
| Security/privacy/legal | Yes | No | SEC/PRIV/LEGAL | Accountable specialist | Yes | |
| Production deploy | No | No | DEVOPS/SRE/QA | SP/DEVOPS/SRE | Yes | |

## AI Tool Permission Matrix

| Tool/system | Allowed AI access | Human approval required | Data restrictions | Logging/evidence | Owner |
|---|---|---:|---|---|---|
| Repository | Read/write by task packet | Yes for protected branches | No secrets | Diff, tests, review | DEVOPS |
| CMS | Staging only by default | Yes | No private data | Change log, screenshots | CMS |
| Hosting/production | Read-only by default | Yes | No secrets in AI context | Deployment evidence | DEVOPS/SRE |
| Analytics | Read-only sanitized | Yes | No raw PII | Report links | DATA |
| Email/payment/DNS | No direct mutation | Always | No live credentials | Approval record | OPS/FIN/DEVOPS |

## AI Run Log Entry

- Run ID:
- Date/time:
- Task packet ID:
- Agent/tool/model version where known:
- Prompt/context summary:
- Files/artifacts changed:
- Commands/checks run:
- Test results:
- Evidence links:
- Cost/usage if available:
- Self-review result:
- Independent review result:
- Human approval:
- Open risks:
- Next action:

## Requirements-to-Test Matrix

| Requirement ID | Source | Test/review/demo | Evidence | Status | Owner | Exception/accepted risk |
|---|---|---|---|---|---|---|

## AI-Generated Work Review Matrix

| Change/task | Task packet | Requirement IDs | Self-review | Independent review | Required checks | Human approval | Status |
|---|---|---|---|---|---|---|---|

## Launch Evidence Checklist

- WordPress AI flow gate evidence register is current; all required gates are passed, deferred by approved exception, or blocked from launch.
- PRD/SRD baselines current.
- Launch-scope requirements accepted, deferred, or risk-accepted.
- Design Artifact Strategy, Human Design Governance record, UX/UI Framework Compliance Matrix, UX laws/UI dos-don'ts coverage, anti-AI visual audit, Human Design Scorecard, content resilience/WordPress visual QA evidence, AI design-tool prompt package, owner-approved page mockup/design baseline package, and frozen design baseline exist for all launch-scope pages/templates.
- Conversion/SEO/Security Applicability Matrix is complete; compulsory defaults and triggered contextual items are implemented or excepted.
- Full-site SEO crawl and remediation evidence exists, with 90%+ SEO audit target met or exceptions approved.
- WordPress cybersecurity evidence package is complete; critical/high findings are fixed or accepted by accountable humans with mitigation and expiry.
- Requirements-to-test matrix complete.
- AI-generated work review matrix and AI execution posture checklist are complete, if AI delivery was used.
- Human approvers signed off by work class.
- QA/UAT exit met.
- Accessibility/security/privacy/performance/SEO/analytics release statuses accepted.
- Rollback tested.
- Monitoring and alerts live.
- Support, operations, sales, and marketing ready.
- AI tools have no unauthorized production, secrets, payment, DNS, email, or customer data access.



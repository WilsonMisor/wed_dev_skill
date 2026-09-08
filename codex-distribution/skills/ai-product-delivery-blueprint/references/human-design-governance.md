# Human Design Governance

Use this reference when planning, prompting, generating, reviewing, or implementing WordPress website design artifacts, mockups, coded prototypes, theme templates, content sections, custom post type templates, admin/editor UI, visual QA, or launch evidence.

This reference operationalizes `codex_wordpress_human_design_governance_update.md`. It is an added governance layer for the existing AI Web Delivery Blueprint. It does not replace the PRD/SRD, UX/UI Framework Compliance Matrix, UX laws/UI dos and don'ts, SEO workflow, cybersecurity workflow, accessibility requirements, or WordPress implementation rules.

## Core Principle

All generated WordPress interfaces must demonstrate deliberate, context-specific design. Do not use a visual treatment simply because it is a common modern website pattern or a frequent AI-generated pattern. Every significant design decision must be defensible through user needs, content, information hierarchy, brand identity, business objectives, conversion objectives, accessibility, interaction requirements, responsive behavior, or the established design system. Generic visual novelty is not sufficient justification.

Consistency is not evidence of AI design. Professional design should use coherent systems for spacing, typography, color, radius, grid, motion, and components. Avoiding the AI look must never result in random inconsistency.

Human design feel is produced by intentionality, brand specificity, content-driven composition, realistic content handling, responsive recomposition, accessibility, and considered restraint. It is not produced by arbitrary asymmetry, unusual fonts, overlap, inconsistent spacing, or decorative complexity.

Familiar patterns are often appropriate. Navigation, forms, search, buttons, tables, filters, links, and other common interactions should remain predictable when predictability improves usability. Originality should come primarily from brand expression, content, hierarchy, composition, imagery, typography, information density, and selective interaction, not from making basic controls unfamiliar.

## Rule Classes

### Hard Guardrails

Hard Guardrails are mandatory unless a technical, legal, accessibility, or project requirement makes compliance impossible. Exceptions require accountable human approval, rationale, mitigation, and expiry/review date where risk remains.

- Do not introduce random visual inconsistency merely to make a site appear human designed.
- Do not treat mobile responsiveness as simple vertical stacking.
- Do not allow a visually polished homepage while leaving major WordPress templates unstyled.
- Do not accept material accessibility failures.
- Do not use generic placeholder content as the basis for final design approval.
- Do not use arbitrary visual effects that have no user, content, brand, hierarchy, interaction, or conversion justification.
- Do not mark a visual interface complete without visual inspection where rendering tools are available.
- Do not silently invent brand characteristics that contradict provided brand information.
- Do not create a visual language that is interchangeable across unrelated industries when the project contains enough information to create a more specific identity.
- Do not ignore realistic WordPress content variation.

### Design Principles

Design Principles are strong defaults that guide decisions. They may have justified exceptions.

- Content should determine component choice.
- Information hierarchy should determine visual hierarchy.
- Brand identity should influence typography, color, imagery, shape, density, layout, and motion.
- Design systems should provide consistency.
- Variation should come from content, hierarchy, and purpose rather than randomness.
- Visual restraint should be preferred over unnecessary decoration.
- Responsive layouts should be recomposed according to device constraints.
- Imagery should communicate information or brand meaning.
- Motion should communicate state, relationship, emphasis, progress, or feedback.
- Familiar interaction patterns should remain familiar when familiarity improves usability.

### AI Pattern Warnings

AI Pattern Warnings identify common patterns that may contribute to generic AI appearance. They are not automatic bans. A pattern may be used when it is appropriate, justified, accessible, responsive, and brand/content aligned. Require review when several warnings accumulate on the same page, viewport, or template group.

## Mandatory Human Design Workflow

Use this workflow inside the existing PRD -> page briefs/sitemap -> Design Artifact Strategy -> UX/UI Framework Compliance Matrix -> prompt package -> mockup/design baseline -> SRD -> coding sequence. If the project already supplies validated outputs for an earlier stage, verify and cite them instead of regenerating them.

1. Project discovery: identify or derive organization/product, industry, audiences, user groups, user needs/problems, business objectives, website objectives, primary/secondary conversions, trust requirements, content requirements, brand attributes/assets, accessibility requirements, technical constraints, WordPress constraints, content management needs, and legal/regulatory constraints where applicable. Use conservative assumptions and record gaps.
2. Information architecture: define sitemap, navigation hierarchy, page purposes, user journeys, conversion journeys, content hierarchy, page relationships, archives, CPT relationships, search/discovery, taxonomies, and footer IA. Do not begin from a decorative homepage template.
3. Content model: identify required content types before selecting layouts, such as narrative text, services, products, case studies, projects, team, testimonials, statistics, evidence, CTAs, images, video, maps, documents, FAQs, processes, timelines, events, articles, tables, comparisons, and forms. Do not decide content should become cards before understanding the content model.
4. Design intent: create a concise, project-specific intent before high-fidelity styling. Define visual character, emotional tone, information density, brand expression, typography direction, color direction, image direction, composition direction, motion direction, interaction tone, visual restraint level, and project-specific visual cliches to avoid. Avoid vague words such as modern, clean, professional, sleek, beautiful, and innovative unless paired with concrete visual interpretation.
5. Low-fidelity structure or equivalent structure proof: solve content order, hierarchy, navigation, conversion path, section relationships, major component selection, and responsive priorities before decorative styling.
6. Design system: define or use coherent tokens for color, typography, spacing, grid, container widths, border radius, borders, shadows, motion, breakpoints, interactive states, focus states, form states, image treatment, and icon treatment. Do not create arbitrary one-off values without justification.
7. High-fidelity composition: apply design intent and system to actual content. Let layout respond to content hierarchy instead of forcing every section into the same module.
8. Responsive recomposition: design major components across large desktop, desktop, tablet landscape, tablet portrait, large mobile, small mobile, and high browser zoom where feasible. Reevaluate order, priority, crops, visibility, interaction, CTAs, navigation, type, density, touch targets, overflow, tables, filters, forms, and media. Do not assume columns merely stack.
9. WordPress implementation: implement the validated design using the existing WordPress architecture and coding rules. Do not let implementation convenience erase design hierarchy.
10. Visual QA: where rendering tools are available, run the site, inspect desktop/tablet/mobile/high-zoom where feasible, inspect interaction/focus/content/media/template states, correct defects, and repeat. Code review alone is not sufficient evidence of visual quality.
11. Anti-AI visual audit: run the pattern convergence audit, pattern budget review, brand specificity test, swap-the-logo test, restraint test, component justification review, and project-specific anti-pattern check.
12. Human Design Score: score major pages/templates with the scorecard. Resolve hard failures first. A score of 90-100 passes, 80-89 requires revision before final acceptance, and below 80 fails.

## Design Decision Rationale

Record lightweight rationale for major visual decisions. Keep it short; the goal is to prevent arbitrary styling.

Use this format:

```text
Decision:

Reason:

Alternative rejected:

Reason rejected:
```

Rationale should exist for major pages/templates and for significant decisions involving hero structure, layout model, typography, color approach, image treatment, section transitions, major components, navigation, responsive behavior, and important motion or interaction. It may remain internal unless the user asks to see it.

## Human Design Principles

### Intentional Hierarchy

Make it clear what users should notice first, second, and third. Do not give equal visual weight to all content. Use size, position, contrast, typography, spacing, color, image scale, density, motion, and grouping to express hierarchy.

### Content-Driven Composition

Select layout based on what users must understand, compare, scan, trust, or act upon. Valid formats include plain text, editorial layout, feature section, cards, list, timeline, comparison, table, statistics, diagram, quote, gallery, map, accordion, tabs, process, case study, story, media feature, and form. Choose the format because it fits the content, not because it is a common web pattern.

### Brand Specificity

Typography, imagery, color, density, layout, shape, illustration, and motion should support the actual organization or product. Avoid generic industry stereotypes when project information permits a more specific identity.

### Systematic Consistency

Use design systems, reusable tokens, consistent spacing scales, grids, standardized components, consistent radii, reusable typography styles, shared states, and reusable breakpoints. These are strengths. The problem is mechanical application without context, not consistency itself.

### Controlled Variation

Variation should come from content type, hierarchy, user task, narrative position, interaction need, information density, or brand emphasis. Standard text may use a narrow reading width; a case study may split text and imagery; statistics may use a wider composition; a quotation may use an offset narrow composition; a gallery may use full-width media. All can still use the same grid and token system.

### Purposeful Restraint

Do not decorate every section. A heading, paragraph, and whitespace may be the right solution. Add icons, gradients, blobs, shadows, cards, background colors, animation, or decorative SVGs only when they improve communication, hierarchy, brand expression, interaction, or user experience.

### Semantic Components

Components must have an information or interaction reason. Cards normally represent discrete, comparable, reusable, or independently actionable objects. Do not wrap every content block in a card merely to make the interface appear designed.

### Realistic Content

Design with realistic content lengths and media characteristics. Do not depend on artificially equal text blocks. Designs must tolerate irregular real-world WordPress content.

### Responsive Recomposition

Responsive design is not shrinking and stacking. Each breakpoint should preserve hierarchy, meaning, functionality, readability, interaction quality, and conversion priority.

### Accessibility As Design

Accessibility must influence visual decisions from the beginning. Consider contrast, focus visibility, text sizing, line height, line length, reflow, keyboard interaction, motion preferences, form clarity, touch targets, semantic structure, and error communication.

## Acceptance Questions

Before final approval, answer internally:

- What is the primary user task on this page?
- What should the user notice first and second?
- What is the primary conversion?
- Why does this page use this layout, typography, color treatment, and imagery?
- Why does each major component exist?
- Which decisions are brand specific?
- Which common patterns were used, and why were they appropriate?
- Which generic patterns were rejected?
- Does mobile preserve the correct priorities?
- Does the page remain usable with realistic content?
- Does the design system remain coherent?
- Is any decoration unnecessary?
- Could the page belong to an unrelated organization after a logo swap?
- Are secondary WordPress states equally considered?
- Does the rendered output match the design intent?

If several answers are weak or generic, revise before approval.
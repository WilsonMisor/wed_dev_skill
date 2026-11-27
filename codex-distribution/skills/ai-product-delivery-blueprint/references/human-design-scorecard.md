# Human Design Scorecard

Use this reference before accepting major WordPress pages/templates, generated mockups, coded mockups, or implemented UI. The scorecard is an acceptance tool, not a substitute for hard guardrails, accessibility, SEO, security, owner approval, or WordPress implementation quality.

Resolve hard failures before scoring. The total score cannot override a hard failure.

## Score Weighting

| Category | Maximum Score |
| --- | ---: |
| Brand specificity | 10 |
| Information hierarchy | 10 |
| Content-driven composition | 10 |
| Typography | 8 |
| Color rationale | 6 |
| Imagery and iconography | 8 |
| Component appropriateness | 8 |
| Layout rhythm and composition | 8 |
| Responsive recomposition | 10 |
| Accessibility | 10 |
| Content resilience | 5 |
| WordPress completeness | 4 |
| Interaction and motion | 3 |
| Total | 100 |

## Scoring Rules

- 90 to 100: Pass.
- 80 to 89: Revise weak areas before final acceptance.
- Below 80: Fail. Redesign and reassess.

Do not average away a serious blocker. Record evidence, reviewer, approver, revision notes, and unresolved exceptions.

## Category Guidance

- Brand specificity: typography, color, imagery, tone, density, shape language, and composition reflect the actual organization/product rather than a generic industry template.
- Information hierarchy: the page makes clear what users should notice first, second, and third, and the conversion path is visible.
- Content-driven composition: layouts and components match the content model and hierarchy.
- Typography: type supports brand character, readable measure, hierarchy, line height, responsive scaling, long headings, long words, uppercase labels, accessible contrast, and high zoom.
- Color rationale: color choices follow brand, semantic meaning, contrast, controlled accent use, background relationships, and interactive/error/warning/success/info states.
- Imagery and iconography: visuals add information, evidence, emotion, or brand meaning; icons are semantically useful and restrained.
- Component appropriateness: components solve a real content or interaction problem and are not selected by habit.
- Layout rhythm and composition: grids are deliberate, spacing is systematic but not mechanical, and variation follows hierarchy/content.
- Responsive recomposition: major components intentionally adapt across viewports and high zoom rather than merely stacking.
- Accessibility: accessibility is designed into visual decisions and critical issues are resolved.
- Content resilience: realistic WordPress content variation does not break layout.
- WordPress completeness: launch-scope templates and states receive deliberate design attention beyond the homepage.
- Interaction and motion: states, feedback, hover/focus, loading, and motion serve purpose and respect reduced motion.

## Hard Failure Conditions

The page or implementation fails review when any of these materially applies:

1. Mobile is treated only as stacked desktop.
2. Critical accessibility requirements are materially broken.
3. Major WordPress templates are visually unfinished.
4. Generic placeholder imagery remains in final production output without explicit user approval.
5. Major interactive states are missing.
6. Content resilience is poor enough that realistic content breaks the layout.
7. The design ignores the supplied brand system.
8. Arbitrary visual inconsistency was introduced merely to appear human designed.
9. The implementation materially diverges from the approved design intent without justification.
10. Major layout or interaction problems are visible during rendering.
11. The page is dominated by accumulated generic AI patterns without project-specific justification.
12. The interface looks polished but fails to communicate the page purpose or conversion path.

Hard failures require redesign, remediation, or accountable human exception. Accessibility, legal, security, privacy, production, and owner approval decisions remain human-only under the main skill.

## Scorecard Record

Use this compact record:

```text
Page/template:
Reviewer:
Date:
Hard failures present: yes/no
Hard failure notes:
Scores by category:
Total:
Result: pass / revise / fail
Required revisions:
Accepted exceptions:
Evidence links: screenshots, prototype, URL, audit notes
Approver:
```
# AI Visual Antipatterns and Audit

Use this reference when choosing layouts/components, creating design intent, writing AI design prompts, auditing generated mockups, reviewing coded UI, or deciding whether a page feels generic. These are warnings, not bans. Common patterns are allowed when appropriate and justified.

For every warning, ask:

- Is this appropriate for this content?
- Is this supported by the brand?
- Does it improve hierarchy or usability?
- Is it being repeated mechanically?
- Is there a more content-specific treatment?
- Is this accumulating with several other generic AI patterns?

## Pattern Catalogue

1. Generic hero formula: eyebrow pill, huge headline, one gradient word, short paragraph, two CTAs, generic stock image, logo strip.
2. Card soup: services, benefits, statistics, testimonials, process steps, contact information, articles, and team members all placed in similar cards by default.
3. Repeated three-column sections across unrelated content types.
4. Excessive rounded rectangles across buttons, cards, images, forms, icons, statistics, CTAs, and navigation.
5. Excessive decorative pill elements.
6. Generic technology gradients: purple, blue, cyan, indigo, neon, or blurred gradients used merely to signify technology or modernity.
7. Decorative gradient blobs or circles used to fill empty space.
8. Glass effects without visual and usability justification.
9. Repeated literal iconography such as shield for security, globe for global, clock for time, heart for healthcare, people for community, light bulb for innovation, or rocket for growth.
10. Repeated icon-inside-rounded-square plus heading plus two-line text pattern.
11. Generic stock photography that could belong to any organization, such as handshake, businesspeople around laptop, customer service headset, doctor with tablet, smiling team, skyline, charity imagery, African entrepreneur, or office meeting.
12. Images that merely repeat the heading instead of adding information, evidence, emotion, or brand meaning.
13. Artificially equal text lengths created only for visual symmetry.
14. Mechanical vertical rhythm: identical section padding repeated without hierarchy or relationship logic.
15. Alternating white and light gray sections without a content reason.
16. Same container width everywhere, regardless of reading, imagery, statistics, media, forms, tables, or editorial needs.
17. One typeface with generic weight changes but no intentional scale, measure, rhythm, hierarchy, or brand character.
18. Trend-driven font pairing selected because it appears frequently in modern interfaces.
19. Excessive fade-up animation on every section.
20. Universal hover lift on every card.
21. Universal button scale on every button.
22. Motion without meaning.
23. Excessive sectioning where every idea becomes a full-width section.
24. Template-like narrative: Hero, About, Features, Benefits, Process, Statistics, Testimonials, FAQ, CTA, Footer used by default.
25. Generic navigation such as Home, About, Services, Blog, Contact, CTA when the actual IA suggests better labels or hierarchy.
26. Desktop-first stacking treated as mobile completion.
27. Overly spacious layouts where whitespace substitutes for hierarchy.
28. Every section attempts to impress through decoration, animation, imagery, or color.
29. Generic trust logo strip without real trust evidence.
30. Generic statistics strip using arbitrary counters for visual interest.
31. Generic testimonial carousel when a carousel is not appropriate to content or user experience.
32. Generic FAQ accordion created because landing pages often contain FAQs.
33. Generic CTA banner disconnected from the conversion journey.
34. Decorative dashed lines and connector graphics added to make a process look visual.
35. Generic dot patterns used as texture without a design-language reason.
36. Excessive gradient text as a default attention mechanism.
37. Excessive badges such as Trusted, New, Best, Premium, Innovation, Future Ready where they do not communicate real information.
38. Repeated component shell for unrelated content types because it simplifies implementation.
39. Generic empty states that ignore actual user context and next actions.
40. Polished homepage with weak secondary templates.

## Pattern Convergence Audit

Do not evaluate warnings only one at a time. A page should trigger mandatory review when several generic patterns appear together in the same viewport, page, or template group.

Example convergence set:

```text
Inter
Purple gradient
Rounded cards
Lucide-style icons
Three-column services
Pill badges
Generic stock image
Fade-up animation
Alternating gray sections
Rounded CTA banner
```

Each item may be valid alone. Together they create a strong generic AI signature.

When convergence is detected:

1. List the patterns.
2. Identify which patterns are justified.
3. Identify which patterns are merely habitual.
4. Remove or redesign unjustified patterns.
5. Preserve useful conventions.
6. Recheck brand specificity.
7. Recheck hierarchy.
8. Recheck responsive behavior.

Do not replace all common patterns at once merely to be different.

## Pattern Budget

The pattern budget is not a numerical ban. It is a review trigger. The page may use familiar patterns, but each should have a reason. When several stereotypical AI visual patterns occur in the same viewport or page, ask whether the page has become statistically generic. Prefer fewer, better-justified visual ideas over a large collection of fashionable effects.

## Brand Specificity Test

Before final acceptance, ask: if the organization name and logo were removed, could this design easily belong to several unrelated organizations?

If yes, investigate typography, color, photography, illustration, content hierarchy, layout, image treatment, shape language, motion, content structure, CTAs, and tone. The page does not fail merely because it uses familiar conventions. It fails when the overall design lacks meaningful project-specific identity despite sufficient project information.

## Swap-The-Logo Test

Mentally substitute unrelated identities such as a law firm, NGO, fintech, property company, healthcare provider, and SaaS company. If the design works equally well for all of them with only a logo and color change, the visual direction is probably underdeveloped. Revise when project information supports greater specificity.

## Restraint Test

For each decorative element, ask whether removing it would reduce meaning, hierarchy, brand expression, navigation, trust, conversion, interaction, or comprehension.

Review decorative icons, gradient blobs, pills, shadows, borders, background decorations, repeated headings, decorative SVGs, animations, cards, and background color changes. If removal does not reduce anything important, consider removing it.

## Component Justification

Before creating a significant component, identify the problem it solves.

- Cards: appropriate when content items are discrete, comparable, reusable, or independently actionable. Potentially inappropriate for one continuous narrative or conceptual argument.
- Accordion: appropriate when users need optional access to secondary information and content remains discoverable. Potentially inappropriate when all information is important and should remain visible.
- Carousel: appropriate only when sequential or constrained browsing provides real value. Do not use a carousel merely to fit content into limited space.
- Tabs: use when content represents closely related alternative views or categories. Do not hide unrelated critical information behind tabs.
- Statistics: use when numbers provide evidence, comparison, or decision value. Do not add counters only for visual impact.
- Timeline: use when sequence and temporal order are meaningful.
- Comparison table: use when users genuinely need to compare attributes.

## Layout, Type, Color, Imagery, Icons, Motion

- Use grids deliberately. Do not avoid grid alignment to appear human designed. A consistent grid can support varied compositions.
- Vary composition within the grid by content need: narrow reading columns, split text/media ratios, full-width imagery, offset quotations, wide statistics, edge-extending media, and compact utility sections.
- Use asymmetry only when it improves hierarchy, composition, narrative, brand expression, or emphasis.
- Use overlap only when it improves visual storytelling and remains robust across responsive layouts and zoom.
- Avoid arbitrary visual exceptions; exceptions to the design system need a reason.
- Do not define human design as unusual typography. Familiar fonts such as Inter, Roboto, Poppins, Open Sans, Montserrat, or system fonts are acceptable when justified and should not be selected automatically either.
- Use color systems that are brand-relevant, accessible, semantic, controlled, and clear across backgrounds and interactive/error/warning/success/info states. Do not use purple/blue/cyan/neon/gradients merely because the project involves technology; do not ban them when they belong to the brand.
- Prefer deliberate imagery: real products, people, locations, projects, services in context, facilities, events, outcomes, original diagrams, or brand-specific illustration. If stock imagery is necessary, select it for brand support, consistent treatment, crop, perspective, lighting, subject, and context.
- Icons should support comprehension. Use consistent icon family/weight where appropriate, clear semantic meaning, accessibility treatment, restraint, and avoid unnecessary icon containers.
- Motion must serve state change, relationship, navigation, feedback, emphasis, spatial orientation, progress, or direct manipulation. Avoid universal entrance animations and identical hover effects on every component. Respect reduced motion.

## Project-Specific Warning Selection

During design intent, identify the AI visual cliches most likely to affect this project.

- Technology risks: purple-blue gradients, neon glows, glass effects, abstract grid backgrounds, dashboard mockups, rocket icons, generic future language.
- NGO risks: generic smiling beneficiary photography, repeated impact statistics, generic donation CTA, globe/heart icons, stock volunteering imagery, emotional imagery without evidence.
- Finance risks: navy/green default palette, generic upward charts, shield icons, excessive trust badges, generic stock market imagery.
- Healthcare risks: blue/white palette by default, heart icons, doctor with tablet, generic medical stock imagery, excessive clean white cards.

The purpose is conscious selection, not prohibition.

## Reasoning Examples

Bad: Six benefits are displayed as six identical cards because a card grid is easiest.
Better: Two primary benefits receive larger explanatory feature sections and four supporting benefits appear in a compact list.
Reason: The information hierarchy contains two major benefits and four secondary benefits; equal cards would falsely communicate equal importance.

Bad: A technology company receives a purple and blue gradient because those colors are common in technology websites.
Better: Color is derived from the brand system, competitive context, product positioning, accessibility requirements, and desired emotional tone.
Reason: Technology is not a visual identity.

Bad: Mobile layout is created by setting every grid to one column.
Better: The mobile version changes order, image crop, CTA placement, spacing, and navigation behavior where needed.
Reason: Responsive design preserves user priorities rather than merely stacking boxes.

Bad: Random border radius values are added to make the design feel handcrafted.
Better: The design uses a small set of radius tokens; components use those tokens according to role.
Reason: Professional human design is systematic.

Bad: Every section receives an icon, gradient, card, or animation.
Better: Several sections use only typography and whitespace; visual emphasis is reserved for moments that need it.
Reason: Restraint strengthens hierarchy.
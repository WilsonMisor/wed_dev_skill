# UX Laws and UI Dos/Don'ts Reference

Use this reference when creating, reviewing, or implementing UX/UI design artifacts, AI design-tool prompts, JSON wireframe/UI specs, coded mockups, page/template mockups, component states, forms, responsive layouts, onboarding flows, loading states, or design QA evidence.

This file operationalizes the two UX/UI source documents:

- `10_UX_Laws_Visual_Reference.docx`
- `20_UX_UI_Design_Dos_and_Donts.docx`

Treat these rules as practical heuristics, not as a replacement for the full workplace UX/UI framework. Apply them through the UX/UI Framework Compliance Matrix, prompt package, mockup audit, coded UI review, and developer handoff.

## 10 UX Laws

### 1. Jakob's Law

Core principle: users spend most of their time using other products, so they expect this product to feel familiar.

Apply it by:

- Use familiar navigation, content structures, controls, icon meanings, and interaction patterns.
- Reuse expected conventions unless a domain-specific reason justifies a new pattern.
- Avoid making users relearn basic navigation, search, profile/account, notification, form, or checkout behavior.
- Flag unusual patterns in design review and require rationale, testing evidence, or owner-approved exception.

Practical check: familiarity should reduce friction; novelty must solve a real problem.

### 2. Hick's Law

Core principle: the more choices users have, the longer they take to decide.

Apply it by:

- Reduce unnecessary equivalent options.
- Group related choices.
- Recommend a default or "best for you" option where the product has a defensible recommendation.
- Reveal advanced customization later instead of presenting every option at once.
- Avoid decision-heavy screens with too many visually equal options.

Practical check: fewer, clearer choices should speed decisions.

### 3. Fitts's Law

Core principle: time to reach a target depends on target size and distance.

Apply it by:

- Make important actions large enough to hit confidently.
- Put primary CTAs and repeated controls within easy reach, especially in mobile thumb zones.
- Separate important actions from destructive, secondary, or unrelated controls.
- Avoid tiny controls, cramped hit areas, and important actions placed far from the user's likely focus or hand position.
- Review touch target size, spacing, and reach during responsive QA.

Practical check: important actions should be easy to hit.

### 4. Miller's Law

Core principle: people can hold only a limited amount of information in working memory.

Apply it by:

- Break content into smaller chunks.
- Group related information into meaningful sections or steps.
- Use short sections, clear headings, and progressive disclosure for advanced material.
- Avoid presenting long undifferentiated blocks, especially in forms, onboarding, account setup, pricing, dashboards, and admin screens.

Practical check: chunk information to reduce memory load.

### 5. Proximity Law

Core principle: elements placed close together feel related.

Apply it by:

- Group labels with their fields.
- Use tighter spacing inside a group and larger spacing between groups.
- Separate unrelated elements clearly.
- Let spacing communicate structure before adding dividers, boxes, or decorative treatment.
- Review form spacing, card content, filter groups, navigation sections, dashboards, and admin metaboxes for relationship clarity.

Practical check: use space to create meaning.

### 6. Von Restorff Effect

Core principle: when many elements look similar, the different one gets noticed and remembered.

Apply it by:

- Highlight the intended primary action, recommended plan, key next step, or selected option.
- Use contrast, button treatment, border, elevation, color, placement, or size intentionally.
- Avoid making every card, alert, CTA, or status badge compete equally.
- Use visual distinction sparingly so the important element actually stands out.

Practical check: make one important thing stand out.

### 7. Serial Position Effect

Core principle: people usually remember the first and last items best.

Apply it by:

- Put critical navigation, benefits, warnings, or decision context early.
- Put important final actions, confirmations, summaries, and next steps at the end.
- Avoid hiding essentials in the middle of long lists, dense pages, onboarding sequences, or pricing comparisons.
- Review page hierarchy for what users encounter first, what they must scan through, and what they see at the decision point.

Practical check: first and last positions carry extra weight.

### 8. Tesler's Law

Core principle: every product has complexity; the design decision is who handles it.

Apply it by:

- Use smart defaults, prefilled values, suggestions, saved preferences, and automation where safe.
- Move repetitive or unnecessary effort away from users.
- Do not expose database order, internal process complexity, or avoidable configuration burden as UI complexity.
- Keep the user in control for high-risk, irreversible, legal, financial, security, privacy, or consent decisions.

Practical check: let the product handle complexity where it can do so safely and transparently.

### 9. Doherty Threshold

Core principle: users stay engaged when the system responds quickly and clearly.

Apply it by:

- Acknowledge user actions immediately.
- Use loading, saving, uploading, processing, success, and failure states.
- Prefer skeleton loading when it can show the shape of incoming content.
- Confirm progress and success so users do not wonder whether an action worked.
- Avoid blank waits, dead buttons, silent failures, and spinners that do not explain what is happening.

Practical check: fast feedback feels better.

### 10. Peak-End Rule

Core principle: people judge an experience strongly by its most intense moment and how it ends.

Apply it by:

- Design important peak moments such as first success, milestone achievement, completed setup, successful booking, submitted application, purchase completion, or saved high-effort work.
- Design strong ending moments: confirmation, thank-you, next step, receipt, support path, or useful empty state after success.
- Avoid ending workflows with ambiguity, abrupt dead ends, missing receipts, unclear status, or no recovery path.
- Treat onboarding success, checkout completion, form submission, account setup, and support resolution as experience moments, not just screens.

Practical check: design the peak and design the end.

## 20 UX/UI Dos and Don'ts

### 1. Highlight the Important Action and Make It Stand Out

Do:

- Make the intended primary action visually distinct.
- Use contrast, color, size, border, spacing, and button treatment to create hierarchy.
- Keep comparable cards or plans consistent while making the recommended or primary choice clear.

Don't:

- Give every card, action, or plan nearly identical visual weight when one choice should lead.
- Make every element compete for attention.

Related laws: Von Restorff Effect, Hick's Law.

### 2. Use Skeleton Loading Instead of Classic Loading Where Useful

Do:

- Use skeleton placeholders that resemble the content structure when loading will take noticeable time.
- Show placeholders for real regions such as avatar, headings, text rows, image/media blocks, cards, or list content.
- Keep the skeleton close enough to the final layout that it does not create false expectations.

Don't:

- Use only a centered spinner on an otherwise empty screen when the upcoming layout can be previewed.
- Leave users guessing whether content is loading, stalled, or missing.

Related law: Doherty Threshold.

### 3. Use Smooth Gradients

Do:

- Use gradual, compatible color transitions.
- Let gradients support the interface instead of becoming the interface.
- Check gradients with realistic content, contrast, brand rules, and accessibility needs.

Don't:

- Use abrupt, competing bands of color that create visual noise.
- Treat a specific gradient palette as mandatory if brand, context, or accessibility requires another direction.

### 4. Put Color Psychology in Mind

Do:

- Use color to reinforce meaning and consequence.
- Use red or strong warning treatment for destructive actions where that convention fits the product.
- Use semantic colors consistently for success, warning, error, info, disabled, selected, and focus states.
- Pair color with labels, icons, shape, or text so meaning does not depend on hue alone.

Don't:

- Use a calm or positive color for destructive actions such as delete-account flows.
- Treat color psychology as universal truth independent of culture, brand, domain, and accessibility.

### 5. Show Where and Why the Error Occurred

Do:

- Place errors near the affected field or control.
- Explain what failed and how to fix it.
- Show validation criteria when they help recovery, such as password requirements.
- Preserve entered data after errors.
- Use form-level summaries for long or complex forms.

Don't:

- Show only a generic message such as "Error found."
- Make users search for the failed field or infer the rule from trial and error.
- Use technical, blaming, or vague error copy.

### 6. Avoid Defaulting to Pure Black and Pure White

Do:

- Consider softened dark and light neutrals for comfortable surfaces, such as dark gray instead of pure black and light gray instead of pure white.
- Preserve sufficient contrast for text, controls, focus states, and important UI boundaries.

Don't:

- Default to absolute black and white purely out of habit when the surface feels harsh.
- Treat this as an absolute accessibility rule. Pure black or pure white can be valid when contrast, brand, or product context supports it.

### 7. Use Search Placeholders to Give Hints

Do:

- Use placeholder text to clarify search scope, such as the object types users can search.
- Keep labels, accessible names, and surrounding context sufficient for accessibility.

Don't:

- Use a generic placeholder like "Search" when users need to know what can be searched.
- Use placeholder text as the only persistent label where a label is needed.

### 8. Use Radio Buttons for Single Choice and Checkboxes for Multiple Choices

Do:

- Use radio buttons when exactly one option in a group can be selected.
- Use checkboxes when multiple values can be selected.
- Make the selection rule visible through control shape, labeling, and grouping.

Don't:

- Use a control that hides or contradicts the selection rule.
- Make users learn through errors whether multiple selections are allowed.

### 9. Use Touch-Appropriate UI Elements

Do:

- Use controls designed for fingers on mobile and tablet surfaces.
- Prefer large touch targets, scrolling pickers, toggles, steppers, segmented controls, or native mobile patterns where they fit.
- Match control choice to input method and device context.

Don't:

- Force precise tapping through tiny dropdowns or pointer-oriented controls on touch-heavy workflows.
- Copy desktop interactions directly into mobile without reviewing reach, target size, and gesture discoverability.

Related law: Fitts's Law.

### 10. Group Similar and Related Elements Together

Do:

- Keep similar and related objects together.
- Use grouping to make categories easier to scan and understand.
- Align category, filter, card, icon, list, and form groupings with the user's mental model.

Don't:

- Alternate categories or mix unrelated visual types in a way that makes relationships unclear.

Related law: Proximity Law.

### 11. Decrease the Corner Radius of Nested Inner Elements When It Improves Composition

Do:

- Use a smaller inner radius for nested rounded containers when it creates a coherent parent-child relationship.
- Align radius choices with spacing, surface size, and design tokens.

Don't:

- Automatically use the same large radius for parent and nested child surfaces when the result feels visually awkward.
- Treat this as a universal mathematical rule; the design system and composition still decide.

### 12. Split Long Forms Into Steps and Show Progress

Do:

- Break long forms into meaningful stages.
- Show progress when the process has multiple steps and a defined end.
- Keep completed steps understandable and editable where appropriate.
- Preserve user input during errors, navigation, or interruptions.

Don't:

- Present many unrelated fields in one continuous screen when it increases cognitive load.
- Hide required fields in collapsed sections or optional-looking steps.

Related laws: Miller's Law, Peak-End Rule.

### 13. Avoid the Super Minimal Look

Do:

- Remove unnecessary content while keeping information required to understand status and meaning.
- Show explicit labels, progress, states, percentages, or descriptive titles when they matter.

Don't:

- Remove labels, state text, progress values, or context just to make the screen look cleaner.
- Make users infer status from ambiguous icons, bare numbers, or decorative bars.

### 14. Make Button Text Clear and Actionable

Do:

- Use action-specific button labels such as Submit, Cancel, Save, Delete, Download, Continue, or Create Account.
- Make dialog actions understandable without requiring users to reread the entire prompt.

Don't:

- Use vague labels like Yes, No, OK, or Submit when a specific verb would be clearer.
- Use button text that hides the consequence of a high-risk action.

### 15. Use Full-Width Buttons on Narrow Layouts When It Helps

Do:

- Use full-width buttons for prominent mobile actions when they improve target size, alignment, hierarchy, or ease of interaction.
- Keep primary and secondary actions visually distinct.

Don't:

- Force full-width buttons into compact toolbars, dense desktop UI, or contexts where button width harms scanability.
- Treat full-width buttons as mandatory outside narrow or card-like layouts.

### 16. Align Inputs With the Type of Information Requested

Do:

- Match input structure to expected data shape.
- Use segmented fields for short verification codes where helpful.
- Use appropriate formatting or controls for dates, phone numbers, card numbers, PINs, and other structured data.

Don't:

- Use one generic text field when the data structure itself helps users understand the task.
- Make users guess required length, grouping, or format.

### 17. Use Progress Bars and Milestones When Progress Matters

Do:

- Show progress visually when it helps users understand how far they have come and what remains.
- Use milestones for onboarding, learning, setup, applications, games, loyalty, profile completion, or other progress-driven experiences.
- Pair visual progress with accessible text, such as percent complete or step labels.

Don't:

- Communicate meaningful progress only as buried text when a progress indicator would improve comprehension.
- Add fake or misleading progress.

### 18. Display All Options for Two or Three Choices

Do:

- Show two or three choices directly, often with radio buttons or segmented controls.
- Let users see available options without opening a dropdown.

Don't:

- Hide tiny choice sets inside a dropdown when direct display would reduce interaction cost.

Related law: Hick's Law.

### 19. Give Users a Skip Option in Optional Onboarding

Do:

- Provide Skip when onboarding screens are optional, educational, or repetitive for experienced users.
- Preserve user control and let returning users reach the product quickly.

Don't:

- Force users through optional onboarding content.
- Make legally required consent, safety information, identity verification, or genuinely necessary setup steps skippable.

### 20. Adjust Spacing to Make Related Groups Feel Connected

Do:

- Use spacing as information.
- Use smaller gaps between label and input, larger gaps between field groups, and larger separation before major actions when the layout benefits.
- Review spacing hierarchy in forms, cards, settings screens, admin panels, and checkout flows.

Don't:

- Use the same spacing between all elements when their relationships differ.
- Add boxes or dividers to fix relationship problems that spacing can solve more cleanly.

Related law: Proximity Law.

## How To Apply This Reference

### In The UX/UI Framework Compliance Matrix

Add rows for each of the 10 UX laws and each of the 20 dos/don'ts when the project has user-facing UI, admin UI, form, workflow, onboarding, search, account, commerce, dashboard, portal, or mobile/touch behavior.

For each row, classify as applied now, applied later, contextual mandatory, not applicable, approved exception, or blocked. Include affected pages/templates/CPT/admin screens/workflows, evidence, owner, reviewer, approver, status, and exception/mitigation/expiry where relevant.

### In AI Design Tool Prompt Packages

Include a "UX laws and UI dos/don'ts constraints" section that tells the design tool or coding agent how to apply the relevant rules. At minimum, cover:

- Familiar patterns and expected controls.
- Choice reduction and clear recommendations.
- Touch target size, reach, and mobile control choice.
- Content chunking, grouping, spacing, and hierarchy.
- Primary-action distinction.
- First/last information placement.
- Smart defaults and safe automation.
- Loading, saving, success, and error feedback.
- Peak and ending moments.
- Form control selection, validation, long-form progress, structured inputs, and action-specific button labels.
- Search scope placeholders, optional onboarding skip, progress indicators, nested radius, gradient restraint, semantic color, and avoiding harmful minimalism.

### In Generated Output Audits

Reject or route to rework when generated designs:

- Use unfamiliar navigation or controls without rationale.
- Present too many equivalent options.
- Hide the primary action or make every action compete.
- Use tiny or unreachable touch targets.
- Present dense content without chunks, headings, grouping, or steps.
- Fail to group related labels, fields, cards, filters, or controls.
- Hide essential information in the middle of long sequences.
- Expose avoidable complexity instead of using safe defaults or automation.
- Leave loading, saving, uploading, success, or failure states ambiguous.
- End important workflows without confirmation, receipt, next step, or recovery path.
- Use generic error messages, vague buttons, inaccessible placeholder-only labels, wrong selection controls, unnecessary dropdowns for two or three choices, or forced optional onboarding.
- Use visual polish, gradients, minimalism, color, or radius choices that weaken clarity, accessibility, or design-system consistency.

### In Coded Mockup And Implementation QA

Verify the built UI preserves the approved design intent:

- CTAs, forms, search, progress, errors, loading states, mobile controls, spacing, grouping, and action labels match the approved baseline or documented exception.
- Semantic colors, contrast, focus states, labels, and accessible names work in code, not only in the mockup.
- Responsive layouts maintain touch reach, full-width mobile actions where approved, text wrapping, spacing hierarchy, and state visibility.
- Skeletons, progress bars, segmented inputs, radio/checkbox groups, onboarding skip, and completion confirmations are implemented where the approved artifacts require them.

## Source Notes

The source documents included branded carousel/watermark information. Treat those source notes as attribution/context from the supplied material, not as project design rules unless the current project explicitly adopts that branding.

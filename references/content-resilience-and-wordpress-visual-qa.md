# Content Resilience and WordPress Visual QA

Use this reference before final design acceptance, coded mockup acceptance, frontend implementation acceptance, QA/UAT, launch readiness, and any rescue/audit of a WordPress website produced through the AI Web Delivery Blueprint.

## Content Resilience Testing

Do not design only for ideal demo content. Test representative components, templates, and content modules against:

- Very short headings.
- Very long headings.
- Long names.
- Long menu labels.
- Long URLs.
- Long paragraphs.
- Very short descriptions.
- Very long descriptions.
- Missing images.
- Portrait images.
- Landscape images.
- Square images.
- Long testimonials.
- Short testimonials.
- Multiple categories.
- Many tags.
- Long article content.
- Embedded media.
- Lists.
- Tables.
- Form validation messages.
- Empty search results.
- Large search result sets.
- Translated content where multilingual support exists.
- Unexpected editor-supplied content.

Record evidence, defects, fixes, and approved exceptions. A layout that depends on equal text blocks, perfect image ratios, or placeholder copy is not ready for final approval.

## WordPress Visual Completeness

Human Design Governance extends beyond the homepage. Where relevant to the project, visually and functionally address:

- `front-page.php`
- `home.php`
- `page.php`
- `single.php`
- `archive.php`
- `category.php`
- `tag.php`
- `taxonomy.php`
- `search.php`
- `404.php`
- Custom post type archives.
- Custom post type singles.
- Navigation.
- Footer.
- Pagination.
- Search results.
- Empty search results.
- Comments if enabled.
- Forms.
- Form errors.
- Form success states.
- Validation.
- Password-protected content if used.
- Empty states.
- Error states.
- Loading states where relevant.
- Cookie interfaces where required.
- Privacy and policy page presentation.
- WordPress-generated content.
- Editor-generated content.

Do not permit the homepage to receive substantially higher design quality while secondary templates remain generic.

## WordPress Component Differentiation

Do not automatically use one card component for posts, services, team members, events, case studies, projects, testimonials, and products.

Reuse code where appropriate, but preserve semantic and visual distinctions where content types require them. Code reuse must not erase content meaning.

For each repeated content type, verify:

- What object the component represents.
- Whether items are comparable, independently actionable, sequential, narrative, evidential, or reference material.
- Which fields vary in real WordPress content.
- Which states are required: loading, empty, error, long content, missing media, taxonomy/tag overflow, and permissions where relevant.
- Whether a shared component should expose variants or whether distinct templates/components are required.

## Visual QA Workflow

Where browser or screenshot tools are available:

1. Run the WordPress site.
2. Render the relevant page.
3. Inspect desktop.
4. Inspect tablet.
5. Inspect mobile.
6. Inspect interactive states.
7. Inspect focus states.
8. Inspect long content.
9. Inspect missing media conditions.
10. Inspect WordPress archives.
11. Inspect search.
12. Inspect 404.
13. Inspect forms.
14. Inspect navigation.
15. Inspect footer.
16. Inspect high zoom where feasible.
17. Correct defects.
18. Repeat inspection.

Do not infer visual quality solely from code review. A technically valid HTML, CSS, PHP, or JavaScript implementation is not sufficient evidence that visual quality is acceptable.

## Evidence Record

Use this compact record:

```text
Page/template/component:
Viewport/device checked:
Content resilience cases checked:
WordPress states/templates checked:
Visual defects found:
Fixes made:
Remaining exceptions:
Screenshots/URLs/evidence:
Reviewer:
Approver:
```
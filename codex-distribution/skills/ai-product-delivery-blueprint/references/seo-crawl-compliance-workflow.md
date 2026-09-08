# SEO Crawl and Compliance Workflow

Use this reference when planning, building, auditing, or remediating SEO for a WordPress/CMS website. This is mandatory skill behavior, not an optional prompt.

## Core Rule

Build SEO into the architecture and implementation, then prove it with a full-site crawl before launch. Target 90%+ SEO audit scores in Lighthouse/PageSpeed or equivalent tools, while documenting tool limitations and accepted exceptions. Do not claim ranking guarantees.
## Applicability Matrix Integration

Load `conversion-seo-security-applicability-matrix.md` before finalizing SEO architecture, page briefs, AI design prompts, build tickets, or launch SEO evidence. Verify compulsory defaults and triggered contextual items including internal links, thank-you/success pages, breadcrumbs, FAQs, case studies, real reviews, maps/directions, local schema, robots.txt, unique page titles, meta descriptions, social share images, alt text, privacy page links where required, and analytics events where measurement is in scope.

Do not add fake reviews, fake ratings, fake local schema, or unsupported business claims for SEO benefit.

## When To Load The Full Prompt

Load `generic-ai-seo-compliance-prompt-for-any-website-architecture.txt` when creating a detailed SEO implementation plan from a website architecture, sitemap, CPT model, template list, feature list, or website brief.

## Execution Order

1. Extract the architecture: pages, posts, CPTs, archives, taxonomies, templates, URL patterns, journeys, goals, geography, languages, and constraints.
2. Create an SEO architecture plan before build: search intent, index/noindex, canonical, sitemap, metadata, schema, URL, image SEO, internal link, redirect, local/multilingual, privacy, and performance rules.
3. Add SEO requirements to PRD/page briefs and SRD/SRS, tied to pages/templates/CPTs and verification methods.
4. Implement SEO in WordPress templates, plugins, or custom code according to the approved architecture.
5. Crawl the full staging site before launch using XML sitemap, homepage discovery, navigation/footer links, archive URLs, taxonomy URLs, CPT routes, pagination, filter/search rules, and important legacy URLs.
6. Check rendered output in major browser engines where tools permit: Chromium/Chrome/Edge, Firefox, and WebKit/Safari. Log unavailable engines and closest available evidence.
7. Remediate applicable SEO issues until critical blockers are closed and the SEO audit target is 90%+ or an accountable human accepts the exception.
8. Record before/after evidence, scores, crawl exports, screenshots, validation links, fixed files, remaining risks, approvers, and launch decision.
9. After launch, verify production indexability, sitemap reachability, robots rules, redirects, Search Console/Bing Webmaster Tools setup, schema, analytics, and crawl/indexing issues.

## WordPress Implementation Behavior

For WordPress projects, verify or implement:

- Theme-level unique title, meta description fallback, canonical, robots/robots.txt behavior, Open Graph, and social image output.
- SEO plugin configuration where approved, with locked critical defaults where possible.
- Template-specific metadata for front page, pages, posts, CPT singles, CPT archives, taxonomies, search, 404, legal/support pages, and landing pages.
- XML sitemap inclusion/exclusion rules for pages, posts, CPTs, archives, taxonomies, media, author archives, date archives, and low-value URL patterns.
- Robots/noindex rules for staging, internal/private content, test pages, search results, thin archives, filtered URLs, and duplicate URL patterns.
- Canonical rules for duplicates, pagination, filtered pages, syndicated/duplicate content, and rewritten URLs.
- Schema output only where appropriate and truthful; do not generate fake reviews, ratings, jobs, credentials, locations, or FAQs.
- Breadcrumbs, internal links, above-the-fold CTA support, thank-you/success paths, FAQs, case studies, real-review modules, maps/directions, and local trust elements that match the sitemap, page hierarchy, truthful business data, and conversion paths where applicable.
- Image filename, alt text, dimensions, responsive sizes, lazy loading, hero/LCP handling, compression, team-photo rights/consent where applicable, and social image fallbacks.
- Redirects for legacy URLs, changed slugs, merged content, deleted pages, and launch migration paths.
- Core Web Vitals safeguards for LCP, INP, CLS, font loading, script loading, caching, media, embeds, and third-party scripts.

## Full-Site Crawl Scope

Include homepage, launch-scope pages, posts, CPT singles/archives, taxonomy archives, category/tag archives where indexable, pagination, search/filter URL behavior, contact/legal/support/account/checkout/error pages where relevant, XML sitemap URLs, important legacy URLs, redirect targets, and social preview URLs.

Exclude admin, private, authenticated, sensitive, staging-only, or deliberately noindexed URLs from public-index expectations, but still verify that they are protected correctly.

## Evidence Required

Produce an SEO Crawl and Compliance Audit Package with URL inventory, score evidence, browser/rendering coverage, index/noindex/canonical/sitemap matrix, metadata findings, schema validation, image SEO findings, internal/external link findings, Core Web Vitals findings, accessibility/SEO alignment findings, remediation log, exceptions, approvers, and a final SEO compliant build specification.
# Conversion, SEO, and Security Applicability Matrix

Use this reference when planning, designing, building, auditing, launching, or rescuing a WordPress/CMS website. The purpose is to prevent blanket checklists while still making important conversion, trust, SEO, analytics, privacy, and security controls hard to miss.

## Core Rule

Classify every item as one of: compulsory default, contextual mandatory, not applicable, or approved exception. A contextual item becomes mandatory when its trigger applies. Every mandatory or excepted item must map to a page/template, PRD/SRD requirement, owner, implementation evidence, QA evidence, and approver.

Do not add deceptive or unearned trust elements. Reviews, local schema, case studies, team photos, maps, directions, business hours, response-time promises, credentials, awards, and testimonials must be truthful, approved, and supported by real evidence or omitted.

## Applicability Matrix

| Item | Default classification | Applies when | Evidence required |
|---|---|---|---|
| Custom form or page-specific form | Contextual mandatory | The page has lead capture, booking, support, quote, donation, registration, checkout, feedback, or workflow submission | Form fields, validation, consent, destination, thank-you behavior, abuse controls, QA submission evidence |
| CTA above the fold | Contextual mandatory | Homepage, landing pages, service pages, sales pages, donation pages, booking/contact pages, campaign pages | Desktop/mobile mockup and implemented page show primary action without scrolling |
| Internal links | Compulsory default for indexable pages | Any indexable public page where related content or conversion paths exist | Crawl/internal-link evidence and page brief mapping |
| Thank-you page or success state | Contextual mandatory | Forms, checkout, booking, newsletter signup, registration, downloads, donations, support requests | Success URL/state, tracking event, clear next step, safe messaging |
| Breadcrumbs | Contextual mandatory | Deep hierarchy, blog/resource hubs, ecommerce, directories, CPT singles/archives, knowledge bases, local/service taxonomies | Breadcrumb UI and structured data where appropriate |
| Case studies | Contextual mandatory | B2B, agencies, consultants, professional services, nonprofits, complex purchases, high-trust sales | Approved case-study page/section, proof, rights, client approval where required |
| FAQs | Contextual mandatory | Repeated objections, complex services, pricing questions, compliance questions, support-heavy products, SEO intent | Approved FAQ content, truthful schema only where appropriate |
| Response-time promise | Contextual mandatory | Contact, lead, support, quote, booking, emergency/service pages and the business can honor the promise | Approved promise, routing/SLA evidence, no unsupported claim |
| Sticky mobile CTA | Contextual mandatory | Mobile-heavy lead generation, calls, WhatsApp, booking, ecommerce, urgent services | Mobile mockup/QA screenshot, does not block content, consent, or accessibility |
| Robots.txt | Compulsory default | Public website, staging, or any indexable/noindex distinction | Robots file/rules verified on staging and production |
| Unique page titles | Compulsory default | Every indexable page/template/CPT/taxonomy | Crawl evidence showing unique title output |
| Meta descriptions | Compulsory default | Every important indexable page/template/CPT/taxonomy | Crawl evidence or approved exception for generated snippets |
| Social share image | Compulsory default | Site has public pages shared on social/search previews | Open Graph/Twitter/social image fallback and page-specific image where needed |
| Maps and directions | Contextual mandatory | Physical location, venue, clinic, office, store, local/service-area business | Map/directions module, address consistency, privacy/performance review |
| Real reviews | Contextual mandatory | Trust/conversion depends on reviews and verifiable reviews exist | Review source, permission, no fake ratings/schema |
| Alt text on images | Compulsory default for meaningful images | Every meaningful/content image, icons that convey meaning, linked images | Media audit or rendered-page check; decorative images marked appropriately |
| Local schema | Contextual mandatory | Local business, clinic, office, venue, service-area business, store, branch/location pages | Valid structured data, real NAP/hours/service data, no false claims |
| Privacy Policy page (PP page) | Contextual mandatory | Forms, analytics, cookies/tracking, user accounts, payments, CRM/email integrations, personal data | Approved privacy page linked from footer/forms where required |
| Google Analytics or approved analytics alternative | Contextual mandatory | Measurement, SEO, campaign, conversion, or product analytics is in scope | Tag/config evidence, consent handling, test event evidence |
| Team photo | Contextual mandatory | Trust depends on people/team credibility and photo rights/consent exist | Approved photo, alt text, image rights/consent |
| Hide API keys | Compulsory default | Any API key/token/secret exists | No secrets in frontend, repo, logs, screenshots, docs; secret storage evidence |
| Prevent Git secrets | Compulsory default | Any repository or generated artifact exists | Secret scan result; real secrets removed/rotated if exposed |
| Enable row-level security or equivalent row ownership controls | Contextual mandatory | Multi-tenant apps, portals, dashboards, user-owned records, custom databases, sensitive records | RLS policy or server-side ownership/capability checks and tests |
| Encrypt sensitive data | Contextual mandatory | Sensitive personal data, credentials, tokens, payment data, confidential business data, backups | Encryption/approved-platform storage evidence and key/secrets handling |
| Enforce server-side auth | Compulsory default for protected actions | Admin, account, API, AJAX/REST, CPT save, upload, settings, export/delete, private content | Capability/auth checks and negative tests |
| Log record access | Contextual mandatory | Sensitive, regulated, admin, account, payment, health, financial, CRM, or user-owned records | Access/audit logs without sensitive leakage |
| Block field tampering | Compulsory default for forms/admin/API | Any submitted hidden/read-only/computed/price/role/status/user-owned field | Server-side recomputation/allowlist validation and tampering tests |
| Secure session cookies | Contextual mandatory | Sessions, login, accounts, checkout, admin, authenticated portal | HttpOnly/Secure/SameSite/session-expiry evidence |
| Hash passwords | Contextual mandatory | Passwords are created or stored by the project | Approved platform password hashing; never custom plaintext storage |
| Rate-limit login | Compulsory default where login exists | WordPress admin/login, accounts, portals, password reset, API auth | Rate-limit/bot defense evidence |
| Add bot protection | Contextual mandatory | Forms, login/reset, comments, checkout, signup, API endpoints, scraping risk | Honeypot/CAPTCHA/rate-limit/WAF evidence and accessibility/privacy review |
| Parameterize queries | Compulsory default | Any custom database query exists | Prepared statements, `$wpdb->prepare()`, ORM parameter binding, identifier allowlists |
| Validate all inputs | Compulsory default | Forms, query strings, cookies, headers, REST/AJAX, webhooks, uploads, imports, admin fields | Server-side validation evidence |
| Escape user content | Compulsory default | Any user/CMS/external content is rendered | Context-aware escaping evidence |
| Restrict file uploads | Contextual mandatory | Media uploads, forms, profile images, documents, imports, CPT photo fields | MIME/type/size/count/access controls, safe names, scan where feasible |
| Trim API responses | Contextual mandatory | REST/AJAX/API endpoints return data | Response allowlists, no secrets/PII/privileged fields, auth-aware tests |
| Security headers | Compulsory default | Public/staging web surfaces | Header scan/evidence for CSP where feasible, HSTS where appropriate, X-Content-Type-Options, frame rules, referrer/permissions policy |
| Force HTTPS | Compulsory default | Any public/staging/authenticated web surface | HTTPS redirect/TLS certificate evidence |
| Scan dependencies | Compulsory default | Themes, plugins, packages, libraries, build tooling, CI artifacts | Dependency/plugin/theme scan result and remediation/exception log |

## Execution Behavior

1. During PRD/page briefs, mark each matrix item as required, contextual trigger pending, not applicable, or exception needed.
2. During AI design prompt generation, include required conversion/trust/privacy/SEO items in the page-by-page prompt.
3. During SRD/SRS, convert required security, SEO, analytics, privacy, and data controls into testable requirements.
4. During build, implement only the required/applicable items and do not create fake proof, fake reviews, fake locations, or unsupported promises.
5. During QA/launch, crawl, inspect, scan, and test mandatory items. Launch is blocked by missing compulsory defaults, triggered contextual items, or unresolved critical/high security risks unless an accountable human records an accepted exception with mitigation and expiry.

## Output Format

Use this table in PRDs, page briefs, AI design prompt packages, SRDs, task packets, QA reports, and launch evidence:

| Item | Classification | Applies? | Trigger/evidence | Page/template/CPT | PRD/SRD/control ID | Owner | Implementation evidence | QA evidence | Status | Exception approver/expiry |
|---|---|---:|---|---|---|---|---|---|---|---|
# WordPress Cybersecurity Build Workflow

Use this reference when planning, building, reviewing, auditing, launching, or operating a WordPress/CMS website where AI performs delivery work. This is mandatory security-by-design behavior, not a post-build checklist.

## Control Baseline

Use current project risk, legal obligations, hosting constraints, and approved human security decisions to choose rigor. As a default baseline, map controls to OWASP Top 10, OWASP ASVS, OWASP Web Security Testing Guide, OWASP Cheat Sheet Series, WordPress hardening guidance, and NIST CSF 2.0 functions: govern, identify, protect, detect, respond, and recover.

## Core Rule

No coding-phase task is complete until applicable cybersecurity controls are implemented, reviewed, tested, and evidenced. For WordPress work this includes form protection, web protection, network protection, database protection, encryption, secrets, admin hardening, plugin/theme supply chain control, logging, backup/restore, and incident response readiness.
## Applicability Matrix Integration

Load `conversion-seo-security-applicability-matrix.md` before releasing security-sensitive build tickets. Treat security controls as compulsory default or contextual mandatory according to actual surfaces. In particular, verify hidden API keys, secret scanning/prevented Git secrets, row-level security or equivalent row ownership where multi-tenant/user-owned records exist, sensitive-data encryption, server-side authorization, record-access logging for sensitive records, field-tampering protection, secure session cookies, password hashing, login rate limits, bot protection, parameterized queries, input validation, output escaping, upload restrictions, trimmed API responses, security headers, HTTPS, and dependency scanning.

## Mandatory Lifecycle Behavior

1. Discovery: classify data, users, roles, forms, admin surfaces, integrations, files, payment/PII exposure, hosting/network edge, and current vulnerabilities.
2. PRD: add product-level security requirements, abuse cases, data minimization, account protection, form protection, availability, support, and compliance expectations.
3. Sitemap/page briefs/security architecture: map every page, form, admin action, REST/AJAX endpoint, CPT save handler, upload surface, database table, integration, webhook, cron job, and public URL pattern to likely abuse cases and controls.
4. Mockups: review forms, login/account flows, consent, error messages, recovery flows, admin screens, and destructive actions for secure UX without leaking sensitive information.
5. SRD/SRS: convert security needs into testable controls with verification methods and owners.
6. AI task packets: include threat-model IDs, security control IDs, sensitive data limits, prohibited actions, required checks, and security evidence for every coding/configuration task.
7. Coding: implement controls as part of the feature, not after the feature.
8. Review: require AI self-review, independent technical review, and human security review for sensitive areas.
9. QA: run dependency scanning, secret scanning, static analysis, dynamic testing, targeted manual tests, and WordPress configuration review.
10. Launch: block launch on unresolved critical/high vulnerabilities unless an accountable human signs risk acceptance with mitigation and expiry.
11. Operations: monitor vulnerabilities, WAF/rate-limit logs, auth anomalies, backups, restore readiness, plugin/theme updates, incident signals, and security debt.

## Coding-Phase Non-Negotiables

- SQL injection prevention: never concatenate untrusted input into SQL. Use prepared statements/parameterized queries, `$wpdb->prepare()` for WordPress custom queries, strict allowlists for dynamic identifiers, and least-privilege database users.
- Input validation: validate all external input server-side at trust boundaries, including forms, query strings, cookies, headers, REST/AJAX payloads, webhooks, uploads, and imported data.
- Output escaping: escape for the exact output context: HTML, attribute, URL, JavaScript, CSS, JSON, XML, email, logs, and SQL identifiers where applicable.
- XSS defense: sanitize stored rich text using approved WordPress APIs, minimize unsafe HTML, avoid inline scripts where possible, and use CSP compatible with required third parties.
- CSRF defense: protect state-changing browser requests with WordPress nonces or approved CSRF tokens, verify method/origin where applicable, and never mutate state through GET requests.
- Authorization: check server-side capabilities for every protected action, admin screen, CPT save, media action, REST endpoint, AJAX action, export/delete request, settings change, user-owned record, and multi-tenant row. Use row-level security or equivalent server-side ownership controls where applicable.
- Authentication/session security: require MFA for privileged users, strong recovery rules, throttling/rate limits for login/reset, bot protection where appropriate, secure HttpOnly/Secure/SameSite cookies, session expiration, logout invalidation, password hashing through approved platform mechanisms, and audit logs.
- Forms: add spam/bot controls, rate limits, honeypot or CAPTCHA where appropriate, consent/privacy controls, duplicate handling, idempotency, safe errors, email/CRM abuse prevention, and file-size limits.
- File uploads: allowlist MIME/type/extensions, verify file content where feasible, limit size/count, rename files safely, prevent public execution, scan when feasible, and restrict access to private files.
- Database protection: use least-privilege credentials, safe migrations, backups, restore tests, encrypted backups where feasible, retention/deletion rules, and no direct exposure of database errors to users.
- Encryption and secrets: force HTTPS/TLS, encrypt sensitive data/backups where risk requires, hash passwords with approved platform mechanisms, store API keys/secrets outside code and frontend bundles, prevent Git secrets with scanning, rotate exposed secrets, and never log secrets or plaintext sensitive data.
- Web and network protection: configure security headers, HTTPS redirects, TLS renewal, HSTS where appropriate, WAF/CDN/rate limits, admin access restrictions, XML-RPC/REST exposure rules, firewall rules, staging authentication, and no public debug output.
- Dependency/supply chain: install only maintained approved themes/plugins/libraries, lock versions, scan dependencies, verify source, remove unused code, and patch critical vulnerabilities before launch.
- Logging/monitoring: log security-relevant events and sensitive record access without leaking sensitive data, centralize logs where feasible, and alert on auth abuse, WAF blocks, suspicious uploads, field-tampering attempts, and configuration changes.

## Required Evidence

Produce a cybersecurity evidence package before launch and after major security-sensitive changes. It must include threat model/control matrix, secure coding checklist, dependency and secret scan results, SAST/DAST results where tools exist, targeted manual tests, SQL injection and form-abuse checks, authentication/authorization tests, upload tests, security header/TLS evidence, WordPress hardening evidence, database/encryption/secrets evidence, backup/restore evidence, open vulnerabilities, accepted risks, approvers, and remediation expiry dates.
# WordPress Deployment

Define deployment around the actual hosting constraints.

## Prepare

1. Exact theme and plugin versions.
2. Environment configuration and secrets.
3. Database migration or content migration steps.
4. Media migration.
5. Backup before consequential changes.
6. Cache and CDN invalidation.
7. Domain, DNS, HTTPS, email, cron, and filesystem permissions.
8. Search indexation transition from staging to production.
9. Smoke tests for frontend, admin, forms, CPTs, integrations, and SEO output.
10. Rollback or restore plan.

Never overwrite production content or database state as a side effect of deploying code without an approved migration plan.

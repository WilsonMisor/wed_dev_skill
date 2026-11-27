# Web Caching

Caching requires explicit ownership and invalidation rules.

## Define

1. Browser cache policy.
2. CDN or edge cache policy.
3. Application cache policy.
4. API response caching.
5. Private versus public data handling.
6. Cache keys, including tenant and user scope where required.
7. Invalidation triggers.
8. Staleness tolerance.
9. Failure behaviour when cache infrastructure is unavailable.
10. Observability for hit rate and stale or incorrect data incidents.

Never cache one user's or tenant's private data under a key that can be reused by another user or tenant.

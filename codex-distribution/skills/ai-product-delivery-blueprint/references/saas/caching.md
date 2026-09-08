# SaaS Caching

Caching must preserve tenant, user, role, plan, locale, and other context that changes the answer.

## Required decisions

1. Cache owner and purpose.
2. Key structure.
3. Tenant and user isolation.
4. Expiry.
5. Invalidation.
6. Stale tolerance.
7. Negative caching.
8. Stampede protection where required.
9. Sensitive value restrictions.
10. Behaviour during cache outage.

A cache isolation defect that exposes another tenant's data is a release blocking security failure.

# SaaS Search

Search indexes must respect the same authorization and tenant boundaries as the source data.

## Define

1. Indexed entities and authoritative source.
2. Tenant isolation strategy.
3. Fields allowed in the index.
4. Update and deletion propagation.
5. Reindexing process.
6. Authorization filtering.
7. Ranking and relevance rules.
8. Pagination and limits.
9. Sensitive data restrictions.
10. Observability for stale or missing documents.

A search result must never expose data the user could not fetch through the authoritative application path.

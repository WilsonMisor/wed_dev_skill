# SaaS File Storage

Files are tenant scoped resources unless explicitly global.

## Requirements

1. Ownership and tenant metadata.
2. Allowed types and size limits.
3. Malware or unsafe content controls where required.
4. Private versus public access.
5. Signed URL or proxy access strategy.
6. Storage path isolation.
7. Metadata validation.
8. Retention and deletion.
9. Backup and restore.
10. CDN caching rules.
11. Audit for sensitive downloads.
12. Orphan cleanup.

Do not treat an unguessable object URL as authorization.

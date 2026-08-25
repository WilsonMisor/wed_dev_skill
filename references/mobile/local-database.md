# Mobile Local Database

Use local persistence deliberately for offline data, cache, drafts, indexes, or user state.

## Define

1. Stored entities and source of truth.
2. Schema and migration strategy.
3. Encryption requirement based on data sensitivity.
4. Tenant and account separation on shared devices.
5. Cache versus durable user generated data.
6. Deletion on logout or account removal where required.
7. Synchronization metadata.
8. Conflict metadata.
9. Backup inclusion or exclusion.
10. Corruption recovery.

Test migrations using representative prior versions before release.

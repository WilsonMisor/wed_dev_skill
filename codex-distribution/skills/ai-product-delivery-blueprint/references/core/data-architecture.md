# Data Architecture

Define authoritative sources, ownership, lifecycle, integrity, and movement of data before implementation fragments them across components.

## Required topics

1. Canonical entities and identifiers.
2. Ownership and tenant scope.
3. Source of truth for each field or aggregate.
4. Relational, document, object, cache, search, and analytics storage responsibilities.
5. Transaction boundaries and consistency requirements.
6. Data validation and constraints.
7. Migrations and compatibility.
8. Retention, deletion, export, archival, and legal hold where applicable.
9. Backup, restore, and recovery objectives.
10. Encryption and access controls.
11. Auditability and lineage where needed.
12. Data quality monitoring.

Do not duplicate authoritative mutable state across stores without an explicit synchronization and conflict strategy.

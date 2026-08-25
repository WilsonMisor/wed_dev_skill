# Database Indexing

Indexes are driven by real query patterns and integrity needs.

## Evaluate

1. Primary and unique indexes.
2. Foreign key access patterns.
3. Tenant plus resource filters.
4. Sort and pagination patterns.
5. Partial or filtered indexes where supported and justified.
6. Composite index column order.
7. Write amplification.
8. Storage cost.
9. Redundant indexes.
10. Query plans on representative data.

Do not add an index for every column. Measure and verify the intended query uses it.

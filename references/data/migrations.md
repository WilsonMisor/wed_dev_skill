# Database Migrations

Migrations are production changes and require rollout design.

## Rules

1. Version every schema change.
2. Separate backward compatible expansion from destructive contraction when zero or low downtime deployment requires it.
3. Backfill large datasets safely and observably.
4. Avoid long blocking operations without impact analysis.
5. Define application compatibility during rolling deployment.
6. Test migration on representative data.
7. Verify constraints after backfill.
8. Define rollback or forward fix when reversal is unsafe.
9. Back up consequential data before destructive changes where required.
10. Record migration evidence in release artifacts.

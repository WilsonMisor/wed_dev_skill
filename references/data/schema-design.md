# Schema Design

A schema is an executable part of the domain contract.

## Requirements

1. Canonical naming.
2. Correct types and precision.
3. Nullability aligned with business meaning.
4. Keys and relationships.
5. Tenant ownership.
6. Uniqueness and checks.
7. Money stored without floating point ambiguity.
8. Date and time semantics documented.
9. Status values governed.
10. Indexes derived from access patterns.
11. Migration path from prior versions.
12. Data classification for sensitive fields.

Application validation does not replace database constraints for critical integrity rules that the database can enforce.

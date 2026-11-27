# API Validation

Validate all untrusted input at the boundary and again at deeper domain boundaries when invariants require it.

## Validate

1. Types and required fields.
2. Lengths and numeric ranges.
3. Enumerations.
4. Identifier format and resource existence.
5. Ownership and tenant relationship.
6. Date and timezone semantics.
7. Money amount and currency.
8. File metadata.
9. Cross field business invariants.
10. Unknown field policy.

Return stable client actionable validation errors without exposing internals. Validation does not replace authorization or database constraints.

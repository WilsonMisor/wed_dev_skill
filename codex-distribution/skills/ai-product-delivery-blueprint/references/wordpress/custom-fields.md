# WordPress Custom Fields

Custom fields must have a defined schema and safe persistence behaviour.

## For each field define

1. Stable key.
2. Purpose and type.
3. Required or optional status.
4. Validation and sanitization.
5. Authorization for edits.
6. Default and empty behaviour.
7. Rendering and escaping context.
8. Migration or compatibility requirements.
9. Search, sorting, or indexing needs.
10. Media relationship if applicable.

Protect save handlers with capability checks and nonces where appropriate. Do not trust browser submitted values.

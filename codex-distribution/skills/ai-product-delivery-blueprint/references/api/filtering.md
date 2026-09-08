# API Filtering and Sorting

Expose only supported filter and sort fields.

## Requirements

1. Define operators per field.
2. Validate values and ranges.
3. Preserve tenant and authorization scopes.
4. Prevent raw query language injection.
5. Add indexes for justified high value access patterns.
6. Limit expensive combinations where necessary.
7. Define null and case sensitivity behaviour.
8. Use stable secondary ordering for pagination.
9. Document defaults.
10. Test boundary and abuse cases.

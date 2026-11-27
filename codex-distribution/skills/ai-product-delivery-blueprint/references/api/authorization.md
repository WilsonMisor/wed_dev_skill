# API Authorization

Every protected API operation must state who may perform it, in which tenant or ownership context, against which resource, and under which conditions.

## Test

1. Unauthenticated caller.
2. Authenticated but unauthorized caller.
3. Wrong tenant.
4. Wrong resource owner.
5. Insufficient role or permission.
6. Missing entitlement.
7. Suspended or removed account.
8. Direct identifier substitution.
9. Bulk and filtered endpoints.
10. Privileged administrative path.

A successful client side permission check is not evidence that the API is protected.

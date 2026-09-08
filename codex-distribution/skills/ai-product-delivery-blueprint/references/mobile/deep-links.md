# Deep Links

Deep links are external entry points into application navigation.

## Requirements

1. Define supported schemes and verified domain links.
2. Validate route and parameters.
3. Handle unauthenticated entry.
4. Preserve intended destination after successful authentication when safe.
5. Enforce authorization after navigation.
6. Handle expired invitations, deleted resources, unsupported versions, and malformed links.
7. Prevent arbitrary external URL execution.
8. Test cold start, background, and foreground cases.
9. Coordinate with web routing when universal or app links share URLs.

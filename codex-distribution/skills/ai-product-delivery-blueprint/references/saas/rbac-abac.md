# RBAC and ABAC

Choose role based access control, attribute based access control, or a hybrid according to domain complexity.

## RBAC

Define roles as named bundles of permissions. Avoid role names as the only authorization check when resource ownership or tenant context also matters.

## ABAC

Use attributes such as tenant membership, ownership, region, account state, resource status, or plan only when they are authoritative and consistently available.

## Governance

1. Maintain a permission catalogue.
2. Define role to permission mapping.
3. Define privileged operations separately.
4. Prevent accidental privilege inheritance.
5. Version material permission changes.
6. Test denial paths.
7. Audit high privilege changes.

Do not create arbitrary one off role checks throughout application code.

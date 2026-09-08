# Application Signing

Signing credentials are production secrets and continuity assets.

## Requirements

1. Define Android signing key ownership and protected storage.
2. Define iOS certificates, identifiers, profiles, and account ownership.
3. Restrict CI access to the minimum required credentials.
4. Separate development and production signing material.
5. Document rotation and recovery where platform rules permit.
6. Keep signing secrets out of source control and ordinary logs.
7. Verify release artifacts are signed with the intended identity.
8. Document who can publish to each store.

Loss of signing control can prevent trusted upgrades. Treat credential custody as an operational requirement.

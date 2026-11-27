# Environment Strategy

Define environments before release automation grows around implicit assumptions.

## Address

1. Local development.
2. Shared development if used.
3. Test or integration.
4. Staging or preproduction.
5. Production.
6. Ephemeral preview environments if used.

For each environment define purpose, data classification, credentials, external integrations, feature flags, deployment method, configuration source, observability, backup expectations, access controls, and reset policy.

Do not use production secrets or uncontrolled production data in development and test environments.

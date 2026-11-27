# API Versioning

Define compatibility policy before consumers depend on the interface.

## Policy should state

1. Breaking versus non breaking changes.
2. Version selection mechanism.
3. Supported versions.
4. Deprecation notice.
5. Sunset criteria.
6. Consumer migration support.
7. Mobile client compatibility.
8. Event and webhook compatibility.
9. Contract tests.
10. Telemetry for deprecated usage.

Breaking changes require coordinated rollout and documented migration. Do not silently repurpose an existing field or enum value with incompatible meaning.

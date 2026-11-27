# Mobile Architecture

Define boundaries that remain testable and resilient to lifecycle and connectivity changes.

## Decide

1. Presentation, domain, data, and platform service boundaries.
2. State ownership and lifecycle.
3. Navigation model.
4. API client and contract mapping.
5. Local persistence and cache responsibilities.
6. Offline and synchronization strategy.
7. Authentication state and secure credential storage.
8. Platform services such as camera, location, notifications, biometrics, and files.
9. Error and recovery model.
10. Dependency injection or service location approach only if justified.
11. Testing seams.
12. Build flavours and environment configuration.

Prefer explicit simple boundaries over ceremonial layers with no independent responsibility.

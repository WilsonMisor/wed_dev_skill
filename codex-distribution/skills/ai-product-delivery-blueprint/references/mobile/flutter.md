# Flutter Profile

Apply when Flutter is selected.

## Conventions

1. Pin supported Flutter and Dart versions for the project.
2. Define project structure and feature boundaries before broad implementation.
3. Keep widget composition readable and avoid business logic inside large build methods.
4. Select state management based on application complexity rather than trend.
5. Centralise API, authentication, persistence, navigation, and environment conventions.
6. Use generated serialization or code generation only when it has clear maintenance value.
7. Keep platform specific code isolated and documented.
8. Enforce formatting, static analysis, unit, widget, and integration tests as applicable.
9. Test release builds, not only debug mode.
10. Record Android and iOS minimum supported versions.

Do not introduce multiple competing state, navigation, networking, or dependency injection patterns without an Architecture Decision Record.

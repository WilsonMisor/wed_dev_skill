# Custom Plugin Profile

Use custom plugins for project functionality that should be independent of presentation.

## Controls

1. Define plugin responsibility and boundaries before coding.
2. Namespace or otherwise isolate project code to avoid collisions.
3. Use WordPress capability checks and nonces appropriately.
4. Sanitize and validate input, escape output, and use prepared database access.
5. Protect REST, AJAX, form, webhook, scheduled, and admin actions.
6. Handle activation, deactivation, uninstall, migrations, and versioning deliberately.
7. Avoid storing secrets in source code.
8. Add tests for critical business and security rules.
9. Document hooks, data structures, endpoints, scheduled tasks, and external integrations.

Do not create a custom plugin merely to duplicate a reliable existing capability without a project reason.

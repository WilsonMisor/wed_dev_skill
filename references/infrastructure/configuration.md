# Configuration Management

Configuration varies by environment but should remain validated, documented, and reproducible.

## Rules

1. Separate configuration from code where values vary by environment.
2. Validate required configuration at startup or deployment.
3. Document names, purpose, format, and sensitivity.
4. Provide safe example values without secrets.
5. Avoid hidden defaults for consequential settings.
6. Version configuration schemas or deployment manifests.
7. Define change ownership.
8. Audit production changes where appropriate.

Do not commit live credentials into example files.

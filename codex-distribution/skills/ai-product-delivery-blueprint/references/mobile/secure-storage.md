# Secure Storage

Use platform protected storage for secrets and long lived credentials when the architecture requires local persistence.

## Rules

1. Classify every locally stored value.
2. Keep tokens, keys, or sensitive credentials out of ordinary preferences or plaintext databases.
3. Minimise stored secrets and their lifetime.
4. Define behaviour on logout, account removal, reinstall, device migration, and backup restore.
5. Avoid placing secrets in logs, crash reports, screenshots, clipboard, or analytics.
6. Document platform differences.
7. Consider device compromise in the threat model.

Secure storage reduces exposure but does not make a compromised device a trusted server authority.

# Mobile Permissions

Request device permissions only when the user reaches a feature that needs them, unless platform rules require otherwise.

## For each permission define

1. Business purpose.
2. User benefit.
3. Platform declaration.
4. Just in time explanation.
5. Denied behaviour.
6. Permanently denied behaviour and settings path if appropriate.
7. Limited or approximate permission behaviour where platforms support it.
8. Data retention and privacy consequences.
9. Revocation handling.
10. Tests on supported platform versions.

Do not block unrelated product functionality because an optional permission is denied.

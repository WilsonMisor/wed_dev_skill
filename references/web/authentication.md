# Web Authentication

Authentication proves identity. Keep it separate from authorization.

## Address

1. Login methods and identity providers.
2. Registration and verification if present.
3. Password policy and reset if passwords are used.
4. Multi factor authentication when required by risk.
5. Session creation, renewal, revocation, expiry, and logout.
6. Brute force and credential stuffing controls.
7. Secure cookie or token storage strategy.
8. Cross site request and redirect protections.
9. Account lock, suspension, deletion, and recovery.
10. Audit events for security significant identity actions.

Do not store sensitive bearer credentials in browser storage when a safer architecture is available.

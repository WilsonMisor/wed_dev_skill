# Web Session Management

Define session behaviour as a lifecycle.

## Required decisions

1. Session identifier format and storage.
2. Secure, HttpOnly, SameSite, and transport protections for cookies when cookies are used.
3. Idle and absolute expiry.
4. Rotation after authentication or privilege change.
5. Logout and server side revocation behaviour.
6. Concurrent session policy.
7. Remember me behaviour if offered.
8. Sensitive action reauthentication where warranted.
9. Cross device revocation or session listing if required.
10. Audit and anomaly monitoring.

Test expiry, revocation, privilege changes, and stale client behaviour, not only successful login.

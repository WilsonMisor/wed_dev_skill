# Push Notifications

Push is an unreliable external delivery channel and must not be the sole source of critical state.

## Define

1. Notification event.
2. Recipient and device token mapping.
3. Permission and preference handling.
4. Tenant and account context.
5. Payload minimisation for lock screen privacy.
6. Foreground, background, and terminated application behaviour.
7. Deep link target.
8. Token rotation and invalid token cleanup.
9. Duplicate handling.
10. Provider failure and retry.
11. Analytics where permitted.

The application must fetch authoritative state from the server when notification data could be stale or sensitive.

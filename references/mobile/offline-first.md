# Offline First Behaviour

Use only when product requirements justify meaningful operation without reliable network access.

## Define per feature

1. What can be read offline.
2. What can be created or edited offline.
3. What cannot proceed offline.
4. Local source of truth while disconnected.
5. Pending operation representation.
6. User visibility of unsynced state.
7. Retry policy.
8. Conflict behaviour.
9. Authentication expiry while offline.
10. Storage and retention limits.

Do not label an application offline first merely because it caches the last screen.

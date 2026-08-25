# Device Testing

Emulators and simulators are necessary but insufficient for release confidence.

## Matrix

Define representative Android and iOS versions, screen sizes, memory classes, network conditions, locales, permission states, and hardware capabilities.

## Critical tests

1. Fresh install.
2. Upgrade from supported prior version.
3. Login and logout.
4. App killed and restored.
5. Network loss and recovery.
6. Background and foreground transitions.
7. Permission denial and revocation.
8. Notifications and deep links.
9. Local database migration.
10. Critical business journeys.
11. Accessibility.
12. Release build signing and installation.

Record actual device or simulator coverage rather than claiming universal compatibility.

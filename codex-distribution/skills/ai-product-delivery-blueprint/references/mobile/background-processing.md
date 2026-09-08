# Mobile Background Processing

Mobile operating systems constrain background work. Design around platform rules rather than assuming a continuously running process.

## Define

1. Work that truly requires background execution.
2. Platform mechanism.
3. Time and resource limits.
4. Network and charging constraints.
5. Idempotency.
6. Persistence across process termination where required.
7. User visible notification requirements for long running work.
8. Failure and retry.
9. Privacy and location implications.
10. Tests on real devices.

Move durable critical processing to server infrastructure when it cannot reliably depend on a mobile process.

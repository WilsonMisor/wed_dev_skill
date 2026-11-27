# Mobile State Management

Classify state before selecting tools.

## State categories

1. Ephemeral widget state.
2. Screen or feature state.
3. Shared application state.
4. Server authoritative state.
5. Persisted local state.
6. Authentication and identity state.
7. Connectivity and synchronization state.
8. Navigation state.

For each state define owner, source of truth, lifetime, persistence, invalidation, error handling, and test strategy.

Avoid copying server authoritative data into multiple mutable client stores without a clear reconciliation rule.

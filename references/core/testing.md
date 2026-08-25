# Testing Strategy

Testing must be derived from requirements, architecture, risks, and failure modes.

## Test layers

Select applicable layers from unit, component, integration, contract, database, migration, end to end, browser, device, accessibility, security, performance, resilience, backup restore, and UAT testing.

## Required properties

1. Every critical requirement has a verification method.
2. Critical business rules include negative and boundary tests.
3. Authorization and tenant isolation include denial tests.
4. Retryable operations test duplication and idempotency where applicable.
5. Migrations test forward execution and rollback or mitigation strategy.
6. External dependencies have failure and timeout scenarios.
7. Regression tests are added for fixed defects where feasible.
8. Tests are deterministic enough for CI and have clear ownership for unavoidable flakiness.

A test suite is not complete because it has high line coverage. Coverage must map to meaningful behaviour and risk.

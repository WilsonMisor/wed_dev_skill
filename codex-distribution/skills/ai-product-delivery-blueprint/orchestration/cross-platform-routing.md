# Cross Platform Routing

Use this module whenever two or more clients, services, workers, integrations, or data stores share the same business concept.

## Canonical contract first

Before independent implementation, define one canonical domain contract for each shared entity, command, query, event, and status model.

The contract must define identifiers, ownership, tenant scope, field names and meanings, types, nullability, validation, money and currency semantics, dates and timezones, enumerations, lifecycle states, authorization, errors, versioning, and audit requirements as applicable.

## Propagation

Map the canonical contract to:

1. Database schema and constraints.
2. Domain model.
3. API schemas.
4. Web client types and forms.
5. Mobile models and local persistence.
6. Worker and queue payloads.
7. Webhook and integration payloads.
8. Tests and fixtures.
9. Analytics and audit events where relevant.

## Change control

A breaking contract change requires an Architecture Decision Record, compatibility plan, migration plan, versioning decision, test updates, and coordinated rollout order.

Do not let each client invent its own spelling, status values, monetary units, timezone rules, or identifier semantics.

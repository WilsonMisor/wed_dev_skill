# Observability

Design observability around user impact and operational decisions.

## Signals

1. Structured logs.
2. Metrics.
3. Traces where distributed request flow warrants them.
4. Audit events for consequential actions.
5. Health and readiness checks.
6. Error and crash reporting.
7. Business or workflow health indicators where useful.

## Requirements

Define correlation identifiers, tenant and user context rules that do not leak sensitive data, retention, access, alert thresholds, dashboards, ownership, and runbook links.

Avoid logging credentials, tokens, full payment details, unnecessary personal data, or secrets.

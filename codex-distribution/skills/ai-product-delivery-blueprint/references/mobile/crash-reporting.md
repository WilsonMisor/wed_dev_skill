# Crash Reporting

Crash and non fatal error reporting must support diagnosis without leaking sensitive data.

## Define

1. Provider or self hosted mechanism.
2. Release and build identifiers.
3. Environment separation.
4. User and tenant identifiers only when privacy policy allows and preferably pseudonymous.
5. Breadcrumbs that exclude secrets.
6. Symbol or mapping upload for readable stack traces.
7. Alert thresholds.
8. Ownership and triage workflow.
9. Data retention.
10. Correlation with release rollout.

Test reporting in non production before relying on it for production incidents.

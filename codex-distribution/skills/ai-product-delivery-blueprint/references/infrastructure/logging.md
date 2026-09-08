# Logging

Logs should support debugging, security review, and operations without becoming a sensitive data dump.

## Requirements

1. Structured format where practical.
2. Timestamp and severity.
3. Service and environment.
4. Correlation identifier.
5. Safe user or tenant context where permitted.
6. Error classification.
7. Retention and access control.
8. Central collection for distributed production systems where justified.
9. Redaction of secrets and sensitive fields.
10. Search and incident workflow.

Do not log passwords, bearer tokens, private signing material, or full sensitive payment data.

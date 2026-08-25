# API Error Contracts

Errors must be stable enough for clients to handle without parsing human prose.

## Error shape should support

1. Machine readable code.
2. Human readable safe message.
3. Field errors where relevant.
4. Correlation or request identifier.
5. Retry guidance when appropriate.
6. Rate limit metadata where applicable.

Differentiate validation, authentication, authorization, not found, conflict, rate limit, dependency failure, and unexpected server failure. Avoid revealing secrets, stack traces, SQL, filesystem paths, or private existence information when authorization requires concealment.

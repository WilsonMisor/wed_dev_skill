# API Rate Limiting

Define limits by risk and capacity rather than one arbitrary global number.

## Consider dimensions

1. IP.
2. User.
3. Tenant.
4. API key.
5. OAuth client.
6. Endpoint or operation.
7. Expensive resource.

Return predictable rate limit responses and retry information when safe. Protect authentication, recovery, export, search, upload, and financial operations separately when their abuse profile differs.

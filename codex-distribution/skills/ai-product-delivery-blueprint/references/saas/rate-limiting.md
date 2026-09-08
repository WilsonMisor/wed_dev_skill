# Rate Limiting and Abuse Protection

Rate limits should protect shared capacity and sensitive operations without creating easy denial of service against legitimate tenants.

## Define

1. Limit dimension, such as IP, user, tenant, API key, operation, or resource.
2. Window or token model.
3. Burst allowance.
4. Response and retry information.
5. Privileged or internal exceptions.
6. Distributed consistency needs.
7. Monitoring and abuse investigation.
8. Separate controls for login, password reset, invitation, expensive search, export, and financial actions where needed.

Do not use one global limit where a noisy tenant can exhaust capacity for every other tenant.

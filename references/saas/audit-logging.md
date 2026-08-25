# SaaS Audit Logging

Audit logs provide accountability for consequential actions.

## Capture as applicable

1. Timestamp.
2. Actor identity and actor type.
3. Tenant.
4. Action.
5. Target resource.
6. Result.
7. Material before and after state or change summary where safe.
8. Request or correlation identifier.
9. Source context such as IP or device where policy permits.
10. Privileged access reason where required.

Protect audit logs from ordinary user modification. Do not log secrets or unnecessary sensitive values.

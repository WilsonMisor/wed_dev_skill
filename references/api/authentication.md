# API Authentication

Define how callers prove identity and how credentials are issued, rotated, expired, revoked, and scoped.

## Possible caller types

1. End user session.
2. Mobile or web client on behalf of a user.
3. Server to server service account.
4. API key consumer.
5. OAuth client.
6. Webhook provider.

Use the mechanism appropriate to the caller and threat model. Keep long lived high privilege credentials rare, revocable, and outside source control. Authentication never replaces per operation authorization.

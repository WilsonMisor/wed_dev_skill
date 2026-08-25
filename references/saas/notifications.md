# Notifications

Treat notifications as domain outputs with consent, preference, retry, and duplication concerns.

## Define

1. Event that triggers the notification.
2. Recipient resolution.
3. Tenant branding and context where applicable.
4. Channel, such as email, push, SMS, or in product.
5. Mandatory versus optional status.
6. Preference and consent rules.
7. Template and localization.
8. Idempotency and duplicate suppression.
9. Retry and provider failure handling.
10. Delivery status and audit requirements.

Do not send security, billing, or user communication from an unverified tenant or recipient context.

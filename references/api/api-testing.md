# API Testing

## Test layers

1. Schema and validation tests.
2. Authentication tests.
3. Authorization and tenant isolation denial tests.
4. Domain behaviour tests.
5. Database integration tests.
6. Contract tests.
7. Idempotency and duplicate tests.
8. Pagination and filter tests.
9. Rate limit tests where practical.
10. Timeout and dependency failure tests.
11. Webhook signature and replay tests.
12. Version compatibility tests.

Test APIs directly. A browser end to end test alone cannot prove protected endpoints reject unauthorized direct requests.

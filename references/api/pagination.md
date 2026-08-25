# API Pagination

Large collections must have bounded responses.

## Decide

1. Cursor or offset model.
2. Stable sort order.
3. Default and maximum page size.
4. Behaviour under concurrent inserts or deletes.
5. Filters and sort compatibility.
6. Next page metadata.
7. Tenant and authorization filtering before pagination.
8. Total count policy when counts are expensive.
9. Invalid cursor behaviour.
10. Contract tests.

Never paginate an unfiltered cross tenant dataset and then remove unauthorized items in the client.

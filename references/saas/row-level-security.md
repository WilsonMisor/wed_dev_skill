# Row Level Security

Use row level security when the selected database and architecture benefit from database enforced tenant or user policies.

## Requirements

1. Define the trusted source of tenant and user context.
2. Define policies for select, insert, update, and delete.
3. Separate service or administrative bypass roles and protect them tightly.
4. Prevent client controlled session variables from creating privilege.
5. Test policies directly at the database layer.
6. Test application code with normal and privileged credentials.
7. Review migrations for policy gaps on new tables.
8. Include views, functions, triggers, storage policies, and background jobs in the threat model.

RLS is defence in depth, not permission to omit application authorization and domain validation.

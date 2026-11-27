# Conflict Resolution

Define conflict policy for each synchronised entity rather than using one global rule.

## Options may include

1. Server wins.
2. Client wins where safe.
3. Last write wins with a well defined clock and accepted consequences.
4. Field level merge.
5. Domain specific merge.
6. User mediated resolution.
7. Immutable append only events.

Record why the selected strategy does not lose unacceptable user or business data. Financial, legal, inventory, booking, and other consequential records often require stronger domain rules than timestamp replacement.

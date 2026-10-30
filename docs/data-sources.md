# Data sources

v0.1 uses manual entry and the manual CSV adapter only. No NBA provider, protected-site scraper, injury feed or API key is connected. Synthetic seed data has no NBA provenance and is clearly labelled.

Each fixture has a source reference; predictions and settlements require evidence. CSV imports retain a digest, source, import time and per-row provenance. The raw CSV is not retained automatically. The Data centre reports that automatic refresh is unavailable; data health returns no successful sync timestamp rather than inventing freshness.

`backend/app/providers/manual_csv.py` accepts validated schema objects. Future provider adapters should return the same normalised input schemas and preserve source/effective/retrieval times. Add permitted access, timeout, rate limiting, bounded backoff, raw retention policy, duplicate keys and meaningful integration tests before enabling scheduled refresh. The schema foundations are not a claim that those jobs exist.

CSV preview uses nested transactions and rolls back staged records. Confirmation commits the batch only if every row passes. Import order is teams, players/fixtures, predictions. Dated player assignments determine fixture eligibility, rather than the current team alone. Slate validation uses UK calendar dates only when explicitly supplied. No fixture/player replacement is inferred.

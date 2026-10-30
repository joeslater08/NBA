# Integration contract v1

Only the NBA repository is attached. Overview HQ and NFL Testing Centre have not been inspected or modified. No shared library has been created. Generic odds/grading code can be considered for reuse after both working systems are inspected.

All endpoints are JSON REST GET routes. `synthetic=false` is the default; demonstration data requires explicit `synthetic=true`. Identifiers are stable strings; timestamps are ISO 8601 UTC. Unknown values are null, never fabricated zeros. Summary includes `schema_version: "1.0"`, generation time and dataset flag. Currency represents nominal paper units, not transactions.

| Endpoint | Meaning |
| --- | --- |
| `/api/v1/nba/summary` | Fixture/prediction counts, pending grades, paper metrics and explicit model/data status |
| `/api/v1/nba/paper-performance` | Entries, stakes, known/full P/L, ROI ratio, missing-return count and drawdown |
| `/api/v1/nba/model-performance` | `status: unavailable`, `metrics: null` until a validated model exists |
| `/api/v1/nba/analysts` | Unique prediction outcomes, decisive hit rate, sample counts and average recorded odds |
| `/api/v1/nba/recent-results` | Latest 100 graded records with evidence and UTC grading time |
| `/api/v1/nba/data-health` | Manual source, unverified fixture count, no automatic refresh, null sync time |

P/L is measured in virtual units. ROI and hit_rate are ratios, not percentages. Consumers should multiply by 100 for percentage display and preserve nulls. Do not combine NBA and NFL forecast accuracy into one percentage. Source-specific bookmaker conventions are stored in structured records, not inferred from display names.

Saving an endpoint response as JSON is the fallback export; the consumer can call these endpoints without HTML scraping. `/api/v1/export/{resource}` supplies CSV audit extracts. FastAPI's `/openapi.json` and `/docs` describe write schemas. There is no authentication in this local release; a future hosted contract must add maintained authentication, least-privilege access and backups before network exposure.

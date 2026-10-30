# Database and history

Run all commands from the repository root. Default storage: `nba.db`, ignored by Git. Foreign keys are enabled on each SQLite connection. UUIDs identify entities independently of names.

| Tables | Role |
| --- | --- |
| teams, team_seasons | Stable team identity; season-specific conference/division foundation |
| players, player_assignments | Current team and dated historical assignment intervals |
| games | UTC start, season, distinct opponents, lifecycle status, scores, source and verification |
| analysts | Extensible source registry with creation timestamp and notes |
| predictions | Locked market, original price, evidence, creation/lock/start snapshot and optional model metadata |
| settlements | One evidence-backed final outcome per prediction; missing results remain pending and are not saved as settled |
| parlays, parlay_legs | Original displayed price, explicit void convention and linked unique selections |
| paper_entries | Immutable virtual stake and original recorded price; exactly one single/parlay target |
| audit_events | Lock, retrospective-entry, fixture-result and grading evidence |
| import_batches, data_provenance | Deduplicated batch and source/retrieval metadata |
| player_game_logs, team_game_logs | Nullable historical box-score/statistics foundations, not yet populated by a provider |
| model_runs | Version, commit, inputs, seed, parameters and execution metadata; no model runs are fabricated |

Core endpoints use these tables, but v0.1 does not expose a full editor for historical logs, trades or model runs. A new player's dated assignment can be supplied at creation. Trade management and amendment APIs are future work.

Unknown statistics remain null, not zero. Availability/DNP reason is separate from minutes. Model-run simulation_count is nullable, and the database rejects a positive count unless execution_status is completed; future runners must also verify actual computation. No database constraint alone can prove a simulation occurred.

## Migrations

`.venv/bin/python -m alembic upgrade head` applies additive revisions. `.venv/bin/python -m alembic check` checks schema drift. Do not use `create_all` for application startup or delete the database to resolve migrations. Tests use temporary databases. Never run a destructive downgrade on real research data without approval and a verified backup. New batch-table migrations must preserve/recreate immutable-table triggers.

Predictions, settlements, paper entries, parlay definitions/legs and audit events reject updates/deletes in SQLite through triggers and in the ORM through event guards. Source metadata and fixture lifecycle updates have controlled APIs; final fixture results cannot be overwritten. Correction/regrade functionality is not yet available.

## Backup and restore

Create a consistent SQLite backup with an unused destination filename:

```bash
.venv/bin/python -m scripts.backup backups/nba-2026-10-30.db
```

Create the `backups` directory first. The utility uses SQLite's backup API, verifies integrity and refuses to overwrite any existing file. Prefer a private destination outside the checkout. Do not publish personal notes or databases.

To restore: stop the server; make a verified backup of the current database; keep that current file under a new preservation name; copy the selected backup to `nba.db`; run integrity and foreign-key checks with SQLite; run `alembic current` and `alembic upgrade head` only if required; restart and verify known records. Do not remove the preserved original until the restored data has been checked. SQLite WAL/SHM files require care: stop all connections before replacing files. JSON/CSV exports are research extracts, not complete database backups.

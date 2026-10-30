# NBA Intelligence Lab

Version 0.1 is a local NBA research and **virtual paper-testing** foundation. There is no real-money wagering, account access, payment, deposit or automated placement functionality. No paid API key is required.

## Implemented

- Responsive dark React/TypeScript dashboard with desktop and mobile controls.
- FastAPI REST API, Pydantic validation, SQLite storage, SQLAlchemy and additive Alembic migrations.
- Team, player, dated team-assignment and fixture records; manual fixture status and final scores.
- Analyst registry, including the six requested names with **no fabricated history**.
- Manual, immediately locked predictions with structured markets, recorded prices, rule references and preserved timestamps. Results live in separate append-only settlements.
- Points, rebounds, assists, PR, PA, RA, PRA, selected-team moneylines/spreads, team totals and game totals. Over/under, integer alternatives, pushes, missing results, DNP and postponement rules.
- Doubles, trebles and larger parlays with unique linked legs; configurable void rules, price completeness warnings and unavailable joint probabilities.
- Virtual paper units, P/L, settled-stake ROI, drawdown and losing streaks; analyst singles records derived from settlements.
- CSV preview/import for teams, players, fixtures and predictions; CSV audit exports; import provenance, duplicate detection and atomic batches.
- Explicit synthetic/real dataset separation and a deterministic numerical demonstration; initial fixture dates are relative to first seeding.
- Versioned Overview HQ integration endpoints and JSON responses, without assuming its architecture.
- Backup utility, tests and learning documentation.

## Install: macOS / Linux

Use Python 3.12+ and Node 24 LTS (Node 20.19+ also satisfies Vite). Python and Node must already be installed. Run from the repository root:

```bash
bash scripts/install.sh
bash scripts/start.sh
```

Open the local application on port 8000 in your browser. The server serves the compiled UI and API together. Interactive API documentation is available at `/docs` on that server. It binds to loopback by default.

## Install: Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r backend/requirements.lock
cd frontend
npm ci
npm run build
cd ..
.venv\Scripts\python.exe -m alembic upgrade head
.venv\Scripts\python.exe -m scripts.seed
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

These Windows commands are documented but have not been executed on a Windows machine. `uvloop` is excluded on Windows; `tzdata` supplies UK timezone data there.

The default database is `nba.db` relative to the repository root. Set `DATABASE_URL` in the process for a different database. `.env.example` is a reference: `.env` is not automatically loaded unless Uvicorn is started with `--env-file .env` (migrations must receive the same variable). Do not commit databases or secrets.

## Development and checks

Run the backend in one terminal:

```bash
.venv/bin/python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

For frontend hot reload, use a second terminal: `cd frontend` then `npm run dev`. Vite proxies API requests to port 8000; never embed credentials in the UI.

```bash
.venv/bin/python -m pytest -q -c backend/pyproject.toml
.venv/bin/ruff check backend scripts migrations
.venv/bin/ruff format --check backend scripts migrations
.venv/bin/python -m alembic check
cd frontend
npm test
npm run build
npm run format:check
```

On Windows replace `.venv/bin/python` with `.venv\Scripts\python.exe` and `.venv/bin/ruff` with `.venv\Scripts\ruff.exe`. All Python commands run from the repository root. In a sandbox, API tests may require permission for local event-loop sockets; a hang does not establish a test pass.

Browser checks use an **isolated test database**, not your research database. In a separate backend terminal, set `DATABASE_URL` to a fresh temporary SQLite path, run migrations and seed it, then start Uvicorn on port 8000. Run `npx playwright install chromium` once in `frontend`, then `npm run test:e2e`. If Chromium is already installed, set `CHROMIUM_PATH` to its executable instead. The tests add fictional records to their selected database. Desktop and mobile projects are included. See [validation](docs/model-validation.md).

## Try the workflow

1. Start in **Synthetic demonstration** mode. The seeded example has one win (+0.90 units), one loss (−1 unit) and one push (0 units): −0.10 units on three units. These are fictional outcomes, not a backtest.
2. Open Games & players to create a fixture and a player with a verified team assignment. Inputs using date/time controls follow your browser timezone; the dashboard explicitly displays UK time. Storage/API timestamps are UTC.
3. Add an analyst, then record a prediction. Select the market, threshold, source evidence and verified settlement conventions. Saving locks the record immediately.
4. Before fixture start, record paper units against the selection or combine selections into a parlay. Always record the original displayed combined price; a calculated odds product is not a replacement for a missing price.
5. After the fixture, record its status/scores, then grade individual selections in Results review using a verified result. For player combinations supply the verified sum; for spread/moneyline supply selected-team score minus opponent score. Match regulation/overtime scope to the locked rules.
6. Check the paper ledger and analyst records. Switch to **Real manual records** for genuine research. No synthetic prediction or return enters those aggregates.

Historical predictions can be entered only with an explicit original timestamp before fixture start. The audit log records the actual lock time and whether entry occurred after game start. These retrospective entries cannot receive new paper units. They are not validated as contemporaneously captured forecasts.

No update/delete routes exist for locked predictions or settlements. SQLite triggers and ORM guards reinforce immutability. An incorrect record currently needs a separately documented audit investigation; an amendment/regrade workflow is **not implemented**, so do not edit the database to conceal an error.

## CSV imports

Use Data centre. Select the dataset and record type, paste CSV, supply a source reference and preview before confirming. All rows must pass before any are saved. Maximum 5,000 rows / 1 MB per request. IDs come from the stored records/API/exports; names are never guessed into identities.

| Type | Required columns | Useful optional columns |
| --- | --- | --- |
| Teams | `name,abbreviation` | `conference,division` |
| Players | `name,team_id` | `position,assignment_start` (timezone-aware ISO timestamp) |
| Fixtures (`games`) | `season,start_utc,home_team_id,away_team_id` | `source` (defaults to import reference) |
| Predictions | `analyst_id,game_id,market` | `player_id,team_id,odds,bookmaker,created_at,evidence,notes,model_version` |

Prediction `market` is a quoted JSON object containing `kind`, `direction`, `threshold`, `includes_overtime`, `dnp`, `postponed` and `rule_reference`. See `/docs` for the schema. Use normal CSV double-quote escaping inside JSON. Empty optional prices remain null. Exported CSVs are audit extracts with generated columns; they are not automatic round-trip import files. Formula-like exported text is escaped to reduce spreadsheet injection risk. JSON integration endpoints retain exact API field semantics.

## Limitations and later stages

This release is local and unauthenticated. Do not expose it publicly. Live providers, automatic refresh/grading, injuries, forecasting, Monte Carlo simulation, backtesting, advanced analyst/RotoBot diagnostics and multi-sport connectivity are planned. Historical-statistics, provenance and model-run tables exist as foundations; box-score ingestion and model execution do not yet exist. No completed model run is seeded. Special settlement promotions and revised correlated parlay prices must not be approximated: use a rule this version explicitly supports or leave the record ungraded/unpriced.

[Architecture](docs/architecture.md) · [Database and backup](docs/database.md) · [Integration](docs/integration.md) · [Learning guide](docs/learning-guide.md) · [Roadmap](ROADMAP.md) · [Acceptance evidence](docs/acceptance.md)

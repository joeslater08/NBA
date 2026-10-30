# Architecture

The initial repository contained only a five-byte README and one commit. No framework, database, dependencies or test conventions existed. Only the NBA checkout is attached; Overview HQ and NFL Testing Centre have not been inspected or modified.

## v0.1 implementation plan

1. Establish Python/FastAPI/SQLAlchemy/Alembic and React/TypeScript foundations.
2. Store stable identities, fixtures, dated assignments and locked predictions.
3. Separate structured market calculation, settlement history, paper accounts and ingestion from API/UI code.
4. Build usable entry/review screens and explicitly fictional demonstration data.
5. Verify core mathematics, API behaviour, migrations, import atomicity and desktop/mobile workflows.
6. Document repeatable local/cloud setup, backup and extension contracts.

No paid service, destructive migration or new shared infrastructure was required. The user explicitly authorised application implementation in addition to environment onboarding.

## Layers

`frontend/src/components/` owns forms and presentation. `App.tsx` composes the workspace; `api.ts` owns HTTP and UK-time formatting. The UI requests the same-origin API (Vite proxies it during hot reload).

`backend/app/main.py` owns REST routes and transaction commits. `schemas.py` validates inputs. `services.py` validates identities, fixture relationships and lifecycle rules and derives aggregates. `markets.py` contains side-effect-free grading and price mathematics. `providers/manual_csv.py` is the manual ingestion adapter. `models.py` and `database.py` own storage. Alembic revisions explicitly evolve it.

The production frontend is served by FastAPI, so local startup needs one server and one SQLite file. No external service or credential is necessary. A built frontend must exist **before** starting the backend for it to mount the UI.

## Research integrity

Predictions snapshot their original fixture start. Later fixture status edits do not mutate that snapshot. Creation time can be historical only when explicitly provided; actual lock time and retrospective entry are audited. Paper entry is forbidden after fixture start. Grades are separate evidence-backed records. Final records cannot be overwritten through supported routes, ORM or SQLite SQL updates/deletes. Financial totals derive from append-only inputs and their settlements, avoiding mutable balances.

`synthetic` belongs to teams, players, fixtures, predictions, parlays and paper entries. Writes validate compatible modes and aggregates filter by mode. Analysts are a shared registry; each analyst's selection statistics are filtered by dataset.

## Deliberate trade-offs

- SQLite suits one local researcher; PostgreSQL requires driver/deployment work, migration verification and equivalent immutable-table triggers before use.
- Plain responsive CSS supplies the small v0.1 design system instead of adding Tailwind/component-library infrastructure. No charting library is installed because no forecast distributions exist yet.
- NumPy, pandas, SciPy and scikit-learn are deferred until their v0.3/v0.4 workflows use them.
- Manual result entry is explicit and source-labelled; it is not a verified provider response. The software cannot prove that a source URL is accurate or that historical odds were genuinely available at the supplied time.
- No public hosting/authentication, live-data jobs, screenshots/OCR, forecasting, simulation or completed backtests in this release.

See decisions/0001-local-research-foundation.md for the decision record.

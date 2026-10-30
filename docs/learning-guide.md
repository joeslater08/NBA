# Learning Centre

## 1. Functions and grading

**What/why:** `grade` turns a structured selection and verified result into an outcome. One rule implementation prevents dashboard and paper calculations disagreeing. **Files:** `backend/app/markets.py`, `backend/tests/test_markets.py`. Parameters are typed variables; the returned string is consumed by settlement services. A list holds parlay outcomes; a dictionary holds market fields. Pydantic checks the dictionary before calculation. `Decimal` protects paper arithmetic from familiar binary floating-point rounding artefacts.

**Test:** run the market test file. **Exercise:** add an over 8.5 rebounds example with actual 9 and predict the result before running it.

## 2. Classes, databases and relationships

**What/why:** SQLAlchemy classes describe SQL tables. `Prediction.game_id` is a foreign key linking to `Game.id`, rather than relying on a matching team name. UUIDs survive name changes. **Files:** `models.py`, `database.py`, `migrations/`. `Mapped[str]` is a type hint, not a replacement for database constraints. Migrations describe reviewed changes over time; they are distinct from changing Python code.

**Test:** `test_migrations.py` builds a temporary database and verifies repeatable seed/backup behaviour. **Exercise:** draw the relationship from analyst to prediction to settlement; explain why a settlement does not overwrite its prediction.

## 3. APIs, JSON and validation

**What/why:** the browser sends JSON over HTTP; FastAPI validates it before writing. **Files:** `main.py`, `schemas.py`, `services.py`, `frontend/src/api.ts`. A request schema is an explicit contract, and a 422 error means the data failed validation. A 409 means the request conflicts with an existing record. Source evidence records what the researcher supplied; software cannot independently prove it is true.

**Test:** `test_api.py`. **Exercise:** use local `/docs` to submit the same fixture prediction twice and observe the duplicate rejection.

## 4. React components and TypeScript

**What/why:** components compose the dashboard and reusable accessible forms. **Files:** `frontend/src/App.tsx`, `components/Forms.tsx`, `PredictionForm.tsx`, `Settlement.tsx`, `api.ts`. React state tracks the selected workspace and dataset. Props pass data to a component. TypeScript helps catch mismatched props before the browser runs the code; server validation remains essential.

**Test:** `npm test`, `npm run build` and the isolated browser workflow. **Exercise:** add a short explanation to a form, keeping its label associated with the input. Check it on mobile.

## 5. CSV and atomic transactions

**What/why:** a batch with one invalid row must not quietly save the others. **Files:** `providers/manual_csv.py`, `components/DataCentre.tsx`. A database savepoint stages validated rows. Preview rolls them back; confirmed batches commit only if every row passes. Stored identifiers disambiguate equal names.

**Test:** API import atomicity tests. **Exercise:** preview two teams with the same abbreviation and inspect the row error. Confirm that neither is saved.

## 6. Virtual paper mathematics

**What/why:** stakes and odds measure a research experiment consistently. **Files:** `markets.py` (`profit`), `services.py` (`paper_details`, `portfolio_metrics`). Return is a function of the locked stake, price and observed settlement. A missing price is not an invitation to use an average. Sample counts matter: one win at large odds is not evidence of reliable forecasting.

**Test:** return/ROI/parlay tests. **Exercise:** calculate P/L for two units at 1.80 for a win, loss and push, then compare with the function.

## 7. Git and documentation

Git records code history; database history is a separate concern. `git status` shows changes, `git diff` explains edits, and migrations describe schema evolution. No changes are automatically committed or pushed by this setup. **Exercise:** read an Alembic revision and describe which columns it adds without running a downgrade.

## 8. Statistics for later releases

A mean is the sum divided by sample size; a median is the middle ordered value. Variance measures average squared distance from the mean (sample variance uses n−1); standard deviation restores the original units. Neither describes injury or role changes by itself.

A distribution describes plausible outcomes, not just a mean. Count statistics need appropriate discrete distributions or empirical samples. Monte Carlo repeatedly samples an assumed distribution and estimates frequencies; a fixed random seed makes computation reproducible, not accurate by itself. Correlation measures association and can invalidate naive multiplication of marginal probabilities. More runs reduce sampling noise but do not repair weak assumptions.

Backtesting reconstructs forecasts using only information available at each historical time. Validation compares errors and calibration on chronologically held-out data. These features are planned, not implemented. **Exercise:** explain why a manually entered historical prediction timestamp alone cannot prove a backtest was free of future information.

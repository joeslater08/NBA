# Validation

v0.1 tests the local research system, not a predictive model. There are no forecast accuracy, Brier score, calibration, simulation or backtest results to report.

- `backend/tests/test_markets.py`: structured market validation, over/under/integer lines, spread signs, missing results, DNP, postponement, push/void accumulators, P/L, ROI, drawdown, break-even and expected profit.
- `backend/tests/test_api.py`: records and references, duplicate/immutable predictions, source timestamps, scope matching, dataset separation, parlay conventions, paper prices, import preview/atomicity and integration responses.
- `backend/tests/test_migrations.py`: fresh migrations, seed repeatability, preserved timestamps, SQL immutability and backup integrity.
- `frontend/src/api.test.ts`: unknown-value rendering and UK daylight-saving display.
- `frontend/e2e/workflow.spec.ts`: real Chromium desktop/mobile rendering, navigation, analyst entry, CSV preview, prediction locking and paper-unit forms.

Browser tests mutate their database. Always run them against an isolated synthetic database. In the cloud, use system Chromium through `CHROMIUM_PATH=/usr/bin/chromium`; desktop users can install Playwright's Chromium. This is functional coverage, not a full manual accessibility audit.

Before forecasting in v0.3, compare season/recent/minutes-adjusted baselines chronologically using only pre-game information. Store data availability timestamps, split train/validation/test by time, measure MAE/RMSE/bias and use walk-forward evaluation. v0.4 must store seeds and completed computation counts; v0.5 adds probability calibration, Brier/log loss, uncertainty intervals and version comparison. No advanced model should replace a baseline without measured improvement. Retrospective manual inputs are not a leakage-safe backtest dataset.

# Version 0.1 acceptance evidence

Validated on 30 October 2026 in the attached Linux cloud instance with Python 3.12.14, Node 24.19.0 and system Chromium. This report covers the local foundation, not later forecasting or hosted deployment.

## Executed checks

| Check | Outcome |
| --- | --- |
| pytest (core maths, API, imports, migration, seeding and backup) | 79 passed; one non-failing upstream TestClient/httpx deprecation warning |
| Vitest (unknown values, GMT and BST) | 4 passed |
| Playwright | 4 passed: desktop/mobile navigation, analyst management, CSV preview, prediction entry and paper-unit recording |
| TypeScript and Vite production build | Passed |
| Ruff lint and formatting | Passed |
| Prettier source formatting | Passed |
| Alembic upgrade and schema-drift check | Passed; no pending upgrade operations |
| pip dependency check | No broken requirements |
| npm production dependency audit | Zero reported vulnerabilities at check time |
| Repeatable install script | Executed successfully with existing database preserved |
| Seed repeatability | Existing prediction IDs/timestamps preserved |
| SQLite backup | Integrity verified; overwrite refusal tested |
| Clean project runtime | Server started via scripts/start.sh; health and compiled dashboard returned HTTP 200 |
| Dataset separation | Clean real dataset has zero games/predictions; synthetic dataset has 2 games / 5 predictions; switching UI to real hides fictional fixtures |

The synthetic paper ledger has 3 settled entries, −0.10 units and −3.333…% settled-stake ROI. This is a deterministic fictional calculation, not historical NBA performance. The six named outside analysts have no invented prediction history. Browser mutation tests used a separate temporary database.

## Acceptance mapping

| Requirement | Evidence |
| --- | --- |
| Local start and dashboard | Working server, compiled-page request, Chromium desktop/mobile rendering |
| Team/player/game storage | API tests and working record forms |
| Analyst creation | API and browser form tests |
| Linked prediction entry | API and browser tests with fixture/player validation |
| Correct markets | Parameterised over/under, integer, spread, moneyline, combination and total tests |
| Paper units and P/L | API and browser tests; Decimal return calculations |
| Analyst records update | Settlement-derived unique singles tests |
| Doubles/parlays | Linked-leg, accumulator, explicit void-entire/reduction and price tests |
| Missing odds | Winning return and full ROI remain null; calculated combined price is separate |
| Invalid fixtures | Unknown IDs, equal opponents, duplicate fixtures, wrong teams and selected-slate tests |
| Preserved timestamps/history | UTC offset conversion, retrospective audit, original/lock display, ORM and database immutability tests |
| Explicit sample labels | Synthetic selector/banner and isolated API aggregates |
| Automated tests | Counts above; no zero-test or skipped predictive suites counted as validation |
| Setup instructions | README macOS/Linux/Windows commands and tested cloud install/start steps |
| No real-money functionality | No payment/placement/account-login endpoints or dependencies implemented |
| Future expansion | Historical-statistics/model-run/provenance tables and documented REST integration contract |

## Remaining boundaries

Windows/macOS commands are documented but only Linux was executed. No full manual accessibility audit, authentication, public hosting, approved live provider, scheduled jobs, automatic box-score grading, statistical forecasts, simulation or backtesting has been validated because those later workflows do not yet exist. Player trade management and explicit correction/regrade workflows need future implementation. Only documented market and parlay conventions are supported; do not approximate unsupported bookmaker promotions or correlated revised prices.

The prepared environment's install_script and start_skill were saved as a configuration draft. Publication and restoration into a new task have not been executed or validated. Review and save the draft in environment settings, then publish the environment when desired. Processes must restart in future tasks.

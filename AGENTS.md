# NBA Intelligence Lab contributor instructions

Read README.md, docs/architecture.md and ROADMAP.md before a substantial change. The immediate release is v0.1; do not treat the full product vision as already implemented.

- Use this existing isolated checkout. Do not create Git worktrees unless the user explicitly asks.
- Never add real-money placement, payment, deposit or bookmaker login functionality.
- Never fabricate NBA statistics, source records, probabilities or completed simulations. Keep synthetic data explicitly labelled and filtered from real aggregates.
- Preserve locked predictions, original prices, timestamps and settlements. Use additive, reviewed migrations; ask before a destructive database change. No database edits that rewrite history.
- Ask before paid services. No secrets in frontend code, source control, logs or test fixtures.
- Use UK English and Europe/London display; UTC API/storage with timezone-aware input.
- Keep business calculations in backend/app/markets.py or services.py, schema validation in schemas.py, provider ingestion in providers/, and UI components separate.
- Python 3.12+, typed boundaries, Ruff; React/TypeScript with accessible labelled controls. Explicit nulls for unknown values.
- All repository commands run at the root unless documented otherwise. Install with `bash scripts/install.sh`; run with `bash scripts/start.sh`. Windows commands are in README.md.
- For meaningful changes run Python tests, Ruff, frontend tests and build. For UI workflows use Playwright with a separate seeded database. Never run browser mutation tests on genuine research data.
- Test grading, prices, missing data, immutable history and reproducibility rather than mirroring implementation. New statistical models require chronological evaluation before promotion.
- Update CHANGELOG.md and relevant docs. Report passed, failed and unrun checks separately.
- Do not assume Overview HQ or NFL Testing Centre architectures until those repositories are inspected. Keep sport-specific model assumptions separate.

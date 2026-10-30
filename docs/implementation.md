# Implementation change map

The initial repository contained only README.md. It is updated; the files below were added for the v0.1 foundation. No changes were committed or pushed automatically.

Root configuration: AGENTS.md, CHANGELOG.md, ROADMAP.md, .gitignore, .env.example, .python-version, .nvmrc and alembic.ini.

- `backend/__init__.py`
- `backend/app/__init__.py`
- `backend/app/database.py`
- `backend/app/main.py`
- `backend/app/markets.py`
- `backend/app/models.py`
- `backend/app/providers/__init__.py`
- `backend/app/providers/manual_csv.py`
- `backend/app/schemas.py`
- `backend/app/services.py`
- `backend/pyproject.toml`
- `backend/requirements.lock`
- `backend/tests/conftest.py`
- `backend/tests/test_api.py`
- `backend/tests/test_markets.py`
- `backend/tests/test_migrations.py`
- `docs/acceptance.md`
- `docs/architecture.md`
- `docs/data-sources.md`
- `docs/database.md`
- `docs/decisions/0001-local-research-foundation.md`
- `docs/glossary.md`
- `docs/integration.md`
- `docs/learning-guide.md`
- `docs/model-methodology.md`
- `docs/model-validation.md`
- `docs/product-brief.md`
- `frontend/e2e/workflow.spec.ts`
- `frontend/index.html`
- `frontend/package-lock.json`
- `frontend/package.json`
- `frontend/playwright.config.ts`
- `frontend/src/App.tsx`
- `frontend/src/api.test.ts`
- `frontend/src/api.ts`
- `frontend/src/components/DataCentre.tsx`
- `frontend/src/components/Forms.tsx`
- `frontend/src/components/PredictionForm.tsx`
- `frontend/src/components/Research.tsx`
- `frontend/src/components/ResearchTables.tsx`
- `frontend/src/components/Settlement.tsx`
- `frontend/src/main.tsx`
- `frontend/src/pages/Analysts.tsx`
- `frontend/src/pages/Dashboard.tsx`
- `frontend/src/pages/Learning.tsx`
- `frontend/src/pages/Portfolio.tsx`
- `frontend/src/styles.css`
- `frontend/tsconfig.json`
- `frontend/vite.config.ts`
- `migrations/env.py`
- `migrations/script.py.mako`
- `migrations/versions/1356c8ef43ae_historical_data_and_model_audit_schema.py`
- `migrations/versions/6a28b2073bf4_initial_research_foundation.py`
- `migrations/versions/d9c44e1b2600_append_only_research_records.py`
- `migrations/versions/f69a890d1c75_explicit_parlay_settlement_rules.py`
- `sample_data/README.md`
- `sample_data/teams.csv`
- `scripts/__init__.py`
- `scripts/backup.py`
- `scripts/install.sh`
- `scripts/seed.py`
- `scripts/start.sh`

Dependencies, compiled UI, databases and browser reports are ignored local outputs. The cloud draft stores complete installation and startup instructions separately.

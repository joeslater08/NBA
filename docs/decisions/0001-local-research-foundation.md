# ADR 0001: Local, append-only research foundation

Status: accepted within the user's requested default stack and v0.1 scope.

Use FastAPI, Pydantic, SQLAlchemy, Alembic and SQLite with React/TypeScript/Vite. Serve the compiled UI and API together; avoid external infrastructure. Store locked predictions separately from observed settlements, derive virtual balances, and use explicit market rules. Use synthetic data until an approved source exists.

Consequences: simple local startup and testable mathematics; no hosting or authentication guarantees. SQLite triggers enforce immutable financial/research rows. Future PostgreSQL support needs equivalent enforcement. Corrections and statistical modelling require dedicated later workflows, not edits to original observations. Plain CSS keeps this first UI small; visualisation dependencies can follow actual model outputs. Numerical packages are not installed speculatively.

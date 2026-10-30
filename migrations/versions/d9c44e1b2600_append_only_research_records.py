"""Protect immutable research records at the SQLite database boundary."""

from alembic import op

revision = "d9c44e1b2600"
down_revision = "f69a890d1c75"
branch_labels = None
depends_on = None
TABLES = (
    "predictions",
    "settlements",
    "paper_entries",
    "parlays",
    "parlay_legs",
    "audit_events",
)


def upgrade():
    if op.get_bind().dialect.name == "sqlite":
        for table in TABLES:
            for action in ("UPDATE", "DELETE"):
                op.execute(
                    f"CREATE TRIGGER preserve_{table}_{action.lower()} BEFORE {action} ON {table} BEGIN SELECT RAISE(ABORT, 'Research records are append-only'); END"
                )


def downgrade():
    if op.get_bind().dialect.name == "sqlite":
        for table in TABLES:
            for action in ("UPDATE", "DELETE"):
                op.execute(f"DROP TRIGGER IF EXISTS preserve_{table}_{action.lower()}")

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from scripts.backup import backup

ROOT = Path(__file__).resolve().parents[2]


def test_migration_seed_repeatability_immutability_and_backup(tmp_path):
    db_path = tmp_path / "fresh.db"
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{db_path}"}
    for command in (
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        [sys.executable, "-m", "scripts.seed"],
    ):
        subprocess.run(command, cwd=ROOT, env=env, check=True, capture_output=True, text=True)
    with sqlite3.connect(db_path) as conn:
        before = conn.execute("SELECT id, created_at FROM predictions ORDER BY id").fetchall()
        assert len(before) == 5
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute("UPDATE predictions SET odds=99")
    subprocess.run(
        [sys.executable, "-m", "scripts.seed"], cwd=ROOT, env=env, check=True, capture_output=True
    )
    with sqlite3.connect(db_path) as conn:
        assert (
            conn.execute("SELECT id, created_at FROM predictions ORDER BY id").fetchall() == before
        )
        assert conn.execute("SELECT count(*) FROM settlements").fetchone()[0] == 3
    target = tmp_path / "backup.db"
    backup(db_path, target)
    with sqlite3.connect(target) as conn:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        assert conn.execute("SELECT count(*) FROM predictions").fetchone()[0] == 5
    with pytest.raises(FileExistsError):
        backup(db_path, target)

"""Consistent SQLite backup, without overwriting an existing backup."""

import argparse
import sqlite3
from pathlib import Path


def backup(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise ValueError("Source database does not exist")
    # Exclusive reservation protects existing files, including the source itself.
    with destination.open("xb"):
        pass
    try:
        with (
            sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True) as src,
            sqlite3.connect(destination) as dst,
        ):
            src.backup(dst)
            if dst.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise ValueError("Backup failed integrity validation")
    except Exception:
        destination.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--source", type=Path, default=Path("nba.db"))
    args = parser.parse_args()
    backup(args.source, args.destination)
    print(f"Verified backup saved to {args.destination}")

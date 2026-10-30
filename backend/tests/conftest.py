from datetime import timedelta

import pytest
from backend.app import models as m
from backend.app.database import Base, get_db
from backend.app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture()
def database():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    @event.listens_for(engine, "connect")
    def fk(conn, _):
        conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    sessions = sessionmaker(engine, expire_on_commit=False)
    with sessions() as db:
        db.add_all(
            [
                m.Team(id="home", name="Home", abbreviation="HOM"),
                m.Team(id="away", name="Away", abbreviation="AWY"),
                m.Team(id="other", name="Other", abbreviation="OTH"),
                m.Analyst(id="analyst", name="Test analyst"),
            ]
        )
        db.flush()
        db.add(m.Player(id="player", name="Test Player", team_id="home"))
        db.flush()
        db.add(
            m.PlayerAssignment(
                player_id="player", team_id="home", effective_from=m.now() - timedelta(days=100)
            )
        )
        db.add_all(
            [
                m.Game(
                    id="future",
                    season="2026-27",
                    start_utc=m.now() + timedelta(days=1),
                    home_team_id="home",
                    away_team_id="away",
                    source="Test fixture",
                ),
                m.Game(
                    id="past",
                    season="2026-27",
                    start_utc=m.now() - timedelta(days=1),
                    home_team_id="home",
                    away_team_id="away",
                    source="Test fixture",
                ),
            ]
        )
        db.commit()
    yield sessions
    engine.dispose()


@pytest.fixture()
def client(database):
    def override():
        with database() as db:
            yield db

    app.dependency_overrides[get_db] = override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def payload():
    return {
        "analyst_id": "analyst",
        "game_id": "future",
        "player_id": "player",
        "market": {
            "kind": "points",
            "direction": "over",
            "threshold": 20.5,
            "includes_overtime": True,
            "dnp": "void",
            "postponed": "pending",
            "rule_reference": "Verified test rules",
        },
        "odds": 1.9,
        "evidence": "Test source",
    }


@pytest.fixture()
def advance_clock(monkeypatch):
    future = m.now() + timedelta(days=2)
    return lambda: monkeypatch.setattr(m, "now", lambda: future)

"""Idempotent synthetic fixture and result examples; never real analyst performance."""

from datetime import timedelta

from sqlalchemy import select

from backend.app import models as m
from backend.app.database import SessionLocal
from backend.app.schemas import PredictionInput, ResultInput
from backend.app.services import add, create_prediction, settle_prediction

INITIAL_ANALYSTS = [
    "Exclusive Analytics",
    "HooveLocks",
    "WH.STS",
    "Keezylocks",
    "Capper Kale",
    "RotoBot AI",
]


def seed():
    with SessionLocal() as db:
        for name in INITIAL_ANALYSTS:
            if not db.scalar(select(m.Analyst).where(m.Analyst.name == name)):
                add(
                    db,
                    m.Analyst,
                    {
                        "name": name,
                        "notes": "Registry entry only. No historical record supplied.",
                    },
                )
        if db.get(m.Team, "demo-home"):
            db.commit()
            return
        home = add(
            db,
            m.Team,
            {
                "id": "demo-home",
                "name": "Example City Comets",
                "abbreviation": "EXC",
                "synthetic": True,
            },
        )
        away = add(
            db,
            m.Team,
            {
                "id": "demo-away",
                "name": "Example Bay Owls",
                "abbreviation": "EXO",
                "synthetic": True,
            },
        )
        player = add(
            db,
            m.Player,
            {
                "id": "demo-player",
                "name": "Example Player",
                "team_id": home.id,
                "position": "G",
                "synthetic": True,
            },
        )
        add(
            db,
            m.PlayerAssignment,
            {
                "player_id": player.id,
                "team_id": home.id,
                "effective_from": m.now() - timedelta(days=365),
            },
        )
        analyst = add(
            db,
            m.Analyst,
            {
                "id": "demo-analyst",
                "name": "Demonstration Research",
                "notes": "Synthetic examples only",
            },
        )
        upcoming = add(
            db,
            m.Game,
            {
                "id": "demo-upcoming",
                "season": "DEMO",
                "start_utc": m.now() + timedelta(days=7),
                "home_team_id": home.id,
                "away_team_id": away.id,
                "source": "Synthetic demonstration — not an NBA fixture",
                "synthetic": True,
            },
        )
        past = add(
            db,
            m.Game,
            {
                "id": "demo-completed",
                "season": "DEMO",
                "start_utc": m.now() - timedelta(days=1),
                "home_team_id": away.id,
                "away_team_id": home.id,
                "status": "completed",
                "home_score": 92,
                "away_score": 101,
                "source": "Synthetic demonstration",
                "synthetic": True,
            },
        )

        def prediction(game, threshold, odds, created, kind="points"):
            return create_prediction(
                db,
                PredictionInput(
                    analyst_id=analyst.id,
                    game_id=game.id,
                    player_id=player.id,
                    market={
                        "kind": kind,
                        "direction": "over",
                        "threshold": threshold,
                        "includes_overtime": True,
                        "dnp": "void",
                        "postponed": "pending",
                        "rule_reference": "Synthetic full-game example rule",
                    },
                    odds=odds,
                    evidence="Synthetic example — no external record",
                    synthetic=True,
                    created_at=created,
                ),
            )[0]

        prediction(upcoming, 20.5, 1.9, m.now())
        prediction(upcoming, 7.5, 1.8, m.now(), kind="rebounds")
        for threshold, odds, actual in [
            (18.5, 1.9, 22),
            (25.5, 2.0, 22),
            (22, 1.8, 22),
        ]:
            p = prediction(past, threshold, odds, past.start_utc - timedelta(hours=3))
            add(
                db,
                m.PaperEntry,
                {
                    "prediction_id": p.id,
                    "units": 1,
                    "recorded_odds": odds,
                    "synthetic": True,
                    "created_at": past.start_utc - timedelta(hours=2),
                },
            )
            settle_prediction(
                db,
                p.id,
                ResultInput(
                    actual=actual,
                    game_status="completed",
                    includes_overtime=True,
                    evidence="Synthetic box score",
                    reason="Deterministic demonstration outcome",
                ),
            )
        db.commit()


if __name__ == "__main__":
    seed()
    print(
        "Analyst registry and synthetic examples ready. No real analyst results created."
    )

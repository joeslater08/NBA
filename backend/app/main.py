import csv
import io
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models as m
from . import schemas as s
from . import services as svc
from .database import get_db


@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(title="NBA Intelligence Lab", version="0.1.0", lifespan=lifespan)
DB = Annotated[Session, Depends(get_db)]


@app.exception_handler(IntegrityError)
async def integrity_error(request, exc):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=409, content={"detail": "Duplicate record or invalid database reference"}
    )


def serial(obj):
    if isinstance(obj, dict):
        return jsonable_encoder(obj)
    result = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = svc.utc(value).isoformat()
    return jsonable_encoder(result)


@app.get("/api/v1/health")
def health(db: DB):
    db.execute(select(m.Team).limit(1))
    return {"status": "ok", "version": "0.1.0", "mode": "local-paper-research"}


@app.get("/api/v1/{resource}")
def list_resource(resource: str, db: DB, synthetic: bool = False):
    tables = {
        "teams": m.Team,
        "players": m.Player,
        "games": m.Game,
        "analysts": m.Analyst,
        "predictions": m.Prediction,
        "parlays": m.Parlay,
        "paper-entries": m.PaperEntry,
        "audit-events": m.AuditEvent,
    }
    cls = tables.get(resource)
    if not cls:
        raise HTTPException(404, "Unknown resource")
    query = select(cls)
    if hasattr(cls, "synthetic"):
        query = query.where(cls.synthetic == synthetic)
    rows = db.scalars(query).all()
    if cls == m.Parlay:
        return [serial(svc.parlay_details(db, r)) for r in rows]
    if cls == m.PaperEntry:
        return [serial(svc.paper_details(db, r)) for r in rows]
    return [
        serial(r) | ({"outcome": svc.outcome(db, r.id)} if cls == m.Prediction else {})
        for r in rows
    ]


@app.post("/api/v1/teams", status_code=201)
def create_team(data: s.TeamInput, db: DB):
    obj = svc.add(db, m.Team, data.model_dump())
    db.commit()
    return serial(obj)


@app.post("/api/v1/players", status_code=201)
def create_player(data: s.PlayerInput, db: DB):
    team = svc.require(db, m.Team, data.team_id)
    if team.synthetic != data.synthetic:
        raise HTTPException(422, "Player and team data modes must match")
    obj = svc.add(db, m.Player, data.model_dump(exclude={"assignment_start"}))
    svc.add(
        db,
        m.PlayerAssignment,
        {
            "player_id": obj.id,
            "team_id": team.id,
            "effective_from": data.assignment_start or m.now(),
        },
    )
    db.commit()
    return serial(obj)


@app.post("/api/v1/games", status_code=201)
def create_game(data: s.GameInput, db: DB):
    svc.validate_fixture(db, data)
    obj = svc.add(db, m.Game, data.model_dump())
    db.commit()
    return serial(obj)


@app.post("/api/v1/games/{identifier}/result")
def record_game_result(identifier: str, data: s.GameResultInput, db: DB):
    game = svc.require(db, m.Game, identifier)
    if game.status in ("completed", "cancelled"):
        raise HTTPException(
            409, "Final fixture record is preserved; use an explicit future correction workflow"
        )
    if svc.utc(game.start_utc) > m.now() and data.status in ("live", "completed"):
        raise HTTPException(422, "Fixture has not started")
    previous = {"status": game.status, "home_score": game.home_score, "away_score": game.away_score}
    game.status, game.home_score, game.away_score = data.status, data.home_score, data.away_score
    game.verified_at = m.now()
    svc.add(
        db,
        m.AuditEvent,
        {
            "entity_id": identifier,
            "action": "fixture_result",
            "details": {"previous": previous, **data.model_dump()},
        },
    )
    db.commit()
    return serial(game)


@app.post("/api/v1/analysts", status_code=201)
def create_analyst(data: s.AnalystInput, db: DB):
    obj = svc.add(db, m.Analyst, data.model_dump())
    db.commit()
    return serial(obj)


@app.post("/api/v1/predictions/preview")
def preview_prediction(data: s.PredictionInput, db: DB):
    return {"warnings": svc.prediction_warnings(db, data)}


@app.post("/api/v1/predictions", status_code=201)
def create_prediction(data: s.PredictionInput, db: DB):
    obj, warnings = svc.create_prediction(db, data)
    db.commit()
    return {**serial(obj), "warnings": warnings}


@app.post("/api/v1/predictions/{identifier}/grade")
def grade_prediction(identifier: str, data: s.ResultInput, db: DB):
    result = svc.settle_prediction(db, identifier, data)
    db.commit()
    return serial(result)


@app.post("/api/v1/parlays", status_code=201)
def create_parlay(data: s.ParlayInput, db: DB):
    svc.require(db, m.Analyst, data.analyst_id)
    if len(set(data.prediction_ids)) != len(data.prediction_ids):
        raise HTTPException(422, "Duplicated legs are not permitted")
    legs = [svc.require(db, m.Prediction, i) for i in data.prediction_ids]
    if len({(p.game_id, p.selection_key) for p in legs}) != len(legs):
        raise HTTPException(
            422, "Repeated selection from different sources is still a duplicate leg"
        )
    if any(svc.outcome(db, p.id) != "pending" or svc.utc(p.game_start_at) <= m.now() for p in legs):
        raise HTTPException(422, "Parlays must be recorded before every leg starts")
    warnings = ["Joint probability unavailable; independence has not been established"]
    if len({p.game_id for p in legs}) < len(legs):
        warnings.append(
            "Correlated selections: multiple legs share a game; verify combined price and settlement rules"
        )
    if any(p.odds is None for p in legs):
        warnings.append("Missing individual odds; a revised void-leg return may be unavailable")
    if data.slate_date:
        from zoneinfo import ZoneInfo

        if any(
            svc.utc(p.game_start_at).astimezone(ZoneInfo("Europe/London")).date().isoformat()
            != data.slate_date
            for p in legs
        ):
            raise HTTPException(422, "Fixture outside the selected UK-date slate")
    if len({p.synthetic for p in legs}) != 1:
        raise HTTPException(422, "Cannot mix demonstration and real selections")
    obj = svc.add(
        db,
        m.Parlay,
        {
            "analyst_id": data.analyst_id,
            "displayed_odds": data.displayed_odds,
            "void_rule": data.void_rule,
            "rule_reference": data.rule_reference,
            "notes": data.notes,
            "synthetic": legs[0].synthetic,
        },
    )
    for p in legs:
        svc.add(db, m.ParlayLeg, {"parlay_id": obj.id, "prediction_id": p.id})
    db.commit()
    return {**serial(svc.parlay_details(db, obj)), "warnings": warnings}


@app.post("/api/v1/paper-entries", status_code=201)
def create_paper(data: s.PaperInput, db: DB):
    if data.prediction_id:
        target = svc.require(db, m.Prediction, data.prediction_id)
        if svc.outcome(db, target.id) != "pending" or svc.utc(target.game_start_at) <= m.now():
            raise HTTPException(422, "Paper entries must precede fixture start and settlement")
        odds = target.odds
    else:
        target = svc.require(db, m.Parlay, data.parlay_id)
        details = svc.parlay_details(db, target)
        if any(
            svc.utc(svc.require(db, m.Prediction, i).game_start_at) <= m.now()
            for i in details["prediction_ids"]
        ):
            raise HTTPException(422, "Paper entries must precede all fixture starts")
        odds = target.displayed_odds
    obj = svc.add(
        db,
        m.PaperEntry,
        {**data.model_dump(), "recorded_odds": odds, "synthetic": target.synthetic},
    )
    db.commit()
    return serial(svc.paper_details(db, obj))


@app.get("/api/v1/nba/summary")
def summary(db: DB, synthetic: bool = False):
    predictions = db.scalars(select(m.Prediction).where(m.Prediction.synthetic == synthetic)).all()
    entries = [
        svc.paper_details(db, e)
        for e in db.scalars(select(m.PaperEntry).where(m.PaperEntry.synthetic == synthetic)).all()
    ]
    return {
        "schema_version": "1.0",
        "generated_at": m.now(),
        "synthetic": synthetic,
        "games": len(db.scalars(select(m.Game).where(m.Game.synthetic == synthetic)).all()),
        "predictions": len(predictions),
        "awaiting_grading": sum(svc.outcome(db, p.id) == "pending" for p in predictions),
        "portfolio": svc.portfolio_metrics(entries),
        "model_status": "Not implemented — planned for v0.3",
        "data_health": "Demonstration data only"
        if synthetic
        else "Manual data — verify source freshness",
    }


@app.get("/api/v1/nba/analysts")
def analyst_stats(db: DB, synthetic: bool = False):
    result = []
    for a in db.scalars(select(m.Analyst)).all():
        ps = db.scalars(
            select(m.Prediction).where(
                m.Prediction.analyst_id == a.id, m.Prediction.synthetic == synthetic
            )
        ).all()
        counts = {
            key: sum(svc.outcome(db, p.id) == key for p in ps)
            for key in ("win", "loss", "push", "void", "pending")
        }
        decisive = counts["win"] + counts["loss"]
        result.append(
            {
                **serial(a),
                "predictions": len(ps),
                **counts,
                "hit_rate": counts["win"] / decisive if decisive else None,
                "average_odds": sum(float(p.odds) for p in ps if p.odds is not None)
                / sum(p.odds is not None for p in ps)
                if any(p.odds is not None for p in ps)
                else None,
            }
        )
    return result


@app.get("/api/v1/nba/paper-performance")
def paper_performance(db: DB, synthetic: bool = False):
    return summary(db, synthetic)["portfolio"]


@app.get("/api/v1/nba/model-performance")
def model_performance():
    return {
        "status": "unavailable",
        "reason": "Forecasting and validation are planned for v0.3–v0.5",
        "metrics": None,
    }


@app.get("/api/v1/nba/recent-results")
def recent_results(db: DB, synthetic: bool = False):
    rows = db.scalars(
        select(m.Settlement)
        .join(m.Prediction)
        .where(m.Prediction.synthetic == synthetic)
        .order_by(m.Settlement.graded_at.desc())
        .limit(100)
    ).all()
    return [serial(r) for r in rows]


@app.get("/api/v1/nba/data-health")
def data_health(db: DB, synthetic: bool = False):
    games = db.scalars(select(m.Game).where(m.Game.synthetic == synthetic)).all()
    return {
        "provider": "manual",
        "synthetic": synthetic,
        "last_successful_sync": None,
        "games": len(games),
        "unverified_games": sum(g.verified_at is None for g in games),
        "automatic_refresh": False,
    }


@app.get("/api/v1/export/{resource}")
def export_csv(resource: str, db: DB, synthetic: bool = False):
    rows = list_resource(resource, db, synthetic)
    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        for row in rows:
            safe = {}
            for k, v in row.items():
                v = str(v) if isinstance(v, (dict, list)) else v
                safe[k] = (
                    "'" + v
                    if isinstance(v, str) and v.startswith(("=", "+", "-", "@", "\t", "\r"))
                    else v
                )
            writer.writerow(safe)
    return Response(
        output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{resource}.csv"'},
    )


@app.post("/api/v1/import/{resource}")
def import_csv(resource: str, data: s.CSVInput, db: DB):
    from .providers.manual_csv import ingest

    return ingest(resource, data, db)


# API routes precede SPA fallback so unknown API resources remain JSON errors.
dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if dist.exists():
    app.mount("/", StaticFiles(directory=dist, html=True), name="dashboard")

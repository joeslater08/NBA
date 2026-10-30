import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models as m
from . import schemas
from .database import Base
from .markets import Market, combined_odds, grade, parlay_outcome, profit


def require[T: Base](db: Session, cls: type[T], identifier: str) -> T:
    obj = db.get(cls, identifier)
    if obj is None:
        raise HTTPException(422, f"Unknown {cls.__name__.lower()} identifier")
    return obj


def utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def add[T: Base](db: Session, cls: type[T], data: dict[str, Any]) -> T:
    obj = cls(**data)
    db.add(obj)
    db.flush()
    return obj


def prediction_warnings(db: Session, data: schemas.PredictionInput) -> list[str]:
    game = require(db, m.Game, data.game_id)
    require(db, m.Analyst, data.analyst_id)
    warnings = []
    teams = {game.home_team_id, game.away_team_id}
    if data.player_id:
        player = require(db, m.Player, data.player_id)
        assignments = db.scalars(
            select(m.PlayerAssignment).where(m.PlayerAssignment.player_id == player.id)
        ).all()
        historical = [
            a.team_id
            for a in assignments
            if utc(a.effective_from) <= utc(game.start_utc)
            and (a.effective_to is None or utc(game.start_utc) < utc(a.effective_to))
        ]
        if len(historical) != 1:
            warnings.append(
                "Player team assignment at game time is unverified; record a dated assignment"
            )
        elif historical[0] not in teams:
            warnings.append("Player-team mismatch: player is not assigned to this fixture")
    if data.team_id and data.team_id not in teams:
        warnings.append("Selected team does not play in this fixture")
    if data.odds is None:
        warnings.append("Missing recorded odds: winning return and complete ROI unavailable")
    if game.status in ("postponed", "cancelled"):
        warnings.append(f"Fixture is {game.status}")
    return warnings


def create_prediction(db: Session, data: schemas.PredictionInput) -> tuple[m.Prediction, list[str]]:
    warnings = prediction_warnings(db, data)
    if any("mismatch" in x or "does not play" in x or "unverified" in x for x in warnings):
        raise HTTPException(422, {"warnings": warnings})
    game = require(db, m.Game, data.game_id)
    player_market = data.market.kind not in ("moneyline", "spread", "team_total", "game_total")
    if player_market != bool(data.player_id):
        raise HTTPException(
            422, "Player markets require a player; team/game markets must not select a player"
        )
    if data.market.kind in ("moneyline", "spread", "team_total") and not data.team_id:
        raise HTTPException(422, "Select the team to which the result applies")
    if player_market and data.team_id:
        raise HTTPException(
            422, "Player markets identify the team through the dated player assignment"
        )
    if data.market.kind == "game_total" and data.team_id:
        raise HTTPException(422, "Game totals apply to both teams")
    timestamp = data.created_at or m.now()
    if utc(timestamp) >= utc(game.start_utc):
        raise HTTPException(422, "Prediction timestamp must precede fixture start")
    if utc(timestamp) > m.now():
        raise HTTPException(422, "Prediction timestamp cannot be in the future")
    if data.synthetic != game.synthetic or (
        data.player_id and require(db, m.Player, data.player_id).synthetic != data.synthetic
    ):
        raise HTTPException(422, "Synthetic and real data must stay separate")
    market = data.market.model_dump()
    key = hashlib.sha256(
        json.dumps(
            [
                data.player_id,
                data.team_id,
                {k: v for k, v in market.items() if k != "rule_reference"},
            ],
            sort_keys=True,
        ).encode()
    ).hexdigest()
    existing = db.scalar(
        select(m.Prediction).where(
            m.Prediction.analyst_id == data.analyst_id,
            m.Prediction.game_id == data.game_id,
            m.Prediction.selection_key == key,
        )
    )
    if existing:
        raise HTTPException(
            409, "Duplicate prediction; reuse the existing selection for another parlay"
        )
    payload = data.model_dump(exclude={"created_at", "market"})
    obj = add(
        db,
        m.Prediction,
        {
            **payload,
            "market": market,
            "selection_key": key,
            "created_at": timestamp,
            "game_start_at": game.start_utc,
        },
    )
    add(
        db,
        m.AuditEvent,
        {
            "entity_id": obj.id,
            "action": "prediction_locked",
            "details": {
                "evidence": data.evidence,
                "historical_entry": data.created_at is not None,
                "entered_after_game_start": m.now() >= utc(game.start_utc),
            },
        },
    )
    return obj, warnings


def settlement(db: Session, prediction_id: str) -> m.Settlement | None:
    return db.scalar(select(m.Settlement).where(m.Settlement.prediction_id == prediction_id))


def outcome(db: Session, prediction_id: str) -> str:
    s = settlement(db, prediction_id)
    return s.outcome if s else "pending"


def settle_prediction(
    db: Session, identifier: str, data: schemas.ResultInput
) -> m.Settlement | dict[str, Any]:
    prediction = require(db, m.Prediction, identifier)
    if settlement(db, identifier):
        raise HTTPException(409, "Already graded; original settlement is preserved")
    if data.includes_overtime != prediction.market["includes_overtime"]:
        raise HTTPException(422, "Result overtime scope does not match the locked market rules")
    if utc(prediction.game_start_at) > m.now() and data.game_status not in (
        "postponed",
        "cancelled",
    ):
        raise HTTPException(422, "Cannot grade a fixture before its start")
    if (
        data.actual is not None
        and prediction.market["kind"] not in ("spread", "moneyline")
        and data.actual < 0
    ):
        raise HTTPException(422, "Statistical results cannot be negative")
    if data.actual is not None and not data.actual.is_integer():
        raise HTTPException(422, "NBA score/statistic results must be integer counts")
    result = grade(Market(**prediction.market), data.actual, data.game_status, data.dnp)
    if result == "pending":
        return {
            "outcome": "pending",
            "preserve": True,
            "message": "No settlement saved: fixture or result is incomplete",
        }
    row = add(
        db,
        m.Settlement,
        {
            "prediction_id": identifier,
            "outcome": result,
            "actual": data.actual,
            "reason": data.reason,
            "evidence": data.evidence,
        },
    )
    add(
        db,
        m.AuditEvent,
        {"entity_id": identifier, "action": "settled", "details": data.model_dump()},
    )
    return row


def parlay_details(db: Session, parlay: m.Parlay) -> dict[str, Any]:
    ids = db.scalars(
        select(m.ParlayLeg.prediction_id).where(m.ParlayLeg.parlay_id == parlay.id)
    ).all()
    legs = [require(db, m.Prediction, i) for i in ids]
    states = [(outcome(db, p.id), p.odds) for p in legs]
    state = parlay_outcome([s for s, _ in states])
    if parlay.void_rule == "void_entire" and any(s in ("void", "push") for s, _ in states):
        state = "void"
    # Displayed original price cannot determine a revised void-leg price. Use recorded leg odds.
    revised = any(s in ("void", "push") for s, _ in states)
    odds = (
        combined_odds(states)
        if revised and parlay.void_rule == "reduce_void_legs"
        else parlay.displayed_odds
    )
    return {
        "id": parlay.id,
        "analyst_id": parlay.analyst_id,
        "prediction_ids": ids,
        "outcome": state,
        "displayed_odds": parlay.displayed_odds,
        "calculated_odds": combined_odds([("pending", p.odds) for p in legs]),
        "settlement_odds": odds,
        "synthetic": parlay.synthetic,
        "notes": parlay.notes,
        "void_rule": parlay.void_rule,
        "rule_reference": parlay.rule_reference,
        "probability": None,
    }


def paper_details(db: Session, entry: m.PaperEntry) -> dict[str, Any]:
    if entry.prediction_id:
        state = outcome(db, entry.prediction_id)
        row = settlement(db, entry.prediction_id)
        settled_at = utc(row.graded_at) if row else None
        odds = entry.recorded_odds
    else:
        details = parlay_details(db, require(db, m.Parlay, entry.parlay_id))
        state = details["outcome"]
        ids = details["prediction_ids"]
        dates = [utc(s.graded_at) for i in ids if (s := settlement(db, i)) is not None]
        settled_at = max(dates) if dates and state != "pending" else None
        revised = any(outcome(db, i) in ("push", "void") for i in ids)
        odds = details["settlement_odds"] if revised else entry.recorded_odds
    return {
        "id": entry.id,
        "prediction_id": entry.prediction_id,
        "parlay_id": entry.parlay_id,
        "units": float(entry.units),
        "recorded_odds": entry.recorded_odds,
        "outcome": state,
        "profit_loss": profit(entry.units, odds, state),
        "synthetic": entry.synthetic,
        "created_at": utc(entry.created_at),
        "settled_at": settled_at,
    }


def portfolio_metrics(entries: list[dict[str, Any]]) -> dict[str, Any]:
    settled = [e for e in entries if e["outcome"] != "pending"]
    known = [e for e in settled if e["profit_loss"] is not None]
    unknown = len(settled) - len(known)
    units = sum(Decimal(str(e["units"])) for e in settled)
    pnl = sum(Decimal(str(e["profit_loss"])) for e in known)
    balance = peak = drawdown = Decimal(0)
    streak = longest = 0
    for e in sorted(
        known, key=lambda e: (e.get("settled_at") or e.get("created_at", ""), e.get("id", ""))
    ):
        balance += Decimal(str(e["profit_loss"]))
        peak = max(peak, balance)
        drawdown = max(drawdown, peak - balance)
        streak = streak + 1 if e["outcome"] == "loss" else 0
        longest = max(longest, streak)
    complete = not unknown
    return {
        "entries": len(entries),
        "settled_entries": len(settled),
        "total_units": sum(e["units"] for e in entries),
        "settled_units": float(units),
        "net_profit_loss": float(pnl) if complete else None,
        "known_profit_loss": float(pnl),
        "roi": float(pnl / units) if units and complete else None,
        "unpriced_settled_entries": unknown,
        "maximum_drawdown": float(drawdown) if complete else None,
        "longest_losing_streak": longest if complete else None,
    }


def validate_fixture(db: Session, data: schemas.GameInput) -> None:
    home = require(db, m.Team, data.home_team_id)
    away = require(db, m.Team, data.away_team_id)
    if home.id == away.id or home.synthetic != data.synthetic or away.synthetic != data.synthetic:
        raise HTTPException(422, "Invalid fixture: distinct teams and matching data modes required")
    if db.scalar(
        select(m.Game).where(
            m.Game.home_team_id == home.id,
            m.Game.away_team_id == away.id,
            m.Game.start_utc == data.start_utc,
        )
    ):
        raise HTTPException(
            409, "Duplicate fixture: these teams already have a game at this start time"
        )

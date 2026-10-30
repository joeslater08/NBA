from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def uid():
    return str(uuid4())


def now():
    return datetime.now(UTC)


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uid)
    name: Mapped[str]
    abbreviation: Mapped[str] = mapped_column(unique=True)
    conference: Mapped[str | None]
    division: Mapped[str | None]
    active: Mapped[bool] = mapped_column(default=True)
    synthetic: Mapped[bool] = mapped_column(default=False)


class Player(Base):
    __tablename__ = "players"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    name: Mapped[str]
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    position: Mapped[str | None]
    secondary_position: Mapped[str | None]
    height_cm: Mapped[float | None]
    status: Mapped[str] = mapped_column(default="unknown")
    provider_ids: Mapped[dict] = mapped_column(JSON, default=dict)
    synthetic: Mapped[bool] = mapped_column(default=False)


class PlayerAssignment(Base):
    __tablename__ = "player_assignments"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    effective_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Game(Base):
    __tablename__ = "games"
    __table_args__ = (CheckConstraint("home_team_id != away_team_id"),)
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    season: Mapped[str]
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    home_team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    status: Mapped[str] = mapped_column(default="scheduled")
    overtime_periods: Mapped[int | None]
    home_score: Mapped[int | None]
    away_score: Mapped[int | None]
    source: Mapped[str]
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    synthetic: Mapped[bool] = mapped_column(default=False)


class Analyst(Base):
    __tablename__ = "analysts"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(unique=True)
    source_type: Mapped[str] = mapped_column(default="manual")
    platform: Mapped[str | None]
    profile_url: Mapped[str | None]
    notes: Mapped[str] = mapped_column(default="")
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Prediction(Base):
    __tablename__ = "predictions"
    __table_args__ = (
        UniqueConstraint("analyst_id", "game_id", "selection_key"),
        CheckConstraint("odds IS NULL OR odds > 1"),
    )
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    analyst_id: Mapped[str] = mapped_column(ForeignKey("analysts.id"))
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"))
    player_id: Mapped[str | None] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[str | None] = mapped_column(ForeignKey("teams.id"))
    market: Mapped[dict] = mapped_column(JSON)
    selection_key: Mapped[str]
    odds: Mapped[float | None] = mapped_column(Numeric(12, 6))
    bookmaker: Mapped[str | None]
    evidence: Mapped[str]
    notes: Mapped[str] = mapped_column(default="")
    model_version: Mapped[str | None]
    projected_mean: Mapped[float | None]
    projected_median: Mapped[float | None]
    projected_standard_deviation: Mapped[float | None]
    estimated_probability: Mapped[float | None]
    confidence_interval: Mapped[dict | None] = mapped_column(JSON)
    confidence_score: Mapped[float | None]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    locked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    game_start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    synthetic: Mapped[bool] = mapped_column(default=False)


@event.listens_for(Prediction, "before_update")
def immutable_prediction(*_):
    raise ValueError(
        "Locked predictions are immutable; create a correction with an audit reference"
    )


class Settlement(Base):
    __tablename__ = "settlements"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    prediction_id: Mapped[str] = mapped_column(ForeignKey("predictions.id"), unique=True)
    outcome: Mapped[str]
    actual: Mapped[float | None]
    reason: Mapped[str]
    evidence: Mapped[str]
    graded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Parlay(Base):
    __tablename__ = "parlays"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    analyst_id: Mapped[str] = mapped_column(ForeignKey("analysts.id"))
    displayed_odds: Mapped[float | None] = mapped_column(Numeric(12, 6))
    void_rule: Mapped[str] = mapped_column(default="reduce_void_legs")
    rule_reference: Mapped[str] = mapped_column(default="Unverified legacy rules")
    notes: Mapped[str] = mapped_column(default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    synthetic: Mapped[bool] = mapped_column(default=False)


class ParlayLeg(Base):
    __tablename__ = "parlay_legs"
    parlay_id: Mapped[str] = mapped_column(ForeignKey("parlays.id"), primary_key=True)
    prediction_id: Mapped[str] = mapped_column(ForeignKey("predictions.id"), primary_key=True)


class PaperEntry(Base):
    __tablename__ = "paper_entries"
    __table_args__ = (
        CheckConstraint("units > 0"),
        CheckConstraint("(prediction_id IS NULL) != (parlay_id IS NULL)"),
    )
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    prediction_id: Mapped[str | None] = mapped_column(ForeignKey("predictions.id"))
    parlay_id: Mapped[str | None] = mapped_column(ForeignKey("parlays.id"))
    units: Mapped[float] = mapped_column(Numeric(12, 4))
    recorded_odds: Mapped[float | None] = mapped_column(Numeric(12, 6))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    synthetic: Mapped[bool] = mapped_column(default=False)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    entity_id: Mapped[str]
    action: Mapped[str]
    details: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ImportBatch(Base):
    __tablename__ = "import_batches"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    digest: Mapped[str] = mapped_column(unique=True)
    source: Mapped[str]
    row_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


for _model in (Prediction, Settlement, PaperEntry, Parlay, ParlayLeg, AuditEvent):

    @event.listens_for(_model, "before_update")
    @event.listens_for(_model, "before_delete")
    def protect_research_records(*_):
        raise ValueError("Research records are append-only")


class TeamSeason(Base):
    __tablename__ = "team_seasons"
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    season: Mapped[str] = mapped_column(primary_key=True)
    conference: Mapped[str | None]
    division: Mapped[str | None]


class PlayerGameLog(Base):
    __tablename__ = "player_game_logs"
    __table_args__ = (UniqueConstraint("player_id", "game_id"),)
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"))
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    opponent_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
    minutes: Mapped[float | None]
    points: Mapped[int | None]
    rebounds: Mapped[int | None]
    assists: Mapped[int | None]
    steals: Mapped[int | None]
    blocks: Mapped[int | None]
    turnovers: Mapped[int | None]
    field_goal_attempts: Mapped[int | None]
    field_goals_made: Mapped[int | None]
    three_point_attempts: Mapped[int | None]
    three_pointers_made: Mapped[int | None]
    free_throw_attempts: Mapped[int | None]
    free_throws_made: Mapped[int | None]
    offensive_rebounds: Mapped[int | None]
    defensive_rebounds: Mapped[int | None]
    personal_fouls: Mapped[int | None]
    starter: Mapped[bool | None]
    availability_status: Mapped[str]
    source: Mapped[str]
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class TeamGameLog(Base):
    __tablename__ = "team_game_logs"
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    game_id: Mapped[str] = mapped_column(ForeignKey("games.id"), primary_key=True)
    possessions: Mapped[float | None]
    pace: Mapped[float | None]
    offensive_efficiency: Mapped[float | None]
    defensive_efficiency: Mapped[float | None]
    rebounds: Mapped[int | None]
    assists: Mapped[int | None]
    turnovers: Mapped[int | None]
    shooting: Mapped[dict | None] = mapped_column(JSON)
    points_in_paint: Mapped[int | None]
    opponent_statistics: Mapped[dict | None] = mapped_column(JSON)
    is_home: Mapped[bool]
    rest_days: Mapped[int | None]
    overtime_periods: Mapped[int | None]
    source: Mapped[str]
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ModelRun(Base):
    __tablename__ = "model_runs"
    __table_args__ = (
        CheckConstraint(
            "simulation_count IS NULL OR (simulation_count > 0 AND execution_status = 'completed')"
        ),
    )
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    model_name: Mapped[str]
    model_version: Mapped[str]
    git_commit_hash: Mapped[str | None]
    input_data_version: Mapped[str]
    run_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    random_seed: Mapped[int | None]
    simulation_count: Mapped[int | None]
    parameters: Mapped[dict] = mapped_column(JSON)
    output_summary: Mapped[dict | None] = mapped_column(JSON)
    runtime_seconds: Mapped[float | None]
    execution_status: Mapped[str]
    validation_status: Mapped[str]


class Provenance(Base):
    __tablename__ = "data_provenance"
    id: Mapped[str] = mapped_column(primary_key=True, default=uid)
    entity_type: Mapped[str]
    entity_id: Mapped[str]
    provider_name: Mapped[str]
    source_identifier: Mapped[str]
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    effective_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    verification_status: Mapped[str]
    source_version: Mapped[str | None]
    ingestion_errors: Mapped[dict | None] = mapped_column(JSON)
    last_successful_sync: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

from datetime import UTC
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator

from .markets import Market


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)

    @field_validator("start_utc", "created_at", "assignment_start", check_fields=False)
    @classmethod
    def normalise_utc(cls, value):
        return value.astimezone(UTC) if value is not None else None


class TeamInput(Input):
    name: str = Field(min_length=1, max_length=120)
    abbreviation: str = Field(min_length=2, max_length=8)
    conference: str | None = None
    division: str | None = None
    synthetic: bool = False


class PlayerInput(Input):
    name: str = Field(min_length=1)
    team_id: str
    position: str | None = None
    assignment_start: AwareDatetime | None = None
    synthetic: bool = False


class GameInput(Input):
    season: str = Field(min_length=4)
    start_utc: AwareDatetime
    home_team_id: str
    away_team_id: str
    source: str = Field(min_length=3)
    synthetic: bool = False


class AnalystInput(Input):
    name: str = Field(min_length=1, max_length=120)
    platform: str | None = None
    profile_url: str | None = None
    notes: str = ""


class PredictionInput(Input):
    analyst_id: str
    game_id: str
    player_id: str | None = None
    team_id: str | None = None
    market: Market
    odds: float | None = Field(default=None, gt=1, le=100000)
    bookmaker: str | None = None
    model_version: str | None = None
    evidence: str = Field(min_length=3)
    notes: str = ""
    synthetic: bool = False
    created_at: AwareDatetime | None = None


class ResultInput(Input):
    actual: float | None = None
    game_status: Literal["scheduled", "live", "completed", "postponed", "cancelled"]
    dnp: bool = False
    includes_overtime: bool
    evidence: str = Field(min_length=3)
    reason: str = Field(min_length=3)


class ParlayInput(Input):
    analyst_id: str
    prediction_ids: list[str] = Field(min_length=2, max_length=20)
    displayed_odds: float | None = Field(default=None, gt=1)
    notes: str = ""
    void_rule: Literal["reduce_void_legs", "void_entire"]
    rule_reference: str = Field(min_length=3)
    slate_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")


class PaperInput(Input):
    prediction_id: str | None = None
    parlay_id: str | None = None
    units: float = Field(default=1, gt=0, le=100000)

    @model_validator(mode="after")
    def one_target(self):
        if bool(self.prediction_id) == bool(self.parlay_id):
            raise ValueError("Choose exactly one prediction or parlay")
        return self


class CSVInput(Input):
    content: str = Field(max_length=1000000)
    source: str = Field(min_length=3)
    synthetic: bool = False
    confirm: bool = False


class GameResultInput(Input):
    status: Literal["scheduled", "live", "completed", "postponed", "cancelled"]
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    evidence: str = Field(min_length=3)

    @model_validator(mode="after")
    def final_scores(self):
        if self.status == "completed" and (self.home_score is None or self.away_score is None):
            raise ValueError("Completed fixtures require both scores")
        return self

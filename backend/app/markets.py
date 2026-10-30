"""Structured, explicitly agreed settlement rules. No bookmaker defaults are inferred."""

from decimal import Decimal
from math import isfinite, prod
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Market(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    kind: Literal[
        "points",
        "rebounds",
        "assists",
        "points_rebounds",
        "points_assists",
        "rebounds_assists",
        "points_rebounds_assists",
        "moneyline",
        "spread",
        "team_total",
        "game_total",
    ]
    direction: Literal["over", "under", "at_least", "win"]
    threshold: float = 0
    includes_overtime: bool
    dnp: Literal["void", "action"]
    postponed: Literal["void", "pending"]
    rule_reference: str = Field(min_length=3)

    @model_validator(mode="after")
    def coherent(self):
        if (self.kind == "moneyline") != (self.direction == "win"):
            raise ValueError(
                "Moneyline requires win; other markets require over, under or at_least"
            )
        if self.kind == "moneyline" and self.threshold != 0:
            raise ValueError("Moneyline threshold must be zero")
        if self.kind == "spread" and self.direction != "over":
            raise ValueError(
                "Spread uses selected-team margin plus handicap; direction must be over"
            )
        if self.kind not in ("spread", "moneyline") and self.threshold < 0:
            raise ValueError("Statistical thresholds must be non-negative")
        if self.direction == "at_least" and not self.threshold.is_integer():
            raise ValueError("Alternative thresholds must be integers")
        return self


def grade(market: Market, actual: float | None, game_status: str, dnp: bool = False) -> str:
    if game_status == "cancelled" or (game_status == "postponed" and market.postponed == "void"):
        return "void"
    if game_status != "completed":
        return "pending"
    if dnp and market.dnp == "void":
        return "void"
    if actual is None:
        return "pending"
    value, threshold = Decimal(str(actual)), Decimal(str(market.threshold))
    if market.kind == "spread":
        value, threshold = value + threshold, Decimal(0)
    if market.direction == "at_least":
        return "win" if value >= threshold else "loss"
    if value == threshold:
        return "push"
    return (
        "win"
        if ((value > threshold) if market.direction in ("over", "win") else (value < threshold))
        else "loss"
    )


def parlay_outcome(outcomes: list[str]) -> str:
    if not outcomes:
        raise ValueError("A parlay needs legs")
    if "loss" in outcomes:
        return "loss"
    if "pending" in outcomes:
        return "pending"
    return "win" if "win" in outcomes else "void"


def profit(units: Decimal | float, odds: Decimal | float | None, outcome: str) -> float | None:
    stake = Decimal(str(units))
    if outcome == "pending":
        return None
    if outcome in ("void", "push"):
        return 0.0
    if outcome == "loss":
        return float(-stake)
    return None if odds is None else float(stake * (Decimal(str(odds)) - 1))


def combined_odds(legs: list[tuple[str, Decimal | float | None]]) -> float | None:
    if any(odds is None for outcome, odds in legs if outcome not in ("void", "push")):
        return None
    return float(
        prod(Decimal(str(odds)) for outcome, odds in legs if outcome not in ("void", "push"))
    )


def break_even(odds: float) -> float:
    if not isfinite(odds) or odds <= 1:
        raise ValueError("Decimal odds must exceed one")
    return 1 / odds


def expected_value(probability: float, odds: float) -> float:
    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between zero and one")
    break_even(odds)
    return probability * odds - 1

import pytest
from backend.app.markets import (
    Market,
    break_even,
    combined_odds,
    expected_value,
    grade,
    parlay_outcome,
    profit,
)
from backend.app.services import portfolio_metrics
from pydantic import ValidationError


def market(**changes):
    return Market(
        **(
            {
                "kind": "points",
                "direction": "over",
                "threshold": 20,
                "includes_overtime": True,
                "dnp": "void",
                "postponed": "pending",
                "rule_reference": "Test rules",
            }
            | changes
        )
    )


@pytest.mark.parametrize(
    "direction,actual,expected",
    [
        ("over", 21, "win"),
        ("over", 20, "push"),
        ("over", 19, "loss"),
        ("under", 19, "win"),
        ("under", 20, "push"),
        ("under", 21, "loss"),
        ("at_least", 20, "win"),
        ("at_least", 19, "loss"),
    ],
)
def test_thresholds(direction, actual, expected):
    assert grade(market(direction=direction), actual, "completed") == expected


@pytest.mark.parametrize(
    "status,actual,expected",
    [
        ("live", 30, "pending"),
        ("scheduled", 30, "pending"),
        ("completed", None, "pending"),
        ("cancelled", None, "void"),
        ("postponed", None, "pending"),
    ],
)
def test_incomplete(status, actual, expected):
    assert grade(market(), actual, status) == expected


def test_explicit_rules():
    assert grade(market(postponed="void"), None, "postponed") == "void"
    assert grade(market(), None, "completed", dnp=True) == "void"
    assert grade(market(dnp="action"), None, "completed", dnp=True) == "pending"
    assert grade(market(dnp="action"), 0, "completed", dnp=True) == "loss"


@pytest.mark.parametrize(
    "margin,handicap,expected",
    [(5, -4.5, "win"), (4, -4, "push"), (-3, 2.5, "loss"), (-2, 2.5, "win")],
)
def test_spreads(margin, handicap, expected):
    assert grade(market(kind="spread", threshold=handicap), margin, "completed") == expected


@pytest.mark.parametrize("margin,expected", [(2, "win"), (-2, "loss"), (0, "push")])
def test_moneyline(margin, expected):
    assert (
        grade(market(kind="moneyline", direction="win", threshold=0), margin, "completed")
        == expected
    )


@pytest.mark.parametrize(
    "legs,expected",
    [
        (["win", "win"], "win"),
        (["win", "void"], "win"),
        (["push", "void"], "void"),
        (["loss", "pending"], "loss"),
        (["win", "pending"], "pending"),
        (["win", "win", "loss"], "loss"),
        (["win", "win", "win", "win"], "win"),
    ],
)
def test_parlays(legs, expected):
    assert parlay_outcome(legs) == expected


def test_parlay_void_reprices():
    assert combined_odds([("win", 2), ("void", 3), ("push", 4)]) == 2
    assert combined_odds([("win", 2), ("win", None)]) is None
    assert combined_odds([("void", None), ("win", 2)]) == 2
    assert combined_odds([("win", 1.9), ("win", 1.9)]) == 3.61


@pytest.mark.parametrize(
    "units,odds,outcome,expected",
    [
        (1, 1.9, "win", 0.9),
        (2, 1.9, "win", 1.8),
        (1, None, "win", None),
        (1, None, "loss", -1),
        (1, None, "push", 0),
        (1, None, "void", 0),
        (1, 2, "pending", None),
    ],
)
def test_returns(units, odds, outcome, expected):
    assert profit(units, odds, outcome) == expected


def test_math():
    assert break_even(2) == 0.5
    assert expected_value(0.6, 2) == pytest.approx(0.2)
    with pytest.raises(ValueError):
        break_even(1)
    with pytest.raises(ValueError):
        expected_value(1.2, 2)
    with pytest.raises(ValueError):
        break_even(float("nan"))


def test_missing_odds_never_invents_roi():
    report = portfolio_metrics([{"outcome": "win", "units": 1, "profit_loss": None}])
    assert report["roi"] is None and report["net_profit_loss"] is None
    assert report["unpriced_settled_entries"] == 1


def test_portfolio_roi_and_drawdown():
    rows = [
        {"id": str(i), "created_at": str(i), "outcome": o, "units": 1, "profit_loss": p}
        for i, (o, p) in enumerate([("win", 1), ("loss", -1), ("loss", -1), ("push", 0)])
    ]
    result = portfolio_metrics(rows)
    assert result["roi"] == -0.25 and result["maximum_drawdown"] == 2
    assert result["longest_losing_streak"] == 2


@pytest.mark.parametrize(
    "changes",
    [
        {"kind": "free text"},
        {"direction": "at_least", "threshold": 7.5},
        {"threshold": float("nan")},
        {"kind": "moneyline"},
        {"threshold": -1},
        {"kind": "spread", "direction": "under"},
    ],
)
def test_invalid_market(changes):
    with pytest.raises(ValidationError):
        market(**changes)


@pytest.mark.parametrize(
    "kind",
    [
        "points_rebounds",
        "points_assists",
        "rebounds_assists",
        "points_rebounds_assists",
        "team_total",
        "game_total",
    ],
)
def test_combination_and_totals(kind):
    assert grade(market(kind=kind), 21, "completed") == "win"

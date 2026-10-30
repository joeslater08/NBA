from datetime import timedelta

import pytest
from backend.app import models as m
from sqlalchemy import select


def post(client, path, payload, expected=201):
    result = client.post("/api/v1/" + path, json=payload)
    assert result.status_code == expected, result.text
    return result.json()


def parlay(client, ids, **kw):
    return post(
        client,
        "parlays",
        {
            "analyst_id": "analyst",
            "prediction_ids": ids,
            "void_rule": "reduce_void_legs",
            "rule_reference": "Verified test accumulator",
            **kw,
        },
    )


def settle(client, p, actual=25, dnp=False, **kw):
    return post(
        client,
        f"predictions/{p['id']}/grade",
        {
            "actual": actual,
            "game_status": "completed",
            "dnp": dnp,
            "includes_overtime": True,
            "evidence": "Test result",
            "reason": "Verified test",
            **kw,
        },
        200,
    )


def test_records_and_health(client):
    assert client.get("/api/v1/health").json()["status"] == "ok"
    team = post(client, "teams", {"name": "New Team", "abbreviation": "NEW"})
    post(client, "players", {"name": "New Player", "team_id": team["id"]})
    post(client, "analysts", {"name": "New analyst"})
    assert len(client.get("/api/v1/analysts").json()) == 2
    game = post(
        client,
        "games",
        {
            "season": "2026-27",
            "start_utc": (m.now() + timedelta(days=5)).isoformat(),
            "home_team_id": "home",
            "away_team_id": team["id"],
            "source": "manual verified",
        },
    )
    assert game["start_utc"].endswith("+00:00")


def test_prediction_lock_and_duplicate(client, payload, database):
    p = post(client, "predictions", payload)
    assert p["locked_at"] and p["game_start_at"]
    post(client, "predictions", payload, 409)
    payload["market"]["rule_reference"] = "Another description of same rule"
    post(client, "predictions", payload, 409)
    assert client.patch("/api/v1/predictions/" + p["id"], json={"odds": 9}).status_code in (
        404,
        405,
    )
    with database() as db:
        obj = db.get(m.Prediction, p["id"])
        obj.odds = 9
        with pytest.raises(ValueError):
            db.flush()


@pytest.mark.parametrize(
    "field,value",
    [
        ("odds", 1),
        ("odds", 0),
        ("odds", -2),
        ("game_id", "missing"),
        ("analyst_id", "missing"),
        ("player_id", "missing"),
        ("team_id", "other"),
    ],
)
def test_bad_prediction(client, payload, field, value):
    payload[field] = value
    post(client, "predictions", payload, 422)


def test_player_team_mismatch(client, payload, database):
    with database() as db:
        assignment = db.scalar(select(m.PlayerAssignment))
        assignment.team_id = "other"
        db.commit()
    report = post(client, "predictions/preview", payload, 200)
    assert any("mismatch" in w for w in report["warnings"])
    post(client, "predictions", payload, 422)


def test_missing_odds(client, payload, advance_clock):
    payload["odds"] = None
    p = post(client, "predictions", payload)
    assert any("Missing" in x for x in p["warnings"])
    e = post(client, "paper-entries", {"prediction_id": p["id"], "units": 1})
    assert e["recorded_odds"] is None and e["profit_loss"] is None
    advance_clock()
    settle(client, p)
    assert client.get("/api/v1/nba/paper-performance").json()["roi"] is None


def test_historical_entry_audited(client, payload):
    payload["game_id"] = "past"
    post(client, "predictions", payload, 422)
    payload["created_at"] = (m.now() - timedelta(days=2)).isoformat()
    p = post(client, "predictions", payload)
    assert p["created_at"] == payload["created_at"]
    audit = client.get("/api/v1/audit-events").json()
    assert audit[0]["details"]["entered_after_game_start"] is True
    post(client, "paper-entries", {"prediction_id": p["id"], "units": 1}, 422)


def test_settlement_and_analyst_records(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    advance_clock()
    assert settle(client, p)["outcome"] == "win"
    post(
        client,
        f"predictions/{p['id']}/grade",
        {
            "actual": 25,
            "game_status": "completed",
            "includes_overtime": True,
            "evidence": "Test result",
            "reason": "Verified test",
        },
        409,
    )
    original = client.get("/api/v1/predictions").json()[0]
    assert original["created_at"] == p["created_at"] and original["odds"] == 1.9
    stats = client.get("/api/v1/nba/analysts").json()[0]
    assert stats["win"] == 1 and stats["hit_rate"] == 1


def test_missing_and_scope_mismatch(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    advance_clock()
    assert settle(client, p, actual=None)["outcome"] == "pending"
    post(
        client,
        f"predictions/{p['id']}/grade",
        {
            "actual": 25,
            "game_status": "completed",
            "includes_overtime": False,
            "evidence": "Test result",
            "reason": "Verified test",
        },
        422,
    )


def test_parlay_void_and_paper(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    payload["market"]["kind"] = "rebounds"
    payload["market"]["threshold"] = 7.5
    q = post(client, "predictions", payload)
    combo = parlay(client, [p["id"], q["id"]], displayed_odds=4.2)
    assert combo["calculated_odds"] == 3.61 and combo["probability"] is None
    post(client, "paper-entries", {"parlay_id": combo["id"], "units": 2})
    assert client.get("/api/v1/nba/analysts").json()[0]["predictions"] == 2
    advance_clock()
    settle(client, p)
    settle(client, q, actual=None, dnp=True)
    entry = client.get("/api/v1/paper-entries").json()[0]
    assert entry["outcome"] == "win" and entry["profit_loss"] == 1.8
    assert client.get("/api/v1/nba/paper-performance").json()["roi"] == 0.9


def test_void_entire_convention(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    payload["market"]["threshold"] = 10.5
    q = post(client, "predictions", payload)
    combo = parlay(client, [p["id"], q["id"]], displayed_odds=3.6, void_rule="void_entire")
    post(client, "paper-entries", {"parlay_id": combo["id"], "units": 1})
    advance_clock()
    settle(client, p, actual=None, dnp=True)
    assert client.get("/api/v1/paper-entries").json()[0]["outcome"] == "void"


def test_parlay_missing_displayed_price_not_invented(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    payload["market"]["threshold"] = 10.5
    q = post(client, "predictions", payload)
    combo = parlay(client, [p["id"], q["id"]])
    e = post(client, "paper-entries", {"parlay_id": combo["id"], "units": 1})
    assert e["recorded_odds"] is None
    advance_clock()
    settle(client, p)
    settle(client, q)
    assert client.get("/api/v1/paper-entries").json()[0]["profit_loss"] is None


def test_duplicates_and_invalid_slate(client, payload):
    p = post(client, "predictions", payload)
    data = {
        "analyst_id": "analyst",
        "prediction_ids": [p["id"], p["id"]],
        "void_rule": "reduce_void_legs",
        "rule_reference": "Test rules",
    }
    post(client, "parlays", data, 422)
    payload["market"]["threshold"] = 10.5
    q = post(client, "predictions", payload)
    data["prediction_ids"] = [p["id"], q["id"]]
    data["slate_date"] = "2000-01-01"
    post(client, "parlays", data, 422)
    post(
        client,
        "paper-entries",
        {"prediction_id": p["id"], "parlay_id": "anything", "units": 1},
        422,
    )


def test_csv_atomic_preview_duplicate_and_export(client):
    data = {
        "content": "name,abbreviation\nFirst,FST\nSecond,SND\n",
        "source": "Manual CSV",
        "confirm": False,
    }
    assert post(client, "import/teams", data, 200)["valid_rows"] == 2
    assert len(client.get("/api/v1/teams").json()) == 3
    data["confirm"] = True
    assert post(client, "import/teams", data, 200)["committed"] is True
    assert post(client, "import/teams", data, 200)["errors"]
    invalid = {
        "content": "name,abbreviation\nValid,VAL\nDuplicate,HOM",
        "source": "Manual CSV",
        "confirm": True,
    }
    assert not post(client, "import/teams", invalid, 200)["committed"]
    assert len(client.get("/api/v1/teams").json()) == 5
    assert "First" in client.get("/api/v1/export/teams").text
    assert client.get("/api/v1/export/unknown").status_code == 404


def test_data_modes_and_interfaces(client, payload):
    payload["synthetic"] = True
    post(client, "predictions", payload, 422)
    assert client.get("/api/v1/nba/summary?synthetic=true").json()["predictions"] == 0
    assert client.get("/api/v1/nba/model-performance").json()["metrics"] is None
    for endpoint in ["summary", "analysts", "paper-performance", "recent-results", "data-health"]:
        assert client.get("/api/v1/nba/" + endpoint).status_code == 200


def test_invalid_fixture(client):
    data = {
        "season": "2026-27",
        "start_utc": m.now().isoformat(),
        "home_team_id": "home",
        "away_team_id": "home",
        "source": "Test fixture",
    }
    post(client, "games", data, 422)
    data["away_team_id"] = "unknown"
    post(client, "games", data, 422)


def test_csv_formula_injection(client):
    post(client, "teams", {"name": "=FORMULA()", "abbreviation": "XXX"})
    assert "'=FORMULA()" in client.get("/api/v1/export/teams").text


def test_fixture_result_preserved(client):
    result = {
        "status": "completed",
        "home_score": 99,
        "away_score": 100,
        "evidence": "Verified final result",
    }
    post(client, "games/past/result", result, 200)
    post(client, "games/past/result", result, 409)
    post(client, "games/future/result", result, 422)


def test_import_games_and_players_is_atomic(client):
    data = {
        "content": "name,team_id\nCSV Player,home",
        "source": "CSV test source",
        "confirm": False,
    }
    preview = post(client, "import/players", data, 200)
    assert preview["valid_rows"] == 1 and not preview["committed"]
    assert len(client.get("/api/v1/players").json()) == 1
    data["confirm"] = True
    assert post(client, "import/players", data, 200)["committed"]
    timestamp = (m.now() + timedelta(days=5)).isoformat()
    data = {
        "content": f"season,start_utc,home_team_id,away_team_id\n2026-27,{timestamp},home,away\n2026-27,{timestamp},home,missing",
        "source": "CSV fixture test",
        "confirm": True,
    }
    report = post(client, "import/games", data, 200)
    assert report["errors"] and not report["committed"]
    assert len(client.get("/api/v1/games").json()) == 2


def test_csv_predictions_and_model_version_storage(client, payload):
    import csv
    import io
    import json

    row = {
        **payload,
        "market": json.dumps(payload["market"]),
        "model_version": "EXTERNAL-RESEARCH-0.1",
    }
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(row))
    writer.writeheader()
    writer.writerow(row)
    data = {"content": stream.getvalue(), "source": "Synthetic test import", "confirm": True}
    assert post(client, "import/predictions", data, 200)["committed"]
    stored = client.get("/api/v1/predictions").json()[0]
    assert stored["model_version"] == "EXTERNAL-RESEARCH-0.1"
    assert stored["projected_mean"] is None


def test_utc_normalisation_and_fixture_duplicates(client):
    data = {
        "season": "2026-27",
        "start_utc": "2030-07-01T20:00:00+02:00",
        "home_team_id": "home",
        "away_team_id": "away",
        "source": "Verified fixture",
    }
    stored = post(client, "games", data)
    assert stored["start_utc"] == "2030-07-01T18:00:00+00:00"
    data["start_utc"] = "2030-07-01T18:00:00Z"
    post(client, "games", data, 409)


def test_fractional_actual_rejected(client, payload, advance_clock):
    p = post(client, "predictions", payload)
    advance_clock()
    post(
        client,
        f"predictions/{p['id']}/grade",
        {
            "actual": 20.5,
            "game_status": "completed",
            "includes_overtime": True,
            "evidence": "Test evidence",
            "reason": "Invalid fractional statistic",
        },
        422,
    )

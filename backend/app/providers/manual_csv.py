"""Manual provider: validate an entire batch before committing anything."""

import csv
import hashlib
import io
import json

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .. import models as m
from .. import schemas as s
from .. import services as svc

SCHEMAS = {
    "teams": (s.TeamInput, m.Team),
    "players": (s.PlayerInput, m.Player),
    "games": (s.GameInput, m.Game),
    "predictions": (s.PredictionInput, m.Prediction),
}


def ingest(resource: str, data: s.CSVInput, db):
    if resource not in SCHEMAS:
        raise HTTPException(404, "Unsupported import resource")
    schema, model = SCHEMAS[resource]
    reader = csv.DictReader(io.StringIO(data.content))
    if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise HTTPException(422, "CSV requires unique column headers")
    if set(reader.fieldnames) - schema.model_fields.keys():
        raise HTTPException(422, "Unknown CSV columns; use the documented import schema")
    rows, errors = [], []
    digest = hashlib.sha256((resource + str(data.synthetic) + data.content).encode()).hexdigest()
    if db.scalar(select(m.ImportBatch).where(m.ImportBatch.digest == digest)):
        return {
            "valid_rows": 0,
            "errors": [{"row": 0, "error": "This CSV has already been imported"}],
            "preview": [],
            "committed": False,
        }
    batch = db.begin_nested()
    try:
        for i, row in enumerate(reader, 2):
            if i > 5001:
                errors.append({"row": i, "error": "Maximum 5,000 rows per import"})
                break
            try:
                with db.begin_nested():
                    clean = {k: v for k, v in row.items() if v != ""}
                    clean["synthetic"] = data.synthetic
                    if resource == "games":
                        clean.setdefault("source", data.source)
                    if resource == "predictions":
                        clean["market"] = json.loads(clean.get("market", "null"))
                        clean.setdefault("evidence", data.source)
                    parsed = schema.model_validate(clean)
                    if resource == "predictions":
                        obj, _ = svc.create_prediction(db, parsed)
                    elif resource == "players":
                        team = svc.require(db, m.Team, parsed.team_id)
                        if team.synthetic != data.synthetic:
                            raise ValueError("Player and team data modes must match")
                        obj = svc.add(db, model, parsed.model_dump(exclude={"assignment_start"}))
                        svc.add(
                            db,
                            m.PlayerAssignment,
                            {
                                "player_id": obj.id,
                                "team_id": team.id,
                                "effective_from": parsed.assignment_start or m.now(),
                            },
                        )
                    elif resource == "games":
                        svc.validate_fixture(db, parsed)
                        obj = svc.add(db, model, parsed.model_dump())
                    else:
                        obj = svc.add(db, model, parsed.model_dump())
                    svc.add(
                        db,
                        m.Provenance,
                        {
                            "entity_type": resource,
                            "entity_id": obj.id,
                            "provider_name": "manual_csv",
                            "source_identifier": data.source,
                            "verification_status": "manually_imported",
                        },
                    )
                    rows.append(parsed.model_dump(mode="json"))
            except (ValueError, TypeError, IntegrityError, HTTPException) as exc:
                message = (
                    exc.detail
                    if isinstance(exc, HTTPException)
                    else "Duplicate record or invalid database reference"
                    if isinstance(exc, IntegrityError)
                    else str(exc)
                )
                errors.append({"row": i, "error": message})
        committed = bool(data.confirm and rows and not errors)
        if committed:
            svc.add(
                db, m.ImportBatch, {"digest": digest, "source": data.source, "row_count": len(rows)}
            )
            batch.commit()
            db.commit()
        else:
            batch.rollback()
        return {"valid_rows": len(rows), "errors": errors, "preview": rows, "committed": committed}
    except Exception:
        if batch.is_active:
            batch.rollback()
        raise

import { useState } from "react";
import { api, type RecordData } from "../api";
import { Field, Form, Select } from "./Forms";
export default function Settlement({
  predictions,
  parlays,
  analysts,
  done,
}: {
  predictions: RecordData[];
  parlays: RecordData[];
  analysts: RecordData[];
  done: () => Promise<void>;
}) {
  const [legs, setLegs] = useState<string[]>([]);
  return (
    <div className="form-grid">
      <Form
        title="Grade a selection"
        label="Save verified settlement"
        submit={async (d) => {
          const result = await api(`predictions/${d.prediction_id}/grade`, {
            actual: d.actual === "" ? null : Number(d.actual),
            game_status: d.game_status,
            dnp: d.dnp === "yes",
            includes_overtime: d.overtime === "yes",
            evidence: d.evidence,
            reason: d.reason,
          });
          await done();
          return result;
        }}
      >
        <Field label="Prediction">
          <Select
            rows={predictions.filter((p) => p.outcome === "pending")}
            name="prediction_id"
          />
        </Field>
        <Field label="Result (selected-team margin for spread / moneyline)">
          <input name="actual" type="number" step="0.01" />
        </Field>
        <Field label="Fixture status">
          <select name="game_status">
            <option value="completed">Completed</option>
            <option value="postponed">Postponed</option>
            <option value="cancelled">Cancelled</option>
            <option value="live">Live</option>
          </select>
        </Field>
        <Field label="Did not play?">
          <select name="dnp">
            <option value="no">No</option>
            <option value="yes">Yes</option>
          </select>
        </Field>
        <Field label="Result scope">
          <select name="overtime">
            <option value="yes">Includes overtime</option>
            <option value="no">Regulation only</option>
          </select>
        </Field>
        <Field label="Result evidence">
          <input name="evidence" required minLength={3} />
        </Field>
        <Field label="Reason / verification note">
          <input name="reason" required minLength={3} />
        </Field>
      </Form>
      <Form
        title="Create double, treble or parlay"
        submit={async (d) => {
          const response = await api("parlays", {
            analyst_id: d.analyst_id,
            prediction_ids: legs,
            void_rule: d.void_rule,
            rule_reference: d.rule_reference,
            slate_date: d.slate_date || null,
            displayed_odds: d.odds ? Number(d.odds) : null,
            notes: d.notes,
          });
          await done();
          return response;
        }}
      >
        <Field label="Source analyst">
          <Select rows={analysts} name="analyst_id" />
        </Field>
        <fieldset>
          <legend>Select at least two legs</legend>
          {predictions
            .filter((p) => p.outcome === "pending")
            .map((p) => (
              <label className="check" key={p.id}>
                <input
                  type="checkbox"
                  checked={legs.includes(p.id)}
                  onChange={(e) =>
                    setLegs(
                      e.target.checked
                        ? [...legs, p.id]
                        : legs.filter((id) => id !== p.id),
                    )
                  }
                />
                {p.name}
              </label>
            ))}
        </fieldset>
        <Field label="UK slate date (optional)">
          <input name="slate_date" type="date" />
        </Field>
        <Field label="Verified void / push convention">
          <select name="void_rule" required>
            <option value="">Confirm rule…</option>
            <option value="reduce_void_legs">
              Remove affected legs and multiply remaining leg prices
            </option>
            <option value="void_entire">Void entire parlay</option>
          </select>
        </Field>
        <Field label="Parlay rule reference">
          <input name="rule_reference" required minLength={3} />
        </Field>
        <Field label="Original displayed odds (optional)">
          <input name="odds" type="number" min="1.001" step="0.001" />
        </Field>
        <Field label="Notes">
          <textarea name="notes" />
        </Field>
        <p className="muted">
          Joint probability is unavailable. Only select the removal rule if the
          recorded terms permit multiplying remaining leg prices. Correlated
          prices and special promotions need separate verification.
        </p>
      </Form>
      <Form
        title="Record virtual paper units"
        submit={async (d) => {
          await api("paper-entries", {
            prediction_id: d.prediction_id || null,
            parlay_id: d.parlay_id || null,
            units: Number(d.units),
          });
          await done();
        }}
      >
        <Field label="Single (choose one target)">
          <select name="prediction_id">
            <option value="">None</option>
            {predictions
              .filter((p) => p.outcome === "pending")
              .map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
          </select>
        </Field>
        <Field label="Parlay (or single above)">
          <select name="parlay_id">
            <option value="">None</option>
            {parlays.map((p) => (
              <option key={p.id} value={p.id}>
                {p.id.slice(0, 8)} · {p.prediction_ids.length} legs
              </option>
            ))}
          </select>
        </Field>
        <Field label="Virtual units (£1 nominal per unit)">
          <input
            name="units"
            type="number"
            min="0.0001"
            step="0.0001"
            defaultValue="1"
            required
          />
        </Field>
        <p className="muted">
          Prices are copied from the recorded selection. No money changes hands.
        </p>
      </Form>
    </div>
  );
}

import { useState } from "react";
import { api, type RecordData, ukTime } from "../api";
import { Field, Form, Select } from "./Forms";
const kinds = [
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
];
export default function PredictionForm({
  games,
  players,
  teams,
  analysts,
  synthetic,
  done,
}: {
  games: RecordData[];
  players: RecordData[];
  teams: RecordData[];
  analysts: RecordData[];
  synthetic: boolean;
  done: () => Promise<void>;
}) {
  const [kind, setKind] = useState("points");
  const playerMarket = ![
    "moneyline",
    "spread",
    "team_total",
    "game_total",
  ].includes(kind);
  return (
    <Form
      title="Record and lock prediction"
      label="Lock prediction"
      submit={async (d) => {
        const body = {
          analyst_id: d.analyst_id,
          game_id: d.game_id,
          player_id: d.player_id || null,
          team_id: d.team_id || null,
          odds: d.odds ? Number(d.odds) : null,
          bookmaker: d.bookmaker || null,
          evidence: d.evidence,
          notes: d.notes,
          synthetic,
          created_at: d.created_at
            ? new Date(d.created_at).toISOString()
            : null,
          market: {
            kind,
            direction:
              kind === "moneyline"
                ? "win"
                : kind === "spread"
                  ? "over"
                  : d.direction,
            threshold: kind === "moneyline" ? 0 : Number(d.threshold),
            includes_overtime: d.overtime === "yes",
            dnp: d.dnp,
            postponed: d.postponed,
            rule_reference: d.rule_reference,
          },
        };
        const response = await api("predictions", body);
        await done();
        return response;
      }}
    >
      <p className="muted">
        Locks immediately. Original inputs and timestamps are preserved. Record
        a new entry to document a correction.
      </p>
      <Field label="Analyst">
        <Select rows={analysts} name="analyst_id" />
      </Field>
      <Field label="Fixture">
        <Select
          rows={games.map((g) => ({
            ...g,
            label: `${g.away_name} at ${g.home_name} · ${ukTime(g.start_utc)}`,
          }))}
          name="game_id"
        />
      </Field>
      <Field label="Market">
        <select value={kind} onChange={(e) => setKind(e.target.value)}>
          {kinds.map((k) => (
            <option key={k} value={k}>
              {k.replaceAll("_", " + ")}
            </option>
          ))}
        </select>
      </Field>
      {playerMarket && (
        <Field label="Player">
          <Select rows={players} name="player_id" />
        </Field>
      )}
      {["moneyline", "spread", "team_total"].includes(kind) && (
        <Field label="Selected team">
          <Select rows={teams} name="team_id" />
        </Field>
      )}
      {!["moneyline", "spread"].includes(kind) && (
        <Field label="Direction">
          <select name="direction">
            <option value="over">Over</option>
            <option value="under">Under</option>
            <option value="at_least">At least (integer alternative)</option>
          </select>
        </Field>
      )}
      {kind !== "moneyline" && (
        <Field
          label={
            kind === "spread"
              ? "Selected-team handicap (e.g. -4.5)"
              : "Threshold"
          }
        >
          <input name="threshold" type="number" step="0.5" required />
        </Field>
      )}
      <Field label="Recorded decimal odds (optional)">
        <input name="odds" type="number" step="0.001" min="1.001" />
      </Field>
      <Field label="Bookmaker / price source (optional)">
        <input name="bookmaker" />
      </Field>
      <Field label="Original prediction timestamp (optional; browser local time)">
        <input name="created_at" type="datetime-local" />
      </Field>
      <Field label="Overtime rule">
        <select name="overtime" required>
          <option value="">Confirm rule…</option>
          <option value="yes">Includes overtime</option>
          <option value="no">Regulation only</option>
        </select>
      </Field>
      <Field label="Did not play rule">
        <select name="dnp">
          <option value="void">Void</option>
          <option value="action">
            Action — supply an explicitly verified result
          </option>
        </select>
      </Field>
      <Field label="Postponed rule">
        <select name="postponed">
          <option value="pending">Keep pending</option>
          <option value="void">Void</option>
        </select>
      </Field>
      <Field label="Verified market rule reference">
        <input name="rule_reference" required minLength={3} />
      </Field>
      <Field label="Evidence source">
        <input name="evidence" required minLength={3} />
      </Field>
      <Field label="Research notes">
        <textarea name="notes" />
      </Field>
    </Form>
  );
}

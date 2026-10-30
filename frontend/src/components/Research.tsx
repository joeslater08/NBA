import { api, type RecordData } from "../api";
import { Form, Field, Select } from "./Forms";
export default function Research({
  teams,
  games,
  synthetic,
  done,
}: {
  teams: RecordData[];
  games: RecordData[];
  synthetic: boolean;
  done: () => Promise<void>;
}) {
  return (
    <div className="form-grid">
      <Form
        title="Add team"
        submit={async (d) => {
          await api("teams", { ...d, synthetic });
          await done();
        }}
      >
        <Field label="Official name">
          <input name="name" required />
        </Field>
        <Field label="Abbreviation">
          <input name="abbreviation" required minLength={2} maxLength={8} />
        </Field>
      </Form>
      <Form
        title="Add player"
        submit={async (d) => {
          await api("players", {
            ...d,
            assignment_start: d.assignment_start
              ? new Date(d.assignment_start).toISOString()
              : null,
            synthetic,
          });
          await done();
        }}
      >
        <Field label="Official name">
          <input name="name" required />
        </Field>
        <Field label="Team">
          <Select rows={teams} name="team_id" />
        </Field>
        <Field label="Position">
          <input name="position" />
        </Field>
        <Field label="Team assignment effective from (optional; browser local time)">
          <input name="assignment_start" type="datetime-local" />
        </Field>
        <p className="muted">
          Leave blank to start the assignment now. Only enter a historical date
          if verified.
        </p>
      </Form>
      <Form
        title="Add fixture"
        submit={async (d) => {
          await api("games", {
            ...d,
            start_utc: new Date(d.start_utc).toISOString(),
            synthetic,
          });
          await done();
        }}
      >
        <Field label="Season">
          <input name="season" placeholder="2026-27" required />
        </Field>
        <Field label="Start (browser local time; displayed in UK time)">
          <input name="start_utc" type="datetime-local" required />
        </Field>
        <Field label="Home team">
          <Select rows={teams} name="home_team_id" />
        </Field>
        <Field label="Away team">
          <Select rows={teams} name="away_team_id" />
        </Field>
        <Field label="Fixture source">
          <input name="source" required minLength={3} />
        </Field>
      </Form>
      <Form
        title="Record fixture result / status"
        submit={async (d) => {
          await api(`games/${d.game_id}/result`, {
            status: d.status,
            home_score: d.home_score === "" ? null : Number(d.home_score),
            away_score: d.away_score === "" ? null : Number(d.away_score),
            evidence: d.evidence,
          });
          await done();
        }}
      >
        <Field label="Fixture">
          <Select
            rows={games.map((g) => ({
              ...g,
              label: `${g.away_name} at ${g.home_name}`,
            }))}
            name="game_id"
          />
        </Field>
        <Field label="Status">
          <select name="status">
            <option value="completed">Completed</option>
            <option value="live">Live</option>
            <option value="postponed">Postponed</option>
            <option value="cancelled">Cancelled</option>
            <option value="scheduled">Scheduled</option>
          </select>
        </Field>
        <Field label="Home score">
          <input name="home_score" type="number" min="0" />
        </Field>
        <Field label="Away score">
          <input name="away_score" type="number" min="0" />
        </Field>
        <Field label="Source evidence">
          <input name="evidence" required minLength={3} />
        </Field>
        <p className="muted">
          Final results are preserved. Selection grading is recorded separately
          in Results review.
        </p>
      </Form>
    </div>
  );
}

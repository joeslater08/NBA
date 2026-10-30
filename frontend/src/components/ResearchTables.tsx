import { number, ukTime, type RecordData } from "../api";

export function Metric({
  title,
  value,
  note,
}: {
  title: string;
  value: string | number;
  note: string;
}) {
  return (
    <section className="metric">
      <p>{title}</p>
      <strong>{value}</strong>
      <small>{note}</small>
    </section>
  );
}
export function Status({
  title,
  detail,
  state,
}: {
  title: string;
  detail: string;
  state: string;
}) {
  return (
    <div className="status-row">
      <div>
        <strong>{title}</strong>
        <small>{detail}</small>
      </div>
      <span className="tag">{state}</span>
    </div>
  );
}
export function GameList({ games }: { games: RecordData[] }) {
  return games.length ? (
    <div>
      {games.map((g) => (
        <div className="game" key={g.id}>
          <div>
            <small>
              {ukTime(g.start_utc)} · {g.season}
            </small>
            <h3>
              {g.away_name}
              <span className="versus"> at </span>
              {g.home_name}
            </h3>
            <small>Source: {g.source}</small>
          </div>
          <span className="badge">{g.status}</span>
        </div>
      ))}
    </div>
  ) : (
    <p className="empty">
      No fixtures stored. Add a verified fixture in Games & players.
    </p>
  );
}
export function PredictionTable({ rows }: { rows: RecordData[] }) {
  return rows.length ? (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Selection / identifier</th>
            <th>Original / lock times</th>
            <th>Odds</th>
            <th>Outcome</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((p) => (
            <tr key={p.id}>
              <td>
                {p.name}
                <small className="id">{p.id}</small>
              </td>
              <td>
                {ukTime(p.created_at)}
                <small className="id">Locked {ukTime(p.locked_at)}</small>
                {new Date(p.locked_at) >= new Date(p.game_start_at) && (
                  <small className="id">Entered after fixture start</small>
                )}
              </td>
              <td>{number(p.odds)}</td>
              <td>
                <span className={`badge ${p.outcome}`}>{p.outcome}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <p className="empty">
      No predictions recorded. Enter a selection with source evidence to begin.
    </p>
  );
}

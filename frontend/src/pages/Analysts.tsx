import { number, type RecordData } from "../api";
import { AnalystForm } from "../components/Forms";
export default function Analysts({
  analysts,
  done: load,
}: {
  analysts: RecordData[];
  done: () => Promise<void>;
}) {
  return (
    <>
      <section className="panel">
        <h2>Observed analyst records</h2>
        <p className="muted">
          Unique singles only. Repeated parlay legs do not increase prediction
          counts. No ranking implies proven skill.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Analyst</th>
                <th>Selections</th>
                <th>W / L / P / V</th>
                <th>Hit rate</th>
                <th>Average odds</th>
              </tr>
            </thead>
            <tbody>
              {analysts.map((a) => (
                <tr key={a.id}>
                  <td>{a.name}</td>
                  <td>{a.predictions}</td>
                  <td>
                    {a.win} / {a.loss} / {a.push} / {a.void}
                  </td>
                  <td>
                    {a.hit_rate == null
                      ? "No decisive results"
                      : number(a.hit_rate * 100, "%")}
                  </td>
                  <td>{number(a.average_odds)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <AnalystForm done={load} />
    </>
  );
}

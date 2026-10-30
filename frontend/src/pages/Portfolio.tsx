import { number, type RecordData } from "../api";
import Settlement from "../components/Settlement";
export default function Portfolio({
  data,
  predictions,
  analysts,
  done: load,
}: {
  data: RecordData;
  predictions: RecordData[];
  analysts: RecordData[];
  done: () => Promise<void>;
}) {
  return (
    <>
      <section className="panel">
        <h2>Virtual paper ledger</h2>
        <p>1 unit = £1 nominal. Missing prices leave total ROI unavailable.</p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Entry</th>
                <th>Units</th>
                <th>Recorded odds</th>
                <th>Outcome</th>
                <th>Virtual P/L</th>
              </tr>
            </thead>
            <tbody>
              {(data["paper-entries"] || []).map((e: RecordData) => (
                <tr key={e.id}>
                  <td>{e.id.slice(0, 8)}</td>
                  <td>{e.units}</td>
                  <td>{number(e.recorded_odds)}</td>
                  <td>
                    <span className={`badge ${e.outcome}`}>{e.outcome}</span>
                  </td>
                  <td>{number(e.profit_loss, " u")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <section className="panel">
        <h2>Parlays</h2>
        {(data.parlays || []).map((p: RecordData) => (
          <p key={p.id}>
            {p.id.slice(0, 8)} · {p.prediction_ids.length} legs · {p.outcome} ·
            joint probability unavailable
          </p>
        ))}
        {!data.parlays?.length && <p>No recorded parlays.</p>}
      </section>
      <Settlement
        predictions={predictions}
        parlays={data.parlays || []}
        analysts={analysts}
        done={load}
      />
    </>
  );
}

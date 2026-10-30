import { number, type RecordData } from "../api";
import {
  Metric,
  Status,
  GameList,
  PredictionTable,
} from "../components/ResearchTables";
export default function Dashboard({
  summary,
  games,
  synthetic,
  predictions,
}: {
  summary: RecordData;
  games: RecordData[];
  synthetic: boolean;
  predictions: RecordData[];
}) {
  const portfolio = summary?.portfolio;
  return (
    <>
      <div className="metrics">
        <Metric
          title="Fixtures stored"
          value={summary?.games ?? 0}
          note="Selected dataset"
        />
        <Metric
          title="Locked predictions"
          value={summary?.predictions ?? 0}
          note={`${summary?.awaiting_grading ?? 0} awaiting grading`}
        />
        <Metric
          title="Virtual net P/L"
          value={number(portfolio?.net_profit_loss, " u")}
          note="Paper units · not real returns"
        />
        <Metric
          title="Paper ROI"
          value={
            portfolio?.roi == null
              ? "Unavailable"
              : number(portfolio.roi * 100, "%")
          }
          note={`${portfolio?.settled_entries ?? 0} settled entries`}
        />
      </div>
      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-heading">
            <h2>Fixture research</h2>
            <span className="tag">UK TIME</span>
          </div>
          <GameList games={games} />
        </section>
        <section className="panel">
          <h2>Research status</h2>
          <Status
            title="Data source"
            detail={
              synthetic ? "Synthetic, manually seeded" : "Manual entry and CSV"
            }
            state="Review"
          />
          <Status
            title="Forecast model"
            detail="Planned for version 0.3"
            state="Unavailable"
          />
          <Status
            title="Simulation engine"
            detail="No simulations have been run"
            state="Planned"
          />
          <Status
            title="Data freshness"
            detail="No automatic provider sync"
            state="Manual"
          />
        </section>
      </div>
      <section className="panel">
        <h2>Latest locked selections</h2>
        <PredictionTable rows={predictions.slice(-5).reverse()} />
      </section>
    </>
  );
}

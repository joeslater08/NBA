import { GameList, PredictionTable } from "./components/ResearchTables";
import Learning from "./pages/Learning";
import Portfolio from "./pages/Portfolio";
import Analysts from "./pages/Analysts";
import Dashboard from "./pages/Dashboard";
import { useCallback, useEffect, useRef, useState } from "react";
import { api, type RecordData } from "./api";
import PredictionForm from "./components/PredictionForm";
import Research from "./components/Research";
import DataCentre from "./components/DataCentre";
const tabs = [
  "Dashboard",
  "Games & players",
  "Predictions",
  "Analysts",
  "Paper portfolio",
  "Results review",
  "Data centre",
  "Learning centre",
];
export default function App() {
  const [tab, setTab] = useState("Dashboard");
  const [synthetic, setSynthetic] = useState(true);
  const [data, setData] = useState<RecordData>({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const requestId = useRef(0);
  const load = useCallback(async () => {
    const currentRequest = ++requestId.current;
    setError("");
    try {
      const names = [
        "teams",
        "players",
        "games",
        "predictions",
        "parlays",
        "paper-entries",
        "nba/summary",
        "nba/analysts",
      ];
      const values = await Promise.all(
        names.map((n) => api(`${n}?synthetic=${synthetic}`)),
      );
      if (currentRequest !== requestId.current) return;
      setData(Object.fromEntries(names.map((n, i) => [n, values[i]])));
    } catch (e) {
      if (currentRequest !== requestId.current) return;
      setError(e instanceof Error ? e.message : "Unable to load data");
    } finally {
      if (currentRequest === requestId.current) setLoading(false);
    }
  }, [synthetic]);
  useEffect(() => {
    setLoading(true);
    setData({});
    void load();
  }, [load]);
  const teams: RecordData[] = data.teams || [],
    players: RecordData[] = data.players || [],
    analysts: RecordData[] = data["nba/analysts"] || [];
  const teamName = (id: string) =>
    teams.find((t) => t.id === id)?.name || "Unknown team";
  const games: RecordData[] = (data.games || []).map((g: RecordData) => ({
    ...g,
    home_name: teamName(g.home_team_id),
    away_name: teamName(g.away_team_id),
  }));
  const predictions: RecordData[] = (data.predictions || []).map(
    (p: RecordData) => ({
      ...p,
      name: `${players.find((x) => x.id === p.player_id)?.name || teams.find((t) => t.id === p.team_id)?.name || "Game"} · ${p.market.kind.replaceAll("_", " + ")} ${p.market.direction} ${p.market.threshold}`,
    }),
  );
  const summary = data["nba/summary"],
    portfolio = summary?.portfolio;
  return (
    <div className="shell">
      <aside>
        <a className="brand" href="#main">
          <span className="brand-icon">N</span>
          <span>
            NBA INTELLIGENCE<small>RESEARCH LAB / 0.1</small>
          </span>
        </a>
        <p className="nav-label">WORKSPACE</p>
        <nav aria-label="Main navigation">
          {tabs.map((t, i) => (
            <button
              className={tab === t ? "active" : ""}
              key={t}
              onClick={() => setTab(t)}
            >
              <span aria-hidden="true">
                {["◫", "◷", "≡", "◉", "▥", "✓", "⇄", "⌘"][i]}
              </span>
              {t}
            </button>
          ))}
        </nav>
        <div className="aside-note">
          <span className="dot" />
          Local research environment
          <p>
            Paper testing only
            <br />
            No real-money functionality
          </p>
        </div>
      </aside>
      <main id="main">
        <header>
          <div>
            <p className="eyebrow">NBA INTELLIGENCE LAB</p>
            <h1>{tab === "Dashboard" ? "Daily command centre" : tab}</h1>
            <p className="muted">
              Every prediction is an experiment. Every result is evidence.
            </p>
          </div>
          <label className="mode">
            Dataset
            <select
              value={synthetic ? "demo" : "real"}
              onChange={(e) => setSynthetic(e.target.value === "demo")}
            >
              <option value="demo">Synthetic demonstration</option>
              <option value="real">Real manual records</option>
            </select>
          </label>
        </header>
        <div className="notice">
          <strong>
            {synthetic ? "DEMONSTRATION DATA" : "MANUAL RESEARCH DATA"}
          </strong>
          <span>
            {synthetic
              ? "Fictional teams, players and fixtures. Excluded from real performance."
              : "No live provider connected. Check source evidence before relying on records."}
          </span>
        </div>
        {error && (
          <div role="alert" className="error">
            {error}
            <button onClick={() => void load()}>Retry</button>
          </div>
        )}
        {loading || summary?.synthetic !== synthetic ? (
          <p role="status">Loading workspace…</p>
        ) : (
          <>
            {tab === "Dashboard" && (
              <Dashboard
                summary={summary}
                games={games}
                synthetic={synthetic}
                predictions={predictions}
              />
            )}
            {tab === "Games & players" && (
              <>
                <section className="panel">
                  <h2>Stored fixtures</h2>
                  <GameList games={games} />
                </section>
                <Research
                  teams={teams}
                  games={games}
                  synthetic={synthetic}
                  done={load}
                />
                <section className="panel">
                  <h2>Player records</h2>
                  {players.length ? (
                    players.map((p) => (
                      <p key={p.id}>
                        {p.name} · {teamName(p.team_id)} ·{" "}
                        {p.position || "Position unknown"}
                      </p>
                    ))
                  ) : (
                    <p>No player records.</p>
                  )}
                </section>
              </>
            )}
            {tab === "Predictions" && (
              <>
                <section className="panel">
                  <h2>Prediction ledger</h2>
                  <PredictionTable rows={predictions} />
                </section>
                <PredictionForm
                  games={games}
                  players={players}
                  teams={teams}
                  analysts={analysts}
                  synthetic={synthetic}
                  done={load}
                />
              </>
            )}
            {tab === "Analysts" && <Analysts analysts={analysts} done={load} />}
            {["Paper portfolio", "Results review"].includes(tab) && (
              <Portfolio
                data={data}
                predictions={predictions}
                analysts={analysts}
                done={load}
              />
            )}
            {tab === "Data centre" && (
              <DataCentre synthetic={synthetic} done={load} />
            )}
            {tab === "Learning centre" && <Learning />}
          </>
        )}
        <footer>
          NBA Intelligence Lab · Version 0.1 · UTC storage / Europe–London
          display · Independent research & paper testing
        </footer>
      </main>
    </div>
  );
}

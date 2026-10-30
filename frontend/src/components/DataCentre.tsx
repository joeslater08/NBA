import { useState } from "react";
import { api } from "../api";
import { Field, Form } from "./Forms";
export default function DataCentre({
  synthetic,
  done,
}: {
  synthetic: boolean;
  done: () => Promise<void>;
}) {
  const [report, setReport] = useState<unknown>(null);
  return (
    <>
      <div className="notice">
        Manual sources only. No live feed, automatic refresh or completed
        simulations are connected.
      </div>
      <Form
        title="Import manual CSV"
        label="Validate / import"
        submit={async (d) => {
          const result = await api(`import/${d.resource}`, {
            content: d.content,
            source: d.source,
            synthetic,
            confirm: d.confirm === "yes",
          });
          setReport(result);
          if (result.committed) await done();
          return {
            message: result.committed
              ? "Import saved successfully"
              : result.errors.length
                ? "Validation failed; no records saved"
                : "Preview complete; no records saved",
            preserve: !result.committed,
          };
        }}
      >
        <Field label="Record type">
          <select name="resource">
            <option value="teams">Teams</option>
            <option value="players">Players</option>
            <option value="games">Fixtures</option>
            <option value="predictions">Predictions</option>
          </select>
        </Field>
        <Field label="CSV content (see README for columns)">
          <textarea
            name="content"
            required
            placeholder={"name,abbreviation\nExample Team,EXT"}
          />
        </Field>
        <Field label="Source reference">
          <input name="source" required minLength={3} />
        </Field>
        <Field label="Action">
          <select name="confirm">
            <option value="no">Preview only</option>
            <option value="yes">Validate and import all rows</option>
          </select>
        </Field>
      </Form>
      {report !== null && (
        <pre className="panel">{JSON.stringify(report, null, 2)}</pre>
      )}
      <section className="panel">
        <h2>CSV exports</h2>
        <div className="exports">
          {[
            "teams",
            "players",
            "games",
            "predictions",
            "paper-entries",
            "analysts",
          ].map((r) => (
            <a key={r} href={`/api/v1/export/${r}?synthetic=${synthetic}`}>
              {r}
            </a>
          ))}
        </div>
        <p>
          Import teams first, then players and fixtures, then predictions using
          the stored identifiers. Preview validates database links without
          saving records. Exports are audit extracts; remove generated fields
          before re-importing.
        </p>
      </section>
    </>
  );
}

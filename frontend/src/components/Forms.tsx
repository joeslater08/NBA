import {
  cloneElement,
  isValidElement,
  useId,
  useState,
  type ReactElement,
  type FormEvent,
  type ReactNode,
} from "react";
import { api, type RecordData } from "../api";
export function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  const id = useId();
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {isValidElement(children)
        ? cloneElement(children as ReactElement<{ id?: string }>, { id })
        : children}
    </div>
  );
}
export function Select({
  rows,
  name,
  empty = "Select…",
  id,
}: {
  rows: RecordData[];
  name: string;
  empty?: string;
  id?: string;
}) {
  return (
    <select id={id} name={name} required>
      <option value="">{empty}</option>
      {rows.map((r) => (
        <option key={r.id} value={r.id}>
          {r.name || r.label || r.id}
        </option>
      ))}
    </select>
  );
}
export function Form({
  title,
  children,
  submit,
  label = "Save",
}: {
  title: string;
  children: ReactNode;
  submit: (d: Record<string, string>) => Promise<unknown>;
  label?: string;
}) {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  async function send(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    setBusy(true);
    setMessage("");
    try {
      const result = await submit(
        Object.fromEntries(new FormData(form)) as Record<string, string>,
      );
      const feedback =
        result && typeof result === "object"
          ? (result as {
              message?: string;
              warnings?: string[];
              preserve?: boolean;
            })
          : undefined;
      setMessage(
        [
          feedback?.message || "Saved successfully",
          ...(feedback?.warnings || []),
        ].join(" · "),
      );
      if (!feedback?.preserve) form.reset();
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Unable to save");
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel">
      <h2>{title}</h2>
      <form onSubmit={send}>
        {children}
        <button disabled={busy}>{busy ? "Saving…" : label}</button>
        <p role="status">{message}</p>
      </form>
    </section>
  );
}
export function AnalystForm({ done }: { done: () => Promise<void> }) {
  return (
    <Form
      title="Add analyst"
      submit={async (d) => {
        await api("analysts", d);
        await done();
      }}
    >
      <Field label="Display name">
        <input name="name" required maxLength={120} />
      </Field>
      <Field label="Platform">
        <input name="platform" />
      </Field>
      <Field label="Source / profile URL">
        <input name="profile_url" type="url" />
      </Field>
      <Field label="Notes">
        <textarea name="notes" />
      </Field>
    </Form>
  );
}

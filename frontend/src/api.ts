export type RecordData = Record<string, any>;
export async function api(path: string, body?: unknown): Promise<any> {
  const res = await fetch(
    "/api/v1/" + path,
    body === undefined
      ? undefined
      : {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
  );
  const data = await res.json();
  if (!res.ok)
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : JSON.stringify(data.detail),
    );
  return data;
}
export function ukTime(value: string): string {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Europe/London",
  }).format(new Date(value));
}
export function number(value: number | null | undefined, suffix = ""): string {
  return value === null || value === undefined
    ? "Unavailable"
    : value.toFixed(2) + suffix;
}

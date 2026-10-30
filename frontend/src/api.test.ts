import { describe, it, expect } from "vitest";
import { ukTime, number } from "./api";
describe("transparent display", () => {
  it("does not invent missing prices", () =>
    expect(number(null)).toBe("Unavailable"));
  it("keeps zero visible", () => expect(number(0)).toBe("0.00"));
  it("uses British summer time", () =>
    expect(ukTime("2026-07-01T20:00:00Z")).toContain("21:00"));
  it("uses GMT in winter", () =>
    expect(ukTime("2026-12-01T20:00:00Z")).toContain("20:00"));
});

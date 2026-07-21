import { describe, expect, test } from "vitest";
import { apiError, results } from "./api";

describe("API helpers", () => {
  test("normalizes paginated results", () => {
    expect(results({ results: [{ id: 1 }] })).toEqual([{ id: 1 }]);
  });
  test("extracts validation messages", () => {
    expect(apiError({ response: { data: { errors: { quantity: ["Insufficient stock."] } } } })).toBe("Insufficient stock.");
  });
});

import { describe, expect, it } from "vitest";
import { decodePixels, shadeTable } from "./shade";

describe("shadeTable", () => {
  it("is black at level 0", () => {
    expect(shadeTable(0)[255]).toBe(0);
  });

  it("is full at level 255", () => {
    expect(shadeTable(255)[255]).toBe(255);
  });

  it("copies the hardware's truncation: a dim channel vanishes at a low level", () => {
    const table = shadeTable(2);
    expect(table[80]).toBe(0);
    expect(table[255]).toBeGreaterThan(0);
  });

  it("is monotonic in channel value and level", () => {
    const quarter = shadeTable(64);
    for (let value = 1; value < 256; value++) expect(quarter[value]).toBeGreaterThanOrEqual(quarter[value - 1]);
    expect(shadeTable(128)[200]).toBeGreaterThan(quarter[200]);
  });

  it("shows a dim strip as visible, as an eye would see it", () => {
    expect(shadeTable(45)[255]).toBeGreaterThan(90);
  });
});

it("decodePixels returns raw bytes", () => {
  expect([...decodePixels("/wAQ")]).toEqual([255, 0, 16]);
});

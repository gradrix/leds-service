import { describe, expect, it } from "vitest";
import { layoutStrip, StripView } from "./layout";

const COUNT = 360;
const SIZES: Array<[string, number, number]> = [
  ["phone", 374, 280],
  ["small phone", 328, 230],
  ["tablet", 768, 420],
  ["desktop", 1300, 760],
  ["taller than wide", 560, 646],
  ["narrow and tall", 300, 1000],
  ["landscape phone", 480, 280],
];
const VIEWS: StripView[] = ["snake", "room"];

describe.each(VIEWS)("%s view", (view) => {
  it.each(SIZES)("keeps all 360 LEDs on a %s canvas", (_, width, height) => {
    const { points } = layoutStrip(view, width, height, COUNT);
    expect(points).toHaveLength(COUNT);
    for (const { x, y } of points) {
      expect(x).toBeGreaterThanOrEqual(0);
      expect(x).toBeLessThanOrEqual(width);
      expect(y).toBeGreaterThanOrEqual(0);
      expect(y).toBeLessThanOrEqual(height);
    }
  });

  it.each(SIZES)("spaces neighbours evenly along the strip on a %s canvas", (_, width, height) => {
    const { points, pitch } = layoutStrip(view, width, height, COUNT);
    for (let i = 1; i < COUNT; i++) {
      const gap = Math.hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y);
      expect(gap).toBeLessThanOrEqual(pitch * 1.001);
      expect(gap).toBeGreaterThan(pitch * 0.6);
    }
  });

  it.each(SIZES)("never puts LEDs on top of each other on a %s canvas", (_, width, height) => {
    const { points, pitch } = layoutStrip(view, width, height, COUNT);
    for (let a = 0; a < COUNT; a++) {
      for (let b = a + 2; b < COUNT; b++) {
        const distance = Math.hypot(points[a].x - points[b].x, points[a].y - points[b].y);
        expect(distance).toBeGreaterThan(pitch * 0.9);
      }
    }
  });
});

it.each(SIZES)("snake LEDs stay big enough to see on a %s canvas", (_, width, height) => {
  expect(layoutStrip("snake", width, height, COUNT).pitch).toBeGreaterThan(7);
});

it("snake runs back and forth", () => {
  const { points } = layoutStrip("snake", 1300, 760, COUNT);
  const rows = new Set(points.map((p) => Math.round(p.y)));
  expect(rows.size).toBeGreaterThan(5);
  expect(points[0].y).toBeLessThan(points[COUNT - 1].y);
});

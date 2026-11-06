import { describe, expect, it } from "vitest";
import { hexToHueSat, hueSatToHex, inkFor, SWATCHES } from "./color";

it.each([
  ["ff0000", 0, 100],
  ["00ff00", 120, 100],
  ["0000ff", 240, 100],
  ["ffffff", 0, 0],
])("%s", (hex, hue, saturation) => {
  expect(hexToHueSat(hex)).toEqual({ hue, saturation });
  expect(hueSatToHex({ hue, saturation })).toBe(hex);
});

it.each([
  ["1f5cff", "#ffffff"],
  ["8a2bff", "#ffffff"],
  ["ffb454", "#101114"],
  ["ffffff", "#101114"],
  ["00d5ff", "#101114"],
])("text on %s is %s", (hex, ink) => {
  expect(inkFor(hex)).toBe(ink);
});

describe("swatches", () => {
  // A strip shows each channel at its linear value, so a stray channel that a screen hides stays visible.
  it.each([
    ["Red", 0],
    ["Green", 1],
    ["Blue", 2],
  ])("%s lights only its own LED", (name, channel) => {
    const hex = SWATCHES.find(([swatch]) => swatch === name)![1];
    const bytes = [0, 2, 4].map((start) => parseInt(hex.slice(start, start + 2), 16));
    expect(bytes).toEqual([0, 1, 2].map((i) => (i === channel ? 255 : 0)));
  });
});

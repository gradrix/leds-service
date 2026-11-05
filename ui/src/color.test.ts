import { expect, it } from "vitest";
import { hexToHueSat, hueSatToHex, inkFor } from "./color";

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

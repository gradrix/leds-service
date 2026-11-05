const DARK_INK = "#101114";
const LIGHT_INK = "#ffffff";
const DARK_INK_LUMINANCE = 0.0056;

function linear(channel: number): number {
  const value = channel / 255;
  return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
}

/** The text colour with the better contrast on a colour (WCAG relative luminance). */
export function inkFor(hex: string): string {
  const n = parseInt(hex, 16);
  const luminance = 0.2126 * linear(n >> 16) + 0.7152 * linear((n >> 8) & 255) + 0.0722 * linear(n & 255);
  const onLight = (luminance + 0.05) / (DARK_INK_LUMINANCE + 0.05);
  const onDark = 1.05 / (luminance + 0.05);
  return onLight >= onDark ? DARK_INK : LIGHT_INK;
}

export interface HueSat {
  hue: number;
  saturation: number;
}

export function hexToHueSat(hex: string): HueSat {
  const n = parseInt(hex, 16);
  const r = ((n >> 16) & 255) / 255;
  const g = ((n >> 8) & 255) / 255;
  const b = (n & 255) / 255;
  const max = Math.max(r, g, b);
  const delta = max - Math.min(r, g, b);
  let hue = 0;
  if (delta > 0) {
    if (max === r) hue = ((g - b) / delta + 6) % 6;
    else if (max === g) hue = (b - r) / delta + 2;
    else hue = (r - g) / delta + 4;
  }
  return { hue: Math.round(hue * 60), saturation: max === 0 ? 0 : Math.round((delta / max) * 100) };
}

/** Full-value colour: how bright it is belongs to the brightness slider. */
export function hueSatToHex({ hue, saturation }: HueSat): string {
  const s = saturation / 100;
  const channel = (n: number) => {
    const k = (n + hue / 60) % 6;
    const v = 1 - s * Math.max(0, Math.min(k, 4 - k, 1));
    return Math.round(v * 255)
      .toString(16)
      .padStart(2, "0");
  };
  return channel(5) + channel(3) + channel(1);
}

const DISPLAY_GAMMA = 2.2;

/**
 * Table from a pixel channel (0-255) to the value to paint on screen at a strip level.
 *
 * Follows the hardware: rpi_ws281x scales each channel with (value * (level + 1)) >> 8, truncating,
 * so very dim colours lose channels on the strip and do here too. LED output is linear
 * light and a screen expects gamma-encoded values, hence the final curve.
 */
export function shadeTable(level: number): Uint8Array {
  const scale = level === 0 ? 0 : level + 1;
  const table = new Uint8Array(256);
  for (let value = 0; value < 256; value++) {
    const emitted = (value * scale) >> 8;
    table[value] = Math.round(255 * (emitted / 255) ** (1 / DISPLAY_GAMMA));
  }
  return table;
}

export function decodePixels(base64: string): Uint8Array {
  const text = atob(base64);
  const pixels = new Uint8Array(text.length);
  for (let i = 0; i < text.length; i++) pixels[i] = text.charCodeAt(i);
  return pixels;
}

export interface Point {
  x: number;
  y: number;
}

export interface StripLayout {
  points: Point[];
  /** The strip's centre line, sampled finely enough to draw smooth curves. */
  trail: Point[];
  /** Distance between neighbouring LEDs in CSS pixels. */
  pitch: number;
}

export type StripView = "snake" | "room";

const PADDING = 22;
/** Rows of the snake stay at least this many LED pitches apart so they read as one strip. */
const MIN_ROW_GAP_PITCHES = 2.2;
const TRAIL_SAMPLES_PER_LED = 4;

export function layoutStrip(view: StripView, width: number, height: number, count: number): StripLayout {
  return view === "snake" ? snake(width, height, count) : room(width, height, count);
}

/** Walks a path of straights and arcs, placing `count` points at equal distance. */
function place(walk: (distance: number) => Point, length: number, count: number): StripLayout {
  const pitch = length / (count - 1);
  const points = Array.from({ length: count }, (_, i) => walk(i * pitch));
  const samples = (count - 1) * TRAIL_SAMPLES_PER_LED + 1;
  const trail = Array.from({ length: samples }, (_, i) => walk((i * pitch) / TRAIL_SAMPLES_PER_LED));
  return { points, trail, pitch };
}

function snakeShape(width: number, height: number, rows: number, count: number) {
  const gap = (height - 2 * PADDING) / (rows - 1);
  const straight = width - 2 * PADDING - gap;
  const turn = (Math.PI * gap) / 2;
  const length = rows * straight + (rows - 1) * turn;
  return { gap, straight, turn, length, pitch: length / (count - 1) };
}

function chooseRows(width: number, height: number, count: number): number {
  let best = 2;
  for (let rows = 2; rows <= 60; rows++) {
    const shape = snakeShape(width, height, rows, count);
    // Taller than wide: too few rows leave no straight at all, more rows may still fit.
    if (shape.straight <= 0) continue;
    if (shape.gap >= MIN_ROW_GAP_PITCHES * shape.pitch) best = rows;
  }
  return best;
}

function snake(width: number, height: number, count: number): StripLayout {
  const rows = chooseRows(width, height, count);
  const { gap, straight, turn, length } = snakeShape(width, height, rows, count);
  const left = PADDING + gap / 2;
  const walk = (distance: number): Point => {
    const span = straight + turn;
    const row = Math.min(rows - 1, Math.floor(distance / span));
    const along = distance - row * span;
    const y = PADDING + row * gap;
    const forward = row % 2 === 0;
    if (along <= straight || row === rows - 1) {
      return { x: forward ? left + along : left + straight - along, y };
    }
    // U-turn into the next row, on the side this row ended.
    const angle = ((along - straight) / turn) * Math.PI;
    const radius = gap / 2;
    const reach = Math.sin(angle) * radius;
    return {
      x: forward ? left + straight + reach : left - reach,
      y: y + radius - Math.cos(angle) * radius,
    };
  };
  return place(walk, length, count);
}

/** The strip as a loop round the walls, seen from above. */
function room(width: number, height: number, count: number): StripLayout {
  const w = width - 2 * PADDING;
  const h = height - 2 * PADDING;
  const radius = Math.min(w, h) * 0.12;
  const sideX = w - 2 * radius;
  const sideY = h - 2 * radius;
  const corner = (Math.PI * radius) / 2;
  const perimeter = 2 * sideX + 2 * sideY + 4 * corner;
  // Ends stop short of each other: it is one strip, not a closed ring.
  const length = perimeter * 0.985;
  const sections: Array<[number, (d: number) => Point]> = [
    [sideX, (d) => ({ x: PADDING + radius + d, y: PADDING })],
    [corner, (d) => arc(PADDING + w - radius, PADDING + radius, radius, -90, d / corner)],
    [sideY, (d) => ({ x: PADDING + w, y: PADDING + radius + d })],
    [corner, (d) => arc(PADDING + w - radius, PADDING + h - radius, radius, 0, d / corner)],
    [sideX, (d) => ({ x: PADDING + w - radius - d, y: PADDING + h })],
    [corner, (d) => arc(PADDING + radius, PADDING + h - radius, radius, 90, d / corner)],
    [sideY, (d) => ({ x: PADDING, y: PADDING + h - radius - d })],
    [corner, (d) => arc(PADDING + radius, PADDING + radius, radius, 180, d / corner)],
  ];
  const walk = (distance: number): Point => {
    let left = distance;
    for (const [size, at] of sections) {
      if (left <= size) return at(left);
      left -= size;
    }
    return sections[0][1](0);
  };
  return place(walk, length, count);
}

function arc(cx: number, cy: number, radius: number, startDegrees: number, fraction: number): Point {
  const angle = ((startDegrees + fraction * 90) * Math.PI) / 180;
  return { x: cx + Math.cos(angle) * radius, y: cy + Math.sin(angle) * radius };
}

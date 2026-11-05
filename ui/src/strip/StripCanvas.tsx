import { MutableRefObject, RefObject, useEffect, useRef } from "react";
import { LiveFrame } from "../useLedService";
import { layoutStrip, Point, StripLayout, StripView } from "./layout";
import { shadeTable } from "./shade";

const MAX_PIXEL_RATIO = 2;
const BLOOM_SCALE = 6;
const AMBIENT_EVERY_FRAMES = 6;

/** Where the strip goes inside the canvas; the rest of the canvas is room for the glow. */
interface Area {
  left: number;
  top: number;
  width: number;
  height: number;
}

interface Scene {
  width: number;
  height: number;
  ratio: number;
  layout: StripLayout;
  radius: number;
  tape: HTMLCanvasElement;
  bloom: HTMLCanvasElement;
  haze: HTMLCanvasElement;
}

function canvasOf(width: number, height: number): HTMLCanvasElement {
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.ceil(width));
  canvas.height = Math.max(1, Math.ceil(height));
  return canvas;
}

/** The unlit strip: backing tape plus one dark chip per LED, drawn once per size. */
function buildScene(view: StripView, width: number, height: number, area: Area, count: number): Scene {
  const ratio = Math.min(window.devicePixelRatio || 1, MAX_PIXEL_RATIO);
  const placed = layoutStrip(view, area.width, area.height, count);
  const shift = (p: Point) => ({ x: p.x + area.left, y: p.y + area.top });
  const layout = { ...placed, points: placed.points.map(shift), trail: placed.trail.map(shift) };
  const radius = Math.max(1.3, Math.min(layout.pitch * 0.34, 7));
  const tape = canvasOf(width * ratio, height * ratio);
  const context = tape.getContext("2d")!;
  context.scale(ratio, ratio);
  context.strokeStyle = "#191c23";
  context.lineWidth = radius * 3;
  context.lineCap = "round";
  context.lineJoin = "round";
  context.beginPath();
  layout.trail.forEach((p, i) => (i ? context.lineTo(p.x, p.y) : context.moveTo(p.x, p.y)));
  context.stroke();
  context.fillStyle = "#2b2f38";
  for (const p of layout.points) {
    context.beginPath();
    context.arc(p.x, p.y, radius * 0.8, 0, Math.PI * 2);
    context.fill();
  }
  return {
    width,
    height,
    ratio,
    layout,
    radius,
    tape,
    bloom: canvasOf(width / BLOOM_SCALE, height / BLOOM_SCALE),
    haze: canvasOf(width / (BLOOM_SCALE * 4), height / (BLOOM_SCALE * 4)),
  };
}

function paint(context: CanvasRenderingContext2D, scene: Scene, frame: LiveFrame, shade: Uint8Array): [number, number, number] {
  const { ratio, layout, radius, tape, bloom, haze, width, height } = scene;
  const { pixels } = frame;
  const canvasWidth = context.canvas.width;
  const canvasHeight = context.canvas.height;
  const bloomContext = bloom.getContext("2d")!;
  bloomContext.clearRect(0, 0, bloom.width, bloom.height);

  context.setTransform(1, 0, 0, 1, 0, 0);
  context.globalCompositeOperation = "source-over";
  context.clearRect(0, 0, canvasWidth, canvasHeight);
  context.drawImage(tape, 0, 0);

  const bloomSize = Math.max(1.2, (radius * 2.4) / BLOOM_SCALE);
  let sumR = 0;
  let sumG = 0;
  let sumB = 0;
  const count = Math.min(layout.points.length, pixels.length / 3);
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  for (let i = 0; i < count; i++) {
    const r = shade[pixels[i * 3]];
    const g = shade[pixels[i * 3 + 1]];
    const b = shade[pixels[i * 3 + 2]];
    if (r === 0 && g === 0 && b === 0) continue;
    sumR += r;
    sumG += g;
    sumB += b;
    const { x, y } = layout.points[i];
    const color = `rgb(${r},${g},${b})`;
    context.fillStyle = color;
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.fill();
    bloomContext.fillStyle = color;
    bloomContext.fillRect(x / BLOOM_SCALE - bloomSize / 2, y / BLOOM_SCALE - bloomSize / 2, bloomSize, bloomSize);
  }

  // Scaling a tiny copy up gives a soft glow everywhere; canvas blur filters are missing on iOS.
  const hazeContext = haze.getContext("2d")!;
  hazeContext.clearRect(0, 0, haze.width, haze.height);
  hazeContext.imageSmoothingQuality = "high";
  hazeContext.drawImage(bloom, 0, 0, haze.width, haze.height);

  context.globalCompositeOperation = "lighter";
  context.imageSmoothingQuality = "high";
  context.globalAlpha = 0.85;
  context.drawImage(bloom, 0, 0, width, height);
  context.globalAlpha = 0.6;
  context.drawImage(haze, 0, 0, width, height);
  context.globalAlpha = 1;

  return count ? [sumR / count, sumG / count, sumB / count] : [0, 0, 0];
}

interface Props {
  frameRef: MutableRefObject<LiveFrame | null>;
  /** The element marking the part of the canvas the strip should occupy. */
  areaRef: RefObject<HTMLElement>;
  view: StripView;
  count: number;
  onAmbient: (rgb: [number, number, number]) => void;
}

export function StripCanvas({ frameRef, areaRef, view, count, onAmbient }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const context = canvas.getContext("2d")!;
    let scene: Scene | null = null;
    let drawnSequence = -1;
    let drawnScene: Scene | null = null;
    let drawnLevel = -1;
    let shade = shadeTable(0);
    let frames = 0;
    let request = 0;

    const resize = () => {
      const { width, height, left, top } = canvas.getBoundingClientRect();
      const box = areaRef.current!.getBoundingClientRect();
      if (box.width < 10 || box.height < 10) return;
      const area = { left: box.left - left, top: box.top - top, width: box.width, height: box.height };
      scene = buildScene(view, width, height, area, count);
      canvas.width = Math.round(width * scene.ratio);
      canvas.height = Math.round(height * scene.ratio);
      context.setTransform(1, 0, 0, 1, 0, 0);
      context.drawImage(scene.tape, 0, 0);
    };

    const loop = () => {
      request = requestAnimationFrame(loop);
      const frame = frameRef.current;
      if (!scene || !frame) return;
      if (frame.sequence === drawnSequence && scene === drawnScene) return;
      if (frame.level !== drawnLevel) {
        shade = shadeTable(frame.level);
        drawnLevel = frame.level;
      }
      const ambient = paint(context, scene, frame, shade);
      drawnSequence = frame.sequence;
      drawnScene = scene;
      if (++frames % AMBIENT_EVERY_FRAMES === 0) onAmbient(ambient);
    };

    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    observer.observe(areaRef.current!);
    resize();
    loop();
    return () => {
      cancelAnimationFrame(request);
      observer.disconnect();
    };
  }, [frameRef, areaRef, view, count, onAmbient]);

  return <canvas ref={canvasRef} className="strip-canvas" role="img" aria-label="Live picture of the LED strip" />;
}

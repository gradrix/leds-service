import { CSSProperties, PointerEvent, useRef } from "react";

interface Props {
  label: string;
  value: number;
  min?: number;
  max?: number;
  disabled?: boolean;
  /** Shown instead of the number, for example "42%". */
  display?: string;
  note?: string;
  track?: string;
  onChange: (value: number) => void;
}

/** Sideways travel that starts a drag. Below it, or when mostly vertical, a touch may be a page scroll. */
const DRAG_THRESHOLD_PX = 6;

/** A full-width pill. The hidden native range input supplies keyboard and screen-reader support. */
export function Slider({ label, value, min = 0, max = 100, disabled, display, note, track, onChange }: Props) {
  const gesture = useRef<{ x: number; y: number; start: number; dragging: boolean; moved: boolean } | null>(null);
  const percent = ((value - min) / (max - min)) * 100;

  const valueAt = (event: PointerEvent<HTMLElement>) => {
    const box = event.currentTarget.getBoundingClientRect();
    const fraction = Math.min(1, Math.max(0, (event.clientX - box.left) / box.width));
    return Math.round(min + fraction * (max - min));
  };

  const down = (event: PointerEvent<HTMLElement>) => {
    if (disabled) return;
    gesture.current = { x: event.clientX, y: event.clientY, start: value, dragging: false, moved: false };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const move = (event: PointerEvent<HTMLElement>) => {
    const active = gesture.current;
    if (!active) return;
    const across = Math.abs(event.clientX - active.x);
    const along = Math.abs(event.clientY - active.y);
    if (Math.max(across, along) >= DRAG_THRESHOLD_PX) active.moved = true;
    if (!active.dragging && across >= DRAG_THRESHOLD_PX && across > 2 * along) active.dragging = true;
    if (active.dragging) onChange(valueAt(event));
  };

  // The browser took the gesture for a page scroll after all.
  const cancel = () => {
    if (gesture.current?.dragging) onChange(gesture.current.start);
    gesture.current = null;
  };

  const up = (event: PointerEvent<HTMLElement>) => {
    if (gesture.current && !gesture.current.moved) onChange(valueAt(event));
    gesture.current = null;
  };

  return (
    <label
      className={`slider${track ? " slider-gradient" : ""}`}
      data-disabled={disabled || undefined}
      style={{ "--percent": `${percent}%`, "--track": track } as CSSProperties}
      onPointerDown={down}
      onPointerMove={move}
      onPointerUp={up}
      onPointerCancel={cancel}
    >
      <span className="slider-fill" aria-hidden />
      <span className="slider-label">{label}</span>
      <span className="slider-value">{note ?? display ?? value}</span>
      <input
        type="range"
        aria-label={label}
        min={min}
        max={max}
        value={value}
        disabled={disabled}
        aria-valuetext={display}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </label>
  );
}

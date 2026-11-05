import { CSSProperties, useCallback, useEffect, useRef, useState } from "react";
import { inkFor } from "./color";
import { ColorPanel } from "./components/ColorPanel";
import { PowerButton } from "./components/PowerButton";
import { ProgramGrid } from "./components/ProgramGrid";
import { Slider } from "./components/Slider";
import { StripView } from "./strip/layout";
import { StripCanvas } from "./strip/StripCanvas";
import { useLedService } from "./useLedService";

const VIEW_KEY = "strip-view";

function savedView(): StripView {
  try {
    return localStorage.getItem(VIEW_KEY) === "room" ? "room" : "snake";
  } catch {
    return "snake";
  }
}

export function App() {
  const { frameRef, layout, status, ledCount, connection, sendFailed, change } = useLedService();
  const [view, setView] = useState<StripView>(savedView);
  const stageRef = useRef<HTMLElement>(null);
  const areaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    try {
      localStorage.setItem(VIEW_KEY, view);
    } catch {
      /* the choice just won't be remembered */
    }
  }, [view]);

  const onAmbient = useCallback(([r, g, b]: [number, number, number]) => {
    const peak = Math.max(r, g, b, 1);
    const lift = Math.min(3, 150 / peak);
    stageRef.current?.style.setProperty("--ambient", `rgb(${r * lift} ${g * lift} ${b * lift} / ${Math.min(0.32, peak / 110)})`);
  }, []);

  const program = layout?.modes.find((mode) => mode.id === status?.mode);
  const color = status?.color ?? "";
  const accentStyle = color ? { "--accent": `#${color}`, "--on-accent": inkFor(color) } : undefined;
  const pill =
    connection === "offline"
      ? { tone: "bad", text: "Offline, retrying" }
      : connection === "busy"
        ? { tone: "wait", text: "Too many viewers" }
        : connection === "connecting"
          ? { tone: "wait", text: "Connecting" }
          : status && !status.isOn
            ? { tone: "preview", text: "Preview, strip is off" }
            : { tone: "live", text: "Live" };

  return (
    <>
    <div className="app" style={accentStyle as CSSProperties}>
      <main className="stage" ref={stageRef} data-preview={(status && !status.isOn) || undefined} data-offline={connection === "offline" || undefined}>
        <StripCanvas frameRef={frameRef} areaRef={areaRef} view={view} count={ledCount} onAmbient={onAmbient} />
        <header className="stage-head">
          <div>
            <p className="eyebrow">{ledCount} LEDs</p>
            <h1>{program?.name ?? "Strip"}</h1>
          </div>
          <div className="stage-tools">
            <p className={`pill pill-${pill.tone}`} role="status">
              <span className="pill-dot" aria-hidden />
              {pill.text}
            </p>
            <div className="views" role="group" aria-label="Strip view">
              {(["snake", "room"] as StripView[]).map((option) => (
                <button key={option} aria-pressed={view === option} onClick={() => setView(option)}>
                  {option === "snake" ? "Snake" : "Room"}
                </button>
              ))}
            </div>
          </div>
        </header>
        <div className="strip-frame" ref={areaRef} />
      </main>

      <aside className="panel" aria-label="Controls">
        <PowerButton isOn={status?.isOn} onToggle={() => status && change("isOn", !status.isOn)} />
        <div className="stack">
          <Slider
            label="Brightness"
            value={status?.brightness ?? 0}
            disabled={!status}
            display={status ? `${status.brightness}%` : "–"}
            onChange={(value) => change("brightness", value)}
          />
          <Slider
            label="Speed"
            value={status?.speed ?? 50}
            min={layout?.minSpeed ?? 0}
            max={layout?.maxSpeed ?? 100}
            disabled={!status || !program?.usesSpeed}
            note={!status ? "–" : program && !program.usesSpeed ? `${program.name} doesn't move` : undefined}
            onChange={(value) => change("speed", value)}
          />
        </div>
        <ProgramGrid programs={layout?.modes ?? []} current={status?.mode} color={color} onSelect={(id) => change("mode", id)} />
        {program?.usesColor && <ColorPanel color={color} onChange={(color) => change("color", color)} />}
      </aside>
    </div>
    <div role="alert">{sendFailed && <p className="notice">That change didn't reach the strip. Try again in a moment.</p>}</div>
    </>
  );
}

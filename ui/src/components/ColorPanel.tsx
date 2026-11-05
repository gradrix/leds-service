import { useEffect, useState } from "react";
import { hexToHueSat, HueSat, hueSatToHex } from "../color";
import { Slider } from "./Slider";

const SWATCHES = [
  ["Warm white", "ffb46b"],
  ["Cool white", "ffffff"],
  ["Amber", "ff8a00"],
  ["Red", "ff1a1a"],
  ["Pink", "ff2d95"],
  ["Violet", "8a2bff"],
  ["Blue", "1f5cff"],
  ["Cyan", "00d5ff"],
  ["Green", "1fe06a"],
];

const HUE_TRACK = "linear-gradient(90deg,#f00,#ff0 16.7%,#0f0 33.3%,#0ff 50%,#00f 66.7%,#f0f 83.3%,#f00)";

interface Props {
  color: string;
  onChange: (color: string) => void;
}

export function ColorPanel({ color, onChange }: Props) {
  // Kept here as well because a grey or black colour loses its hue when converted to hex.
  const [picked, setPicked] = useState<HueSat>({ hue: 30, saturation: 80 });

  useEffect(() => {
    if (color && hueSatToHex(picked) !== color.toLowerCase()) setPicked(hexToHueSat(color));
    // Only the service's colour should move the sliders, not the sliders themselves.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [color]);

  const choose = (next: HueSat) => {
    setPicked(next);
    onChange(hueSatToHex(next));
  };

  const pure = hueSatToHex({ hue: picked.hue, saturation: 100 });
  return (
    <section aria-label="Colour">
      <h2>Colour</h2>
      <div className="swatches">
        <button className="swatch swatch-random" aria-pressed={color === ""} aria-label="Random colours" title="Random colours" onClick={() => onChange("")} />
        {SWATCHES.map(([name, hex]) => (
          <button
            key={hex}
            className="swatch"
            style={{ background: `#${hex}` }}
            aria-pressed={color.toLowerCase() === hex}
            aria-label={name}
            title={name}
            onClick={() => onChange(hex)}
          />
        ))}
      </div>
      <div className="stack">
        <Slider label="Hue" value={picked.hue} max={359} track={HUE_TRACK} display={`${picked.hue}°`} onChange={(hue) => choose({ ...picked, hue })} />
        <Slider
          label="Saturation"
          value={picked.saturation}
          track={`linear-gradient(90deg,#fff,#${pure})`}
          display={`${picked.saturation}%`}
          onChange={(saturation) => choose({ ...picked, saturation })}
        />
      </div>
    </section>
  );
}

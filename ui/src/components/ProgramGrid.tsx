import { CSSProperties } from "react";
import { Program } from "../api";

const PLACEHOLDERS = 6;

interface Props {
  programs: Program[];
  current: number | undefined;
  color: string;
  onSelect: (id: number) => void;
}

export function ProgramGrid({ programs, current, color, onSelect }: Props) {
  return (
    <section aria-label="Effect">
      <h2>Effect</h2>
      <div className="programs">
        {programs.length === 0 && Array.from({ length: PLACEHOLDERS }, (_, i) => <span key={i} className="program program-placeholder" aria-hidden />)}
        {programs.map((program) => (
          <button
            key={program.id}
            className="program"
            aria-pressed={program.id === current}
            onClick={() => onSelect(program.id)}
          >
            <span
              className={`program-art art-${program.name.toLowerCase()}`}
              style={{ "--chosen": color ? `#${color}` : undefined } as CSSProperties}
              aria-hidden
            />
            {program.name}
          </button>
        ))}
      </div>
    </section>
  );
}

interface Props {
  isOn: boolean | undefined;
  onToggle: () => void;
}

export function PowerButton({ isOn, onToggle }: Props) {
  const known = isOn !== undefined;
  return (
    <button className="power" aria-label="Strip power" aria-pressed={!!isOn} disabled={!known} onClick={onToggle}>
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round">
        <path d="M12 3v8" />
        <path d="M6.3 7.2a8 8 0 1 0 11.4 0" />
      </svg>
      <span className="power-text">
        <strong>{known ? (isOn ? "On" : "Off") : "Power"}</strong>
        <small>{known ? (isOn ? "Strip is lit" : "Strip is dark") : "Finding the strip"}</small>
      </span>
      <span className="power-switch" aria-hidden />
    </button>
  );
}

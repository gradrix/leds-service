export interface Status {
  isOn: boolean;
  brightness: number;
  mode: number;
  speed: number;
  color: string;
}

export interface Program {
  id: number;
  name: string;
  usesSpeed: boolean;
  usesColor: boolean;
}

export interface Layout {
  modes: Program[];
  minSpeed: number;
  maxSpeed: number;
}

async function json<T>(response: Response): Promise<T> {
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json() as Promise<T>;
}

export const getLayout = () => fetch("/api/layout/").then((r) => json<Layout>(r));
export const getStatus = () => fetch("/api/status/").then((r) => json<Status>(r));

export const changeStatus = (key: keyof Status, value: Status[keyof Status]) =>
  fetch("/api/changestatus/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key, value }),
  }).then((r) => json<Status>(r));

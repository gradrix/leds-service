import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { changeStatus, getLayout, getStatus, Layout, Status } from "./api";
import { ChangeQueue } from "./changeQueue";
import { decodePixels } from "./strip/shade";

export interface LiveFrame {
  pixels: Uint8Array;
  level: number;
  sequence: number;
}

/** `busy`: the service answers but refused a picture stream, because too many are open. */
export type Connection = "connecting" | "live" | "offline" | "busy";

const DEFAULT_LED_COUNT = 360;
const RETRY_MS = 3000;
const OFFLINE_AFTER_MS = 4000;
const NOTICE_MS = 6000;
/** Unconfirmed values expire on a timer, and a static effect sends nothing to re-render on. */
const HOLD_CHECK_MS = 500;

export function useLedService() {
  const frameRef = useRef<LiveFrame | null>(null);
  const [layout, setLayout] = useState<Layout | null>(null);
  const [served, setServed] = useState<Status | null>(null);
  const [ledCount, setLedCount] = useState(DEFAULT_LED_COUNT);
  const [connection, setConnection] = useState<Connection>("connecting");
  const [sendFailed, setSendFailed] = useState(false);
  const [, redraw] = useState(0);

  const queue = useMemo(
    () =>
      new ChangeQueue<Status>(
        async (key, value) => {
          setServed(await changeStatus(key, value));
          setSendFailed(false);
        },
        () => setSendFailed(true),
      ),
    [],
  );

  const change = useCallback(
    <K extends keyof Status>(key: K, value: Status[K]) => {
      queue.set(key, value);
      redraw((n) => n + 1);
    },
    [queue],
  );

  useEffect(() => {
    if (!sendFailed) return;
    const timer = setTimeout(() => setSendFailed(false), NOTICE_MS);
    return () => clearTimeout(timer);
  }, [sendFailed]);

  useEffect(() => {
    const timer = setInterval(() => redraw((n) => n + 1), HOLD_CHECK_MS);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (layout) return;
    const load = () => getLayout().then(setLayout).catch(() => undefined);
    load();
    const timer = setInterval(load, RETRY_MS);
    return () => clearInterval(timer);
  }, [layout]);

  useEffect(() => {
    let source: EventSource | null = null;
    let retry: ReturnType<typeof setTimeout> | undefined;
    let silence: ReturnType<typeof setTimeout> | undefined;

    const expectFrames = () => {
      silence ??= setTimeout(() => setConnection("offline"), OFFLINE_AFTER_MS);
    };

    const heard = () => {
      clearTimeout(silence);
      silence = undefined;
      expectFrames();
    };

    const refused = () => {
      // EventSource gives up after a non-200 answer, so ask why and try again ourselves.
      getStatus()
        .then((status) => {
          setServed(status);
          clearTimeout(silence);
          silence = undefined;
          setConnection("busy");
        })
        .catch(() => setConnection("offline"));
      retry = setTimeout(open, RETRY_MS);
    };

    const open = () => {
      source?.close();
      expectFrames();
      source = new EventSource("/api/frames/");
      source.addEventListener("status", (event) => setServed(JSON.parse((event as MessageEvent).data)));
      source.addEventListener("frame", (event) => {
        const { pixels, level, sequence } = JSON.parse((event as MessageEvent).data);
        const decoded = decodePixels(pixels);
        frameRef.current = { pixels: decoded, level, sequence };
        setLedCount(decoded.length / 3);
        setConnection("live");
        heard();
      });
      source.addEventListener("offline", () => setConnection("offline"));
      source.onerror = () => {
        if (source?.readyState === EventSource.CLOSED) refused();
      };
    };

    const close = () => {
      source?.close();
      source = null;
      clearTimeout(retry);
      clearTimeout(silence);
      silence = undefined;
    };

    // A hidden tab should not keep a stream open on the Pi.
    const onVisibility = () => {
      if (document.hidden) {
        close();
      } else {
        setConnection("connecting");
        open();
      }
    };

    open();
    document.addEventListener("visibilitychange", onVisibility);
    return () => {
      close();
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, []);

  const status = served ? queue.overlay(served) : null;
  return { frameRef, layout, status, ledCount, connection, sendFailed, change };
}

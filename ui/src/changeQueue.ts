export type Send<K, V> = (key: K, value: V) => Promise<void>;

interface Entry<V> {
  value: V;
  sending: boolean;
  dirty: boolean;
  settledAt: number | null;
}

/**
 * Sends slider drags without flooding the Pi, and keeps the control showing the user's value
 * until the service agrees: one request per key at a time, the newest value wins, and values
 * reported by the service are overlaid until they match or `holdMs` passes after the last send.
 */
export class ChangeQueue<S extends object> {
  private entries = new Map<keyof S, Entry<S[keyof S]>>();

  constructor(
    private send: Send<keyof S, S[keyof S]>,
    private onError: () => void,
    private gapMs = 70,
    private holdMs = 1500,
    private now: () => number = () => performance.now(),
  ) {}

  set<K extends keyof S>(key: K, value: S[K]): void {
    const entry = this.entries.get(key);
    if (entry) {
      entry.value = value;
      entry.dirty = true;
      entry.settledAt = null;
      if (!entry.sending) this.flush(key, entry);
      return;
    }
    const created: Entry<S[keyof S]> = { value, sending: false, dirty: true, settledAt: null };
    this.entries.set(key, created);
    this.flush(key, created);
  }

  private flush(key: keyof S, entry: Entry<S[keyof S]>): void {
    entry.sending = true;
    entry.dirty = false;
    this.send(key, entry.value)
      .catch(() => {
        this.entries.delete(key);
        this.onError();
      })
      .finally(() => {
        setTimeout(() => {
          entry.sending = false;
          if (entry.dirty && this.entries.get(key) === entry) this.flush(key, entry);
          else entry.settledAt = this.now();
        }, this.gapMs);
      });
  }

  /** The service's status with unconfirmed user values on top. */
  overlay(status: S): S {
    const merged = { ...status };
    for (const [key, entry] of this.entries) {
      const settled = entry.settledAt !== null;
      if (settled && (status[key] === entry.value || this.now() - entry.settledAt! > this.holdMs)) {
        this.entries.delete(key);
      } else {
        merged[key] = entry.value;
      }
    }
    return merged;
  }
}

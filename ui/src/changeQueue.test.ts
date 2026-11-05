import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ChangeQueue } from "./changeQueue";

interface State {
  brightness: number;
  speed: number;
}

const GAP = 70;
const HOLD = 1500;

describe("ChangeQueue", () => {
  let sent: Array<[keyof State, number]>;
  let resolve: Array<() => void>;
  let queue: ChangeQueue<State>;
  let errors: number;

  const settle = async () => {
    resolve.shift()?.();
    await vi.advanceTimersByTimeAsync(GAP);
  };

  beforeEach(() => {
    vi.useFakeTimers();
    sent = [];
    resolve = [];
    errors = 0;
    queue = new ChangeQueue<State>(
      (key, value) => {
        sent.push([key, value]);
        return new Promise((done) => resolve.push(done));
      },
      () => (errors += 1),
      GAP,
      HOLD,
      () => Date.now(),
    );
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("sends the first value at once and only the newest while a request is out", async () => {
    queue.set("brightness", 1);
    queue.set("brightness", 2);
    queue.set("brightness", 3);
    expect(sent).toEqual([["brightness", 1]]);
    await settle();
    expect(sent).toEqual([["brightness", 1], ["brightness", 3]]);
  });

  it("keeps the dragged value against a stale status", async () => {
    queue.set("brightness", 80);
    expect(queue.overlay({ brightness: 10, speed: 5 }).brightness).toBe(80);
    await settle();
    expect(queue.overlay({ brightness: 10, speed: 5 }).brightness).toBe(80);
  });

  it("follows the service again once it agrees", async () => {
    queue.set("brightness", 80);
    await settle();
    expect(queue.overlay({ brightness: 80, speed: 5 }).brightness).toBe(80);
    expect(queue.overlay({ brightness: 30, speed: 5 }).brightness).toBe(30);
  });

  it("gives up holding when the service never agrees, such as after clamping", async () => {
    queue.set("brightness", 80);
    await settle();
    await vi.advanceTimersByTimeAsync(HOLD + 1);
    expect(queue.overlay({ brightness: 70, speed: 5 }).brightness).toBe(70);
  });

  it("does not hold other keys", () => {
    queue.set("brightness", 80);
    expect(queue.overlay({ brightness: 10, speed: 5 }).speed).toBe(5);
  });

  it("reports a failed send and shows the service value again", async () => {
    const failing = new ChangeQueue<State>(() => Promise.reject(new Error("down")), () => (errors += 1), GAP, HOLD, () => Date.now());
    failing.set("brightness", 80);
    await vi.advanceTimersByTimeAsync(GAP);
    expect(errors).toBe(1);
    expect(failing.overlay({ brightness: 10, speed: 5 }).brightness).toBe(10);
  });
});

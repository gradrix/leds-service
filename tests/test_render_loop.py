"""Behaviour of the render loop: what reaches the strip, and what the mirror sees."""
import random
import threading

import pytest

from gpio_service.common.brightness import brightnessLevel
from gpio_service.common.ledsbase import LedsBase
from gpio_service.controller import Controller
from gpio_service.settings import Settings

COUNT = 360
SOLID, COLLIDERS, RAINBOW, CHRISTMAS, COMET, AURORA = 1, 2, 3, 4, 5, 6
ANIMATED = [COLLIDERS, RAINBOW, CHRISTMAS, COMET, AURORA]


class FakeStrip(LedsBase):
    def __init__(self):
        self.writes = []

    def write(self, pixels, level):
        self.writes.append((bytes(pixels), level))

    def count(self):
        return COUNT

    @property
    def last(self):
        return self.writes[-1]


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


@pytest.fixture
def rig(tmp_path, monkeypatch):
    monkeypatch.setattr("gpio_service.settings.STATE_FILE", str(tmp_path / "saved-data"))

    def build(mode=SOLID, isOn=True, brightness=50, color="ff8000"):
        settings = Settings()
        settings.isOn = isOn
        settings.mode = mode
        settings.brightness = brightness
        settings.color = color
        strip = FakeStrip()
        clock = Clock()
        controller = Controller(strip, settings, clock=clock)
        return controller, strip, clock

    return build


def run_for(controller, clock, seconds, step=0.02):
    for _ in range(round(seconds / step)):
        clock.now += step
        controller.tick()


def lit(pixels):
    return sum(1 for i in range(0, len(pixels), 3) if any(pixels[i:i + 3]))


def test_solid_paints_the_chosen_colour_in_true_rgb(rig):
    controller, strip, _ = rig(color="ff8000")
    controller.tick()
    assert strip.last[0][:3] == bytes((0xff, 0x80, 0x00))
    assert lit(strip.last[0]) == COUNT


@pytest.mark.parametrize("mode", [SOLID] + ANIMATED)
def test_brightness_reaches_the_strip_on_the_next_tick_in_every_program(rig, mode):
    controller, strip, clock = rig(mode=mode, brightness=50)
    controller.tick()
    controller.changeBrightness(80)
    clock.now += 0.02
    controller.tick()
    assert strip.last[1] == brightnessLevel(80)


def test_static_program_tells_the_loop_to_sleep_but_a_command_wakes_it(rig):
    controller, strip, _ = rig(mode=SOLID)
    assert controller.tick() >= 0.5
    controller.wake.clear()
    controller.changeColor("00ff00")
    assert controller.wake.is_set()
    controller.tick()
    assert strip.last[0][:3] == bytes((0, 255, 0))


@pytest.mark.parametrize("mode", ANIMATED)
def test_animated_programs_draw_and_change_over_time(rig, mode):
    controller, strip, clock = rig(mode=mode, color="")
    run_for(controller, clock, 0.5)
    first = strip.last[0]
    run_for(controller, clock, 1.0)
    assert lit(strip.last[0]) > 0
    assert strip.last[0] != first


def test_programs_run_time_based_and_ask_for_about_50_fps(rig):
    controller, _, _ = rig(mode=RAINBOW)
    assert 0 < controller.tick() <= 0.02


def collider_travel(rig, speed):
    random.seed(7)
    controller, _, clock = rig(mode=COLLIDERS)
    controller.changeSpeed(speed)
    sticks = controller.repo.currentProgram.sticks
    travel = 0.0
    for _ in range(100):
        before = [stick.pos for stick in sticks]
        clock.now += 0.02
        controller.tick()
        travel += sum(abs(stick.pos - b) for stick, b in zip(sticks, before))
    return travel


def test_collider_speed_changes_how_fast_sticks_travel(rig):
    assert collider_travel(rig, 100) > 8 * collider_travel(rig, 0)


def test_colliders_stay_on_the_strip_and_never_overlap(rig):
    random.seed(3)
    controller, _, clock = rig(mode=COLLIDERS)
    controller.changeSpeed(100)
    sticks = controller.repo.currentProgram.sticks
    for _ in range(500):
        clock.now += 0.02
        controller.tick()
        assert all(0 <= s.pos and s.pos + s.size <= COUNT for s in sticks)
        ordered = sorted(sticks, key=lambda s: s.pos)
        assert all(a.pos + a.size <= b.pos + 1e-6 for a, b in zip(ordered, ordered[1:]))


def rainbow_shift(rig, speed):
    controller, strip, clock = rig(mode=RAINBOW)
    controller.changeSpeed(speed)
    clock.now += 0.02
    controller.tick()
    start = controller.repo.currentProgram.phase
    run_for(controller, clock, 0.2)
    return controller.repo.currentProgram.phase - start


def test_rainbow_speed_is_monotonic_and_zero_does_not_crash(rig):
    assert 0 < rainbow_shift(rig, 0) < rainbow_shift(rig, 50) < rainbow_shift(rig, 100)


def test_speed_is_remembered_per_program(rig):
    controller, _, _ = rig(mode=COLLIDERS)
    controller.changeSpeed(90)
    controller.changeMode(RAINBOW)
    assert controller.settings.speed == 50
    controller.changeSpeed(10)
    controller.changeMode(COLLIDERS)
    assert controller.settings.speed == 90


@pytest.mark.parametrize("change,value,attr,expected", [
    ("changeBrightness", 300, "brightness", 100),
    ("changeBrightness", -5, "brightness", 0),
    ("changeSpeed", 300, "speed", 100),
    ("changeSpeed", -5, "speed", 0),
])
def test_values_are_clamped(rig, change, value, attr, expected):
    controller, _, _ = rig()
    getattr(controller, change)(value)
    assert getattr(controller.settings, attr) == expected


def test_unknown_program_is_ignored(rig):
    controller, _, _ = rig(mode=RAINBOW)
    controller.changeMode(99)
    assert controller.settings.mode == RAINBOW


def test_colour_change_does_not_restart_colliders_but_repaints_the_sticks(rig):
    controller, strip, clock = rig(mode=COLLIDERS, color="ff0000")
    controller.tick()
    sticks = controller.repo.currentProgram.sticks
    run_for(controller, clock, 0.2)
    controller.changeColor("00ff00")
    clock.now += 0.02
    controller.tick()
    assert controller.repo.currentProgram.sticks is sticks
    pixels = strip.last[0]
    colours = {bytes(pixels[i:i + 3]) for i in range(0, len(pixels), 3)}
    assert colours == {bytes((0, 0, 0)), bytes((0, 255, 0))}


def test_colour_change_does_not_send_a_comet_back_to_the_start(rig):
    controller, _, clock = rig(mode=COMET, color="ff0000")
    run_for(controller, clock, 1.0)
    position = controller.repo.currentProgram.position
    controller.changeColor("00ff00")
    clock.now += 0.02
    controller.tick()
    assert controller.repo.currentProgram.position > position


def test_choosing_random_gives_solid_a_new_colour(rig):
    controller, strip, clock = rig(mode=SOLID, color="123456")
    controller.tick()
    controller.changeColor("")
    clock.now += 0.02
    controller.tick()
    assert strip.last[0][:3] != bytes((0x12, 0x34, 0x56))


def test_off_blanks_the_hardware_at_once(rig):
    controller, strip, clock = rig(mode=RAINBOW)
    controller.tick()
    controller.changeOnOff(False)
    clock.now += 0.02
    controller.tick()
    assert lit(strip.last[0]) == 0


def test_off_with_a_viewer_previews_on_the_mirror_while_the_hardware_stays_dark(rig):
    controller, strip, clock = rig(mode=RAINBOW, isOn=False)
    with controller.bus.subscribe():
        run_for(controller, clock, 0.2)
        frame = controller.bus.latest
    assert lit(frame.pixels) == COUNT
    assert all(lit(pixels) == 0 for pixels, _ in strip.writes)


def test_off_without_viewers_idles(rig):
    controller, _, _ = rig(mode=RAINBOW, isOn=False)
    assert controller.tick() >= 0.5


def test_mirror_frame_matches_what_the_strip_received(rig):
    controller, strip, clock = rig(mode=COLLIDERS)
    run_for(controller, clock, 0.1)
    frame = controller.bus.latest
    assert (frame.pixels, frame.level) == strip.last


def test_slider_drag_does_not_hammer_the_sd_card(rig, monkeypatch):
    controller, _, clock = rig()
    saves = []
    monkeypatch.setattr(controller.settings, "saveToFile", lambda: saves.append(clock.now))
    for value in range(40):
        controller.changeBrightness(value)
        clock.now += 0.05
        controller.tick()
    assert saves == []
    clock.now += 3
    controller.tick()
    controller.tick()
    assert len(saves) == 1


def test_commands_from_other_threads_do_not_break_the_loop(rig):
    controller, _, clock = rig(mode=COLLIDERS)
    stop = threading.Event()

    def spam():
        value = 0
        while not stop.is_set():
            value = (value + 7) % 101
            controller.changeSpeed(value)
            controller.changeBrightness(value)
            controller.changeMode(1 + value % 6)
            controller.changeColor("" if value % 2 else "00ff00")

    thread = threading.Thread(target=spam)
    thread.start()
    try:
        run_for(controller, clock, 4)
    finally:
        stop.set()
        thread.join()

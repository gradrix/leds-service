import threading
import time

from gpio_service.common.brightness import BRIGHTNESS_MAX, brightnessLevel
from gpio_service.common.framebuffer import FrameBuffer
from gpio_service.common.framebus import FrameBus
from gpio_service.ledprogramrepository import LedProgramRepository
from gpio_service.settings import Settings

FRAME_SECONDS = 0.02
IDLE_SECONDS = 1.0
# A dropped frame must not make programs jump.
MAX_FRAME_STEP_SECONDS = 0.1
# The state file is on an SD card and slider drags send many changes.
SAVE_DELAY_SECONDS = 2.0
SPEED_MAX = 100


class Controller:
    """Owns the strip. Commands arrive on gRPC threads and only change settings;
    the render loop (one thread) is the only thing that draws or touches the hardware."""

    def __init__(self, driver, settings=None, clock=time.monotonic):
        if settings is None:
            settings = Settings()
            settings.openFromFile()
        self.settings = settings
        self.driver = driver
        self.clock = clock
        self.lock = threading.Lock()
        self.wake = threading.Event()
        self.changed = True
        self.restartProgram = False
        self.colorChanged = False
        self.saveAt = None
        self.lastTick = clock()
        self.nextRefresh = 0
        self.frame = FrameBuffer(driver.count())
        self.dark = bytes(driver.count() * 3)
        self.bus = FrameBus(onSubscribe=self.requestRedraw)
        self.repo = LedProgramRepository(self.settings, self.frame)

    # -----------------------------
    # Commands (any thread)
    # -----------------------------
    def requestRedraw(self):
        with self.lock:
            self.changed = True
        self.wake.set()

    def commit(self, restartProgram=False):
        with self.lock:
            self.restartProgram = self.restartProgram or restartProgram
            self.saveAt = self.clock() + SAVE_DELAY_SECONDS
        self.requestRedraw()

    def changeOnOff(self, value):
        self.settings.isOn = value
        self.commit()

    def changeBrightness(self, value):
        self.settings.brightness = max(0, min(BRIGHTNESS_MAX, value))
        self.commit()

    def changeMode(self, value):
        """Returns False when no such program exists."""
        with self.lock:
            known = self.repo.changeMode(value)
        if known:
            self.commit(restartProgram=True)
        return known

    def changeSpeed(self, value):
        self.settings.speed = max(0, min(SPEED_MAX, value))
        self.commit()

    def changeColor(self, value):
        self.settings.color = value
        with self.lock:
            self.colorChanged = True
        self.commit()

    def resetSettings(self):
        self.settings.reset()
        self.commit(restartProgram=True)

    def getModeLayout(self):
        return self.repo.getModeLayout()

    # -----------------------------
    # Render loop (one thread)
    # -----------------------------
    def tick(self):
        """Draw one frame if one is due; returns how long the loop may sleep."""
        now = self.clock()
        seconds = min(now - self.lastTick, MAX_FRAME_STEP_SECONDS)
        self.lastTick = now

        with self.lock:
            program = self.repo.currentProgram
            restartProgram, self.restartProgram = self.restartProgram, False
            colorChanged, self.colorChanged = self.colorChanged, False
            changed, self.changed = self.changed, False
        isOn = bool(self.settings.isOn)
        # Viewers get a preview while the strip is off; the hardware stays dark.
        drawing = isOn or self.bus.hasSubscribers
        running = drawing and program.animated
        # Rewriting a held picture recovers from a glitch on the data line.
        refresh = now >= self.nextRefresh

        if restartProgram:
            program.initialize()
        elif colorChanged:
            program.colorChanged()
        if drawing and (running or changed or refresh):
            program.render(seconds)
            pixels = self.frame.snapshot()
            level = brightnessLevel(self.settings.brightness)
            if isOn:
                self.driver.write(pixels, level)
            self.bus.publish(pixels, level)
        if not isOn and (changed or refresh):
            self.driver.write(self.dark, 0)
        if refresh:
            self.nextRefresh = now + IDLE_SECONDS

        self.saveIfDue(now)
        if not running:
            return IDLE_SECONDS
        return max(0.001, FRAME_SECONDS - (self.clock() - now))

    def saveIfDue(self, now):
        with self.lock:
            due = self.saveAt is not None and now >= self.saveAt
            if due:
                self.saveAt = None
        if due:
            self.settings.saveToFile()

    def flush(self):
        with self.lock:
            pending, self.saveAt = self.saveAt, None
        if pending is not None:
            self.settings.saveToFile()

    def run(self, stop):
        while not stop.is_set():
            pause = self.tick()
            self.wake.wait(pause)
            self.wake.clear()

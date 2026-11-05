import math
import random

from gpio_service.common.color import Color
from gpio_service.common.ledprogrambase import LedProgramBase

MIN_SIZE = 2
MAX_SIZE = 6
OBJ_AMOUNT = 15
SLOWEST_MS_PER_LED = 300
FASTEST_MS_PER_LED = 15


class Stick:
    def __init__(self, pos, size, color):
        self.pos = float(pos)
        self.size = size
        self.color = color
        direction = random.choice((-1, 1))
        self.velocity = direction * 1000 / random.randint(FASTEST_MS_PER_LED, SLOWEST_MS_PER_LED)


class Colliders(LedProgramBase):
    """Sticks of light on a line: equal masses, so a collision swaps velocities."""

    modeIndex = 2
    modeName = "Colliders"
    usesColor = True

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.sticks = []
        for _ in range(OBJ_AMOUNT):
            self.spawnSingle()
        # Sticks can never pass each other, so this order holds from here on.
        self.sticks.sort(key=lambda stick: stick.pos)

    def spawnSingle(self):
        for _ in range(10):
            size = random.randint(MIN_SIZE, MAX_SIZE)
            start = random.randint(0, self.leds.count() - size)
            if all(start + size < stick.pos or stick.pos + stick.size < start for stick in self.sticks):
                self.sticks.append(Stick(start, size, self.newColor()))
                return

    def colorChanged(self):
        for stick in self.sticks:
            stick.color = self.newColor()

    def newColor(self):
        return Color.fromHex(self.settings.color) if self.settings.color else Color.generateRandom()

    def render(self, seconds):
        elapsed = seconds * self.speedScale()
        fastest = max(abs(stick.velocity) for stick in self.sticks)
        # Small enough steps that no stick can jump through another.
        steps = max(1, math.ceil(fastest * elapsed))
        for _ in range(steps):
            self.advance(elapsed / steps)
        self.draw()

    def advance(self, seconds):
        count = self.leds.count()
        sticks = self.sticks
        for stick in sticks:
            stick.pos += stick.velocity * seconds
        first, last = sticks[0], sticks[-1]
        if first.pos < 0:
            first.velocity = abs(first.velocity)
        if last.pos + last.size > count:
            last.velocity = -abs(last.velocity)

        for left, right in zip(sticks, sticks[1:]):
            if left.pos + left.size > right.pos and left.velocity > right.velocity:
                left.velocity, right.velocity = right.velocity, left.velocity
                if not self.settings.color:
                    left.color = Color.generateRandom()
                    right.color = Color.generateRandom()

        # Separate whatever still overlaps, walls first, so the invariant survives a pile-up.
        first.pos = max(first.pos, 0)
        for left, right in zip(sticks, sticks[1:]):
            right.pos = max(right.pos, left.pos + left.size)
        last.pos = min(last.pos, count - last.size)
        for left, right in zip(reversed(sticks[:-1]), reversed(sticks[1:])):
            left.pos = min(left.pos, right.pos - left.size)

    def draw(self):
        self.leds.clear()
        for stick in self.sticks:
            start = int(stick.pos)
            rgb = stick.color.toRGB()
            for i in range(start, min(start + stick.size, self.leds.count())):
                self.leds[i] = rgb

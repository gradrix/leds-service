import colorsys
import random

from gpio_service.common.color import Color
from gpio_service.common.ledprogrambase import LedProgramBase

COMETS = 3
TAIL = 56
LEDS_PER_SECOND = 40
FADE = [(1 - step / TAIL) ** 2.6 for step in range(TAIL)]


class Comet(LedProgramBase):
    """Comets chasing round the strip with long fading tails."""

    modeIndex = 5
    modeName = "Comet"
    usesColor = True

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.position = 0.0
        self.colorChanged()

    def colorChanged(self):
        hue = random.random()
        self.colors = [colorsys.hsv_to_rgb((hue + i / COMETS) % 1, 0.85, 1) for i in range(COMETS)]

    def render(self, seconds):
        count = self.leds.count()
        self.position += seconds * LEDS_PER_SECOND * self.speedScale()
        chosen = Color.fromHex(self.settings.color).toRGB() if self.settings.color else None
        self.leds.clear()
        for comet in range(COMETS):
            head = int(self.position + comet * count / COMETS)
            r, g, b = chosen or tuple(channel * 255 for channel in self.colors[comet])
            for step in range(TAIL):
                fade = FADE[step]
                self.leds[(head - step) % count] = (int(r * fade), int(g * fade), int(b * fade))

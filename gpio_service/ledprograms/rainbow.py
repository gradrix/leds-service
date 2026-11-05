from gpio_service.common.color import Color
from gpio_service.common.ledprogrambase import LedProgramBase

TH = 3
CYCLES_PER_SECOND = 0.2


def wheel(pos):
    """Rainbow colour for a position in 0-255."""
    if pos < 85:
        return Color(pos * TH, 255 - pos * TH, 0)
    if pos < 170:
        pos -= 85
        return Color(255 - pos * TH, 0, pos * TH)
    pos -= 170
    return Color(0, pos * TH, 255 - pos * TH)


WHEEL = [wheel(pos).toRGB() for pos in range(256)]


class Rainbow(LedProgramBase):
    modeIndex = 3
    modeName = "Rainbow"

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.phase = 0.0

    def render(self, seconds):
        self.phase += seconds * CYCLES_PER_SECOND * self.speedScale()
        offset = int(self.phase * 256)
        for i in range(self.leds.count()):
            self.leds[i] = WHEEL[(i + offset) & 255]

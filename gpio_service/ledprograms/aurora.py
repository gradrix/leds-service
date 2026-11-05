import math

from gpio_service.common.ledprogrambase import LedProgramBase

TABLE = 512
WAVE = [0.5 + 0.5 * math.sin(2 * math.pi * i / TABLE) for i in range(TABLE)]
MASK = TABLE - 1
GREEN = (8, 235, 130)
VIOLET = (130, 40, 245)
FLOW_PER_SECOND = 14


class Aurora(LedProgramBase):
    """Slow curtains of green and violet light."""

    modeIndex = 6
    modeName = "Aurora"

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.flow = 0.0

    def render(self, seconds):
        self.flow += seconds * FLOW_PER_SECOND * self.speedScale()
        flow = int(self.flow)
        leds = self.leds
        for i in range(leds.count()):
            mix = WAVE[(i * 2 + flow) & MASK]
            glow = 0.12 + 0.88 * WAVE[(i * 5 - flow * 2) & MASK] * WAVE[(i * 3 + flow) & MASK]
            leds[i] = (
                int((GREEN[0] + (VIOLET[0] - GREEN[0]) * mix) * glow),
                int((GREEN[1] + (VIOLET[1] - GREEN[1]) * mix) * glow),
                int((GREEN[2] + (VIOLET[2] - GREEN[2]) * mix) * glow),
            )

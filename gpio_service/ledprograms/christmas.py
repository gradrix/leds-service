import random

from gpio_service.common.ledprogrambase import LedProgramBase

BLOCK = 9
RED = (220, 16, 16)
GREEN = (16, 170, 44)
STAR = (255, 205, 130)
DRIFT_LEDS_PER_SECOND = 3
STARS_PER_SECOND = 16
STAR_LIFE_SECONDS = 0.9


class Christmas(LedProgramBase):
    """Red and green garland drifting along the strip, with warm stars twinkling on top."""

    modeIndex = 4
    modeName = "Christmas"

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.offset = 0.0
        self.stars = []

    def render(self, seconds):
        scale = self.speedScale()
        count = self.leds.count()
        self.offset += seconds * DRIFT_LEDS_PER_SECOND * scale
        shift = int(self.offset)
        for i in range(count):
            self.leds[i] = RED if ((i + shift) // BLOCK) % 2 else GREEN

        if random.random() < seconds * STARS_PER_SECOND * scale:
            self.stars.append([random.randrange(count), STAR_LIFE_SECONDS])
        for star in self.stars:
            star[1] -= seconds * scale
            if star[1] > 0:
                self.leds[star[0]] = self.twinkle(star[1] / STAR_LIFE_SECONDS)
        self.stars = [star for star in self.stars if star[1] > 0]

    def twinkle(self, life):
        return tuple(int(channel * life) for channel in STAR)

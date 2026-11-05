from gpio_service.common.color import Color
from gpio_service.common.ledprogrambase import LedProgramBase


class Solid(LedProgramBase):
    modeIndex = 1
    modeName = "Solid"
    usesSpeed = False
    usesColor = True
    animated = False

    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()

    def initialize(self):
        self.randomColor = Color.generateRandom()

    def colorChanged(self):
        self.initialize()

    def render(self, seconds):
        color = Color.fromHex(self.settings.color) if self.settings.color else self.randomColor
        self.leds.fill(color.toRGB())

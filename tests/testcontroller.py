import time
import sys
import neopixel
import board
from settings import Settings
from controller import Controller
from tests.ledstestwrapper import LedsTestWrapper

# LED strip configuration:
LED_COUNT       = 360       # Number of LED pixels

class TestController(Controller):
    def __init__(self, leds):
        self.settings = Settings()
        self.settings.ledCount = LED_COUNT
        self.settings.openFromFile()
        self.settings.isOn = True
        self.leds = leds
        self.leds.initialize(LED_COUNT)
        super().__init__(leds = leds, settings = self.settings)

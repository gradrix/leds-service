import time
from neopixel import *
from common.ledprogrambase import LedProgramBase

TH = 3

class Rainbow(LedProgramBase):
    
    #Constructor
    def __init__(self, settings, leds):
      super().__init__(settings, leds)
    #end

    #LedProgramBase implementation
    modeIndex = 1
    modeName = "Rainbow"
    minSpeed = 20
    maxSpeed = 200

    def show(self):
        self.rainbow()
    #end
   
    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * TH, 255 - pos * TH, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * TH, 0, pos * TH)
        else:
            pos -= 170
            return Color(0, pos * TH, 255 - pos * TH)

    def rainbow(self, wait_ms=3, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.settings.strip.numPixels()):
                self.settings.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.settings.strip.show()
            time.sleep(1 / (self.settings.speed))
    


import time
from common.ledprogrambase import LedProgramBase
from common.color import Color

class Solid(LedProgramBase):

    #Constructor
    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()
    #end

    #LedProgramBase implementation
    modeIndex = 0
    modeName = "Solid"
    minSpeed = 0
    maxSpeed = 100

    def initialize(self):
        if (self.settings.color == ""):
            self.color = Color.generateRandom()
        
    def show(self):
        if (self.settings.color != ""):
            self.color = Color.fromHex(self.settings.color)

        for i in range(self.leds.count()):
            self.leds[i] = self.color.toRGB()
    
        self.leds.refresh()
        time.sleep(1)
    #end

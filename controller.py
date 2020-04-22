import time
import sys
import board
from settings import Settings
from ledprogramrepository import LedProgramRepository
from common.ledswrapper import LedsWrapper

# LED strip configuration:
LED_COUNT       = 360       # Number of LED pixels
LED_PIN         = board.D18 # GPIO pin connectedto the pixels (18 uses PWM!).

class Controller():
    """
    Class full of stuff needed to control leds through RaspberyPi
    """
    def __init__(self, leds = None, settings = None):
          
        if (settings == None):
          self.settings = Settings(None)
          self.settings.ledCount = LED_COUNT
          self.settings.openFromFile()
        else:
          self.settings = settings

        if (leds == None):
          leds = LedsWrapper(LED_PIN, LED_COUNT)
        else:
          leds = leds
        self.leds = leds
        self.repo = LedProgramRepository(self.settings, leds)

    #Making changes
    def change(self, command):
        value = None
        #Brightness
        if (command.find("B:") != -1):
            value = command.replace("B:", "")
            self.settings.brightness = int(value)
            self.leds.changeBrightness(self.settings.brightness)
        #Switch ON/OFF
        elif (command.find("O:") != -1):
            value = command.replace("O:", "")
            if (value == "0"):
                self.settings.isOn = False
                self.leds.clear(True)
            else:
                self.settings.isOn = True
        #Mode
        elif (command.find("M:") != -1):
            value = int(command.replace("M:", ""))
            self.repo.changeMode(value)
        #Toggle
        elif (command.find("T:") != -1):
            value = command.replace("T:", "")
            self.settings.toggle = int(value)
        #Speed
        elif (command.find("S:") != -1):
            value = command.replace("S:", "")
            self.settings.speed = int(value)
        
        self.settings.saveToFile()
        return self.settings

    def getModeLayout(self):
        return self.repo.getModeLayout()

    def show(self):
        if (self.settings.isOn):
          self.repo.show()
        else:
          time.sleep(5)

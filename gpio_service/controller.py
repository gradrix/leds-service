import time
from gpio_service.settings import Settings
from gpio_service.ledprogramrepository import LedProgramRepository

# -----------------------------
# Controller which changes led behavour values based on received commands
# -----------------------------
class Controller():
    def __init__(self, leds, settings = None):
        if (settings == None):
          self.settings = Settings()
          self.settings.openFromFile()
        else:
          self.settings = settings
        print("Initializing leds with:")
        print("Brightness: "+str(self.settings.brightness)+" isOn: "+str(self.settings.isOn))
        self.leds = leds
        self.repo = LedProgramRepository(self.settings, leds)
        #Init
        self.leds.changeBrightness(self.settings.brightness)
        if (self.settings.isOn == False):
            self.leds.clear(True)

    # -----------------------------
    # Making led setting changes
    # -----------------------------
    def changeOnOff(self, value):
        self.settings.isOn = value
        if (value == False):
            self.leds.clear(True)
        self.settings.saveToFile()
        return self.settings
    
    def changeBrightness(self, value):
        self.settings.brightness = value
        self.leds.changeBrightness(self.settings.brightness)
        self.settings.saveToFile()
        return self.settings
    
    def changeMode(self, value):
        self.repo.changeMode(value, True)
        self.settings.saveToFile()
        return self.settings
    
    def changeToggleValue(self, value):
        self.settings.toggle = value
        self.settings.saveToFile()
        return self.settings
    
    def changeSpeed(self, value):
        self.settings.speed = value
        self.settings.saveToFile()
        return self.settings
    
    def changeColor(self, value):
        self.settings.color = value
        self.repo.reinitializeLedProgram()
        self.settings.saveToFile()
        return self.settings

    # -----------------------------
    # Gets led program layout
    # -----------------------------
    def getModeLayout(self):
        return self.repo.getModeLayout()

    # -----------------------------
    # Runs current program frame
    # -----------------------------
    def show(self):
        if (self.settings.isOn):
          self.repo.show()
        else:
          self.leds.clear(True)
          time.sleep(1)

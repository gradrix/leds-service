import time
from settings import Settings
from ledprogramrepository import LedProgramRepository

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
    def change(self, command):
        value = None
        #Brightness
        if (command.find("B:") != -1):
            value = command.replace("B:", "")
            if (int(value) > 100):
              value = 100
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
            value = command.replace("M:", "")
            self.repo.changeMode(int(value), True)
        #Toggle
        elif (command.find("T:") != -1):
            value = command.replace("T:", "")
            self.settings.toggle = int(value)
        #Speed
        elif (command.find("S:") != -1):
            value = command.replace("S:", "")
            self.settings.speed = int(value)
        #Color
        elif (command.find("C:") != -1):
            value = command.replace("C:", "").strip()
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
          time.sleep(5)

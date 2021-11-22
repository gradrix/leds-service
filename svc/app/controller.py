import os
import time
import sys
import board
from settings import Settings
from ledprogramrepository import LedProgramRepository
from neopixelwrapper import NeopixelWrapper

# -----------------------------
# Controller which changes led behavour values based on received commands
# -----------------------------
class Controller():
    def __init__(self, leds = None, settings = None):
         
        pidInt = int(os.environ.get("LED_PID", default=18))
        pid = self.getPid(pidInt)
        ledCount = int(os.environ.get("LED_COUNT", default=100))

        if (settings == None):
          self.settings = Settings()
          self.settings.ledCount = ledCount
          self.settings.openFromFile()
        else:
          self.settings = settings

        if (leds == None):
          leds = NeopixelWrapper(pid, ledCount)
        else:
          leds = leds
        self.leds = leds
        self.repo = LedProgramRepository(self.settings, leds)

    # ----------------------------
    # Get board PID by int
    # ----------------------------
    def getPid(self, pidInt):
        pid = None
        if (pidInt == 18):
            pid = board.D18
        elif (pidInt == 21):
            pid = board.D21
        else:
            raise ValueError("Incorrect PID value, only 18 and 21 are supported")

        return pid

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

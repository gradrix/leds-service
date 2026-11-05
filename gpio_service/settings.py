import os
import pickle

from gpio_service.common.brightness import migrateLinearBrightness
from gpio_service.common.ledprogrambase import SPEED_DEFAULT

STATE_FILE = os.environ.get("LEDS_STATE_FILE", "saved-data")
STATE_VERSION = 2


class Settings:

    def __init__(self):
        self.loadDefaults()

    def loadDefaults(self):
        self.brightness = 0
        self.isOn = False
        self.mode = 1
        self.speeds = {}
        self.color = ""

    @property
    def speed(self):
        return self.speeds.get(self.mode, SPEED_DEFAULT)

    @speed.setter
    def speed(self, value):
        self.speeds[self.mode] = value

    def reset(self):
        self.loadDefaults()
        self.saveToFile()

    def saveToFile(self):
        temporary = STATE_FILE + ".tmp"
        try:
            with open(temporary, "wb") as out:
                pickle.dump({
                    "version": STATE_VERSION,
                    "brightness": self.brightness,
                    "isOn": self.isOn,
                    "mode": self.mode,
                    "speeds": self.speeds,
                    "color": self.color,
                }, out, pickle.HIGHEST_PROTOCOL)
            # A power cut mid-write must not cost the saved state.
            os.replace(temporary, STATE_FILE)
        except OSError as e:
            print("Error while trying to save led settings: " + str(e))

    def openFromFile(self):
        try:
            with open(STATE_FILE, "rb") as inp:
                loaded = pickle.load(inp)
            self.brightness = loaded["brightness"]
            self.isOn = loaded["isOn"]
            self.mode = loaded["mode"]
            self.color = loaded["color"]
            if loaded.get("version") == STATE_VERSION:
                self.speeds = loaded["speeds"]
            else:
                # Version 1: linear brightness, one speed shared by programs that mostly ignored it.
                self.brightness = migrateLinearBrightness(self.brightness)
                self.speeds = {}
        except Exception as e:
            print("Error while loading saved data: " + str(e))
            self.loadDefaults()
            self.brightness = 15
            self.saveToFile()

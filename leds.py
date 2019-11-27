#!/usr/bin/python3.5

import time
import sys
import neopixel
import board
from LedPrograms.rainbow import Rainbow
from LedPrograms.colliders import Colliders
from ledsettings import LedSettings

# LED strip configuration:
LED_COUNT       = 360       # Number of LED pixels
LED_PIN         = board.D18 # GPIO pin connectedto the pixels (18 uses PWM!).

class Leds:
    """
    Class full of stuff needed to control leds through RaspberyPi
    """
    def __init__(self):
        self.settings = LedSettings(None)
        self.settings.ledCount = LED_COUNT
        self.settings.openFromFile()
        self.leds = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write=False,pixel_order=neopixel.RGB)
        self.rainbow = Rainbow(self.settings)
        self.colliders = Colliders(self.settings, self.leds)

    #Making changes
    def change(self, command):
        value = None
        #Brightness
        if (command.find("B:") != -1):
            value = command.replace("B:", "")
            self.settings.brightness = int(value)
            self.leds.brightness = self.settings.brightness * 0.01
        #Switch ON/OFF
        elif (command.find("O:") != -1):
            value = command.replace("O:", "")
            if (value == "0"):
                self.leds.brightness = 0
                self.settings.isOn = False
            else:
                self.leds.brightness = self.settings.brightness * 0.01
                self.settings.isOn = True
        #Mode
        elif (command.find("M:") != -1):
            value = command.replace("M:", "")
            self.settings.mode = int(value)
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
    
    def currentStatus(self):
        return self.settings

    def show(self):
        if (self.settings.isOn):
            mode = self.settings.mode
            self.colliders.show()
            #if (mode == 0):
            #    self.rainbow.show(self.settings)
            #elif (mode == 1):
             #    self.colliders.show(self.settings)
        else:
          time.sleep(5)

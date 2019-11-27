#!/usr/bin/python

import pickle

class LedSettings:
    
    brightness = 0
    isOn = None
    mode = 0
    toggle = 0
    speed = 0
    ledCount = 0

    def __init__(self, strip):
        self.strip = strip
    
    def saveToFile(self):
        try:
            with open("saved-data", "wb") as fi:
                settingsDict = {}
                settingsDict["brightness"] = self.brightness
                settingsDict["isOn"] = self.isOn
                settingsDict["mode"] = self.mode
                settingsDict["toggle"] = self.toggle
                settingsDict["speed"] = self.speed
                pickle.dump(settingsDict, fi, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print("Error while trying to save led settings: "+str(e))

    def openFromFile(self):
        try:
            with open("saved-data", "rb") as inp:
                loadedSettings = pickle.load(inp)
                self.brightness = loadedSettings["brightness"]
                self.isOn = loadedSettings["isOn"]
                self.mode = loadedSettings["mode"]
                self.toggle = loadedSettings["toggle"]
                self.speed = loadedSettings["speed"]
        except Exception as e:
            print("Error while loading saved data: "+str(e))
            self.brightness = 20
            self.isOn = True
            self.mode = 0
            self.toggle = 0
            self.speed = 4             
            print('Brightness: '+str(self.brightness))   

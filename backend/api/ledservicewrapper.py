import sys
import re
import os
from api.models.ledsettings import LedSettings
from api.models.modelayout import ModeLayout
from api.models.ledprogram import LedProgram
from api.commandclient import CommandClient

LED_HOST = os.environ.get("LED_SERVER_HOST")
LED_PORT = os.environ.get("LED_SERVER_PORT")

class LedServiceWrapper():

    def __init__(self, ip = LED_HOST, port = LED_PORT):
        self.cmdClient = CommandClient(ip, port)

    def getSettings(self, settingsString = None):
        res = LedSettings()
        if (settingsString == None):
            settingsData = self.cmdClient.send("ST")
        else:
            settingsData = settingsString
        
        resultArray = re.findall("(?:[a-zA-Z]*:)(?:(?!;).)*", settingsData, re.DOTALL)

        for param in resultArray:
            paramValues = param.split(":")
            key = paramValues[0]
            value = paramValues[1]

            if (key == "B"):
                res.brightness = int(value)
            elif (key == "O"):
                res.isOn = True if value == "True" else False
            elif (key == "M"):
                res.mode = int(value)
            elif (key == "T"):
                res.toggle = int(value)
            elif (key == "S"):
                res.speed = int(value)
            elif (key == "C"):
                res.color = str(value)
        return res
    
    def getModeLayout(self):
        res = ModeLayout()
        layoutData = self.cmdClient.send("LA")
        resultArray = re.findall("(?:[a-zA-Z]*:)(?:(?!;).)*", layoutData, re.DOTALL)

        for param in resultArray:
            paramValues = param.split(":")
            key = paramValues[0]
            value = paramValues[1]

            if (key == "I"):
                res.modeId = str(value)
            elif (key == "Smin"):
                res.minSpeed = int(value)
            elif (key == "Smax"):
                res.maxSpeed = int(value)
            elif (key == "M"):      
                res.modes = []          
                value = re.sub(r'(\[|\])', '', value)
                modes = value.split(",")

                for mode in modes:
                    modeValues = mode.split("=")
                    res.modes.append(LedProgram(int(modeValues[0]), str(modeValues[1])))
        return res

    def setSetting(self, setting):
        allSettings = self.cmdClient.send(setting)
        return self.getSettings(allSettings)

#!python3

import os
import time
import threading
import builtins
from controller import Controller
from commandlistener import CommandListenerServer

# -----------------------------
# Main program entry point
# -----------------------------
class LedService:

    def __init__(self, ip, port, controller = None):
        self.ip = ip
        self.port = port
        if (controller == None):
            self.controller = Controller()
        else:
            self.controller = controller

    # -----------------------------
    # Processes received commands via TCP
    # -----------------------------
    def processCommand(self, command):
        try:
            if (command == "ST"):
                return self.encodeSettings(self.controller.settings)
            elif (command == "LA"):
                return self.encodeModeLayout(self.controller.getModeLayout())
            elif (command == "RS"):
                self.controller.settings.reset()
                return "DONE"
            else: 
                return self.encodeSettings(self.controller.change(command))
        except Exception as e:
            print("processCommand error: "+str(e))

    # -----------------------------
    # Encodes leds setting object into string
    # -----------------------------
    def encodeSettings(self, settings):
        ledSettingStr = "B:"+(str(settings.brightness))+";"
        ledSettingStr += "S:"+(str(settings.speed))+";"
        ledSettingStr += "O:"+(str(settings.isOn))+";"
        ledSettingStr += "M:"+(str(settings.mode))+";"
        ledSettingStr += "T:"+(str(settings.toggle))+";"
        ledSettingStr += "C:"+(str(settings.color))+";"
        return ledSettingStr

    # -----------------------------
    # Encodes leds program layout settings object into string
    # -----------------------------
    def encodeModeLayout(self, layout):
        layoutStr = "I:"+str(layout.modeIndex)+";"
        layoutStr += "Smin:"+str(layout.minSpeed)+";"
        layoutStr += "Smax:"+str(layout.maxSpeed)+";"
        layoutStr += "M:["
        for index, mode in enumerate(layout.modes):
            if (index > 0):
                layoutStr += ","
            layoutStr += str(mode[0]) + "=" + str(mode[1])
        layoutStr += "];"
        return layoutStr

    # -----------------------------
    #  ZMQ listener object thread
    # -----------------------------
    def listener(self):
        self.cmdListener = CommandListenerServer(self.ip, self.port, self.processCommand)
        self.cmdListener.startListening()

    # -----------------------------
    #  Starts ZMQ command listener and begins led program
    # -----------------------------
    def start(self):
        thread = threading.Thread(target=self.listener, args=())
        thread.daemon = True
        thread.start()

        while True:
            self.controller.show()

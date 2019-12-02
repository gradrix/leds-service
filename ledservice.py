#!/usr/local/bin/python3.7

import threading
from controller import Controller
from commandlistener import CommandListener

class LedService:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.controller = Controller()

    def processCommand(self, command):
        if (command == "ST"):
            return self.encodeSettings(self.controller.settings)
        elif (command == "LA"):
            return self.encodeModeLayout(self.controller.getModeLayout())
        else: 
            return self.encodeSettings(self.controller.change(command))

    def encodeSettings(self, settings):
        ledSettingStr = "B:"+(str(settings.brightness))+";"
        ledSettingStr += "O:"+(str(settings.isOn))+";"
        ledSettingStr += "M:"+(str(settings.mode))+";"
        ledSettingStr += "T:"+(str(settings.toggle))+";"
        return ledSettingStr

    def encodeModeLayout(self, layout):
        layoutStr = "N:"+str(layout.modeName)+";"
        layoutStr += "I:"+str(layout.modeIndex)+";"
        layoutStr += "Smin:"+str(layout.minSpeed)+";"
        layoutStr += "Smax:"+str(layout.maxSpeed)+";"
        return layoutStr

    def listener(self):
        self.cmdListener = CommandListener(self.ip, self.port, self.processCommand)
        self.cmdListener.startListening()

    def start(self):
        #Starting TCP listener
        thread = threading.Thread(target=self.listener, args=())
        thread.daemon = True
        thread.start()

        while True:
            self.controller.show()

ledSvc = LedService("localhost", "800")
ledSvc.start()

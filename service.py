#!/usr/local/bin/python3.7

import threading
from leds import Leds
from commandlistener import CommandListener

class LedService:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.leds = Leds()

    def updateLeds(self, command):
        if (command != "ST"):
            return self.leds.change(command)
        else: 
            return self.leds.currentStatus()

    def listener(self):
        self.cmdListener = CommandListener(self.ip, self.port, self.updateLeds)
        self.cmdListener.listen()

    def start(self):
        #Starting TCP listener
        thread = threading.Thread(target=self.listener, args=())
        thread.daemon = True
        thread.start()

        while True:
            self.leds.show()

ledSvc = LedService("localhost", "8080")
ledSvc.start()

#!python3

import threading
import os
import sys
from ledservice import LedService
from controller import Controller
from settings import Settings
from tests.ledstestwrapper import LedsTestWrapper

LED_COUNT = 360

leds = LedsTestWrapper()
leds.initialize(LED_COUNT)

settings = Settings()
settings.ledCount = LED_COUNT
settings.openFromFile()
settings.isOn = True

controller = Controller(leds, settings)

ledSvc = LedService("localhost", "9001", controller)
thread = threading.Thread(target=ledSvc.start, args=())
leds.start()
thread.start()

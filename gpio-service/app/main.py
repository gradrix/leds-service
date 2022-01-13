#!python3
import os
from neopixelwrapper import NeopixelWrapper
from controller import Controller
from ledservice import LedService

#Start service
port = int(os.environ.get("LED_PORT", default=9000))
pinInt = int(os.environ.get("LED_PIN", default=18))
ledCount = int(os.environ.get("LED_COUNT", default=100))

leds = NeopixelWrapper(pinInt, ledCount)
controller = Controller(leds)
service = LedService("0.0.0.0", port, controller)
service.start()

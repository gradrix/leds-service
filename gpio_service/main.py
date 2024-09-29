#!python3
import os
from gpio_service.neopixelwrapper import NeopixelWrapper
from gpio_service.controller import Controller
from gpio_service.ledservice import LedService

#Start service
port = int(os.environ.get("LED_PORT", default=9000))
pinInt = int(os.environ.get("LED_PIN", default=18))
ledCount = int(os.environ.get("LED_COUNT", default=100))

leds = NeopixelWrapper(pinInt, ledCount)
controller = Controller(leds)
service = LedService(port, controller)
service.start()

#!python3
import os

from gpio_service.controller import Controller
from gpio_service.ledservice import LedService

port = int(os.environ.get("LED_PORT", default=9000))
pin = int(os.environ.get("LED_PIN", default=18))
ledCount = int(os.environ.get("LED_COUNT", default=360))

if os.environ.get("LED_DRIVER") == "sim":
    from gpio_service.simulatedstrip import SimulatedStrip
    driver = SimulatedStrip(ledCount)
else:
    from gpio_service.neopixelwrapper import NeopixelWrapper
    driver = NeopixelWrapper(pin, ledCount)

LedService(port, Controller(driver)).start()

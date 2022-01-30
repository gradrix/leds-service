import board
import neopixel
from common.ledsbase import LedsBase

class NeopixelWrapper(LedsBase):

  def __init__(self, pinInt, ledCount):
    pin = None
    if (pinInt == 18):
        pin = board.D18
    elif (pinInt == 21):
        pin = board.D21
    else:
        raise ValueError("Incorrect pin value, only 18 and 21 are supported")
    self.ledCount = ledCount
    print('Initializing neopixel strip on pin '+str(pinInt)+ ' with '+str(ledCount)+' leds')
    self.leds = neopixel.NeoPixel(pin, ledCount, auto_write = False, pixel_order = neopixel.RGB)

  def __getitem__(self, key):
    return self.leds[key]

  def __setitem__(self, key, value):
    self.leds[key] = value

  def clear(self, show = False):
    self.leds.fill((0, 0, 0))
    if (show):
      self.refresh()

  def refresh(self):
    self.leds.show()

  def changeBrightness(self, value):
    self.leds.brightness = value * 0.01

  def currentBrightness(self):
    return self.leds.brightness / 0.01

  def count(self):
    return self.ledCount

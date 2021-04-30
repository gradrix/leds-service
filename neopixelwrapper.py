from common.ledsbase import LedsBase
import neopixel

class NeopixelWrapper(LedsBase):

  def __init__(self, pin, ledCount):
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

  def getLength(self):
    return len(self.leds)

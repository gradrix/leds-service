from rpi_ws281x import Adafruit_NeoPixel
import _rpi_ws281x as ws
from common.ledsbase import LedsBase

# LED strip configuration:
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5           # DMA channel to use for generating signal (try 5)

class NeopixelWrapper(LedsBase):

  def __init__(self, pin, ledCount):
    channel = None
    #These PINS share PWM0
    if (pin == 12 or pin == 18 or pin == 21):
        channel = 0
    #These PINS share PWM1
    elif (pin == 13 or pin == 19):
        channel = 1
    elif (pin == 10 or pin == 21):
        print("Warning: PIN "+str(pin)+ " is not PWM PIN!")
        channel = 0
    else:
        raise ValueError("Incorrect pin value, only 10, 12, 13, 18, 19 or 21 are supported")
    self.ledCount = ledCount
    print('Initializing neopixel strip on pin '+str(pin)+ ' with '+str(ledCount)+' leds')
    self.leds = Adafruit_NeoPixel(ledCount, pin, LED_FREQ_HZ, LED_DMA, False, 5, channel, ws.WS2811_STRIP_RGB)
    self.leds.begin()

  def __getitem__(self, key):
    return self.leds.getPixelColor(key)

  def __setitem__(self, key, value):
    r, g, b = value
    self.leds.setPixelColorRGB(key, r, g, b)

  def clear(self, show = False):
    for i in range(0, self.count()):
        self.leds.setPixelColorRGB(i, 0, 0, 0)
    if (show):
      self.refresh()

  def refresh(self):
    self.leds.show()

  def changeBrightness(self, value):
    brightness = int((value * 255) / 100)
    self.leds.setBrightness(brightness)

  def currentBrightness(self):
    return int((self.leds.getBrightness() * 100) / 255)

  def count(self):
    return self.leds.numPixels()

from rpi_ws281x import Adafruit_NeoPixel
import _rpi_ws281x as ws
from gpio_service.common.ledsbase import LedsBase

LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5           # DMA channel to use for generating signal (try 5)


class NeopixelWrapper(LedsBase):

  def __init__(self, pin, ledCount):
    channel = None
    # These PINS share PWM0
    if pin in (12, 18, 21):
      channel = 0
    # These PINS share PWM1
    elif pin in (13, 19):
      channel = 1
    elif pin == 10:
      print("Warning: PIN " + str(pin) + " is not PWM PIN!")
      channel = 0
    else:
      raise ValueError("Incorrect pin value, only 10, 12, 13, 18, 19 or 21 are supported")
    self.ledCount = ledCount
    print("Initializing neopixel strip on pin " + str(pin) + " with " + str(ledCount) + " leds")
    self.leds = Adafruit_NeoPixel(ledCount, pin, LED_FREQ_HZ, LED_DMA, False, 5, channel, ws.WS2811_STRIP_RGB)
    self.leds.begin()

  def write(self, pixels, level):
    setPixel = self.leds.setPixelColorRGB
    for i in range(self.ledCount):
      offset = i * 3
      # This strip's chips read the three bytes in blue, red, green order.
      setPixel(i, pixels[offset + 2], pixels[offset], pixels[offset + 1])
    self.leds.setBrightness(level)
    self.leds.show()

  def count(self):
    return self.ledCount

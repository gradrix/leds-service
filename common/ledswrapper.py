class LedsWrapper:

  def __init__(self, leds):
    self.leds = leds

  def clear(self, show = False):
    self.leds.fill((0, 0, 0))
    if (show):
      self.refresh()

  def refresh(self):
    self.leds.show()

  def changeBrightness(self, value):
    self.leds.brightness = value * 0.01

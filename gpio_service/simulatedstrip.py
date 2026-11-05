from gpio_service.common.ledsbase import LedsBase


class SimulatedStrip(LedsBase):
  """Strip without hardware (LED_DRIVER=sim): the web mirror is the only output."""

  def __init__(self, ledCount):
    self.ledCount = ledCount

  def write(self, pixels, level):
    pass

  def count(self):
    return self.ledCount

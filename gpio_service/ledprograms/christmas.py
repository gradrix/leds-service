from common.ledprogrambase import LedProgramBase

class Christmas(LedProgramBase):

  #Constructor
  def __init__(self, settings, leds):
    super().__init__(settings, leds)
    self.initialize()
  #end

  #LedProgramBase implementation
  modeIndex = 3
  modeName = "Christmas"
  minSpeed = 0
  maxSpeed = 100

  def initialize(self):
    pass

  def show(self):
    pass
  #end
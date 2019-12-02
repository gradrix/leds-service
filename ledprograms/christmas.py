from common.ledprogrambase import LedProgramBase

class Christmas(LedProgramBase):

  #Constructor
  def __init__(self, settings, leds):
    super().__init__(settings, leds)
  #end

  #LedProgramBase implementation
  modeIndex = 2
  modeName = "Christmas"
  minSpeed = 0
  maxSpeed = 100

  def show(self):
    pass
  #end

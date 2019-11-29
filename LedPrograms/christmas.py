from LedPrograms.ledprogrambase import *

class Christmas(LedProgramBase):

  #Constructor
  def __init__(self, settings, leds):
    super().__init__(settings, leds)
  #end

  #LedProgramBase implementation
  modeIndex = 2
  modeName = "Christmas"

  def show(self, settings = None):
    pass
  #end

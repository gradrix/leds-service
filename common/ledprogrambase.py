from abc import ABC, abstractmethod, abstractproperty
from common.ledswrapper import LedsWrapper

class LedProgramBase(ABC, LedsWrapper):

  @abstractmethod
  def __init__(self, settings, leds):
    self.settings = settings
    super().__init__(leds = leds)

  @abstractproperty
  def modeIndex(self):
    pass

  @abstractproperty
  def modeName(self):
    pass  
  
  @abstractproperty
  def minSpeed(self):
    pass  
  
  @abstractproperty
  def maxSpeed(self):
    pass  
  
  @abstractmethod
  def show(self):
    pass

from abc import ABC, abstractmethod, abstractproperty
from common.ledswrapper import LedsWrapper

class LedProgramBase(ABC):

  @abstractmethod
  def __init__(self, settings, leds):
    self.settings = settings
    self.leds = leds
    super().__init__()

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

from abc import ABC, abstractmethod, abstractproperty

class LedProgramBase(ABC):

  @abstractmethod
  def __init__(self, settings, leds):
    self.settings = settings
    self.leds = leds

  @abstractproperty
  def modeIndex(self):
    pass

  @abstractproperty
  def modeName(self):
    pass  
  
  @abstractmethod
  def show(self):
    pass



from abc import ABC, abstractmethod

class LedsBase(ABC):

  @abstractmethod
  def __getitem__(self, key):
    pass

  @abstractmethod
  def __setitem__(self, key, value):
    pass

  @abstractmethod
  def clear(self, show = False):
    pass

  @abstractmethod
  def refresh(self):
    pass

  @abstractmethod
  def changeBrightness(self, value):
    pass

  @abstractmethod
  def getLength(self):
    pass

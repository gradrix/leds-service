from abc import ABC, abstractmethod

# -------------------------------------- #
# Abstract class of led control service  #
# -------------------------------------- #
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
  def count(self):
    pass

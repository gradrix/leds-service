from abc import ABC, abstractmethod


class LedsBase(ABC):
  """A strip driver. Only the render loop calls it, so drivers need no locking."""

  @abstractmethod
  def write(self, pixels, level):
    """Show pixels (bytes of r,g,b per LED) at level (0-255)."""

  @abstractmethod
  def count(self):
    pass

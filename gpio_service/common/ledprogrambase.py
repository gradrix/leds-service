from abc import ABC, abstractmethod

SPEED_DEFAULT = 50
# Speed 50 is a program's natural pace; each step of this many doubles it (0 is 1/8, 100 is 8x).
SPEED_PER_OCTAVE = 50 / 3


class LedProgramBase(ABC):
  """One effect. The render loop owns timing: render() draws a frame and must not sleep."""

  usesSpeed = True
  usesColor = False
  # Static programs are only redrawn when something changes.
  animated = True

  @abstractmethod
  def __init__(self, settings, leds):
    self.settings = settings
    self.leds = leds

  @property
  @abstractmethod
  def modeIndex(self):
    pass

  @property
  @abstractmethod
  def modeName(self):
    pass

  @abstractmethod
  def initialize(self):
    pass

  @abstractmethod
  def render(self, seconds):
    """Draw the frame that comes seconds after the previous one."""

  def colorChanged(self):
    """The chosen colour changed: repaint without restarting the animation."""

  def speedScale(self):
    return 2 ** ((self.settings.speed - SPEED_DEFAULT) / SPEED_PER_OCTAVE)

import threading
from collections import namedtuple
from contextlib import contextmanager

Frame = namedtuple("Frame", "sequence pixels level")


class FrameBus:
  """Hands the newest frame to any number of viewers; a slow viewer simply skips frames."""

  def __init__(self, onSubscribe=None):
    self.condition = threading.Condition()
    self.latest = None
    self.subscribers = 0
    self.onSubscribe = onSubscribe

  def publish(self, pixels, level):
    with self.condition:
      sequence = self.latest.sequence + 1 if self.latest else 1
      self.latest = Frame(sequence, pixels, level)
      self.condition.notify_all()

  def wait(self, afterSequence, timeout):
    """The newest frame after afterSequence, or None if none arrived within timeout."""
    with self.condition:
      self.condition.wait_for(
        lambda: self.latest is not None and self.latest.sequence > afterSequence, timeout)
      if self.latest is None or self.latest.sequence <= afterSequence:
        return None
      return self.latest

  @property
  def hasSubscribers(self):
    return self.subscribers > 0

  @contextmanager
  def subscribe(self):
    with self.condition:
      self.subscribers += 1
    if self.onSubscribe:
      self.onSubscribe()
    try:
      yield self
    finally:
      with self.condition:
        self.subscribers -= 1

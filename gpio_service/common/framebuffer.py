class FrameBuffer:
  """The frame programs draw into: true r,g,b per LED."""

  def __init__(self, ledCount):
    self.ledCount = ledCount
    self.data = bytearray(ledCount * 3)

  def __getitem__(self, index):
    offset = index * 3
    return tuple(self.data[offset:offset + 3])

  def __setitem__(self, index, rgb):
    offset = index * 3
    self.data[offset], self.data[offset + 1], self.data[offset + 2] = rgb

  def clear(self):
    self.data[:] = bytes(len(self.data))

  def fill(self, rgb):
    self.data[:] = bytes(rgb) * self.ledCount

  def count(self):
    return self.ledCount

  def snapshot(self):
    return bytes(self.data)

import datetime
import time
import sys
import threading
from common.ledsbase import LedsBase
from common.color import Color
from tests.ledLog import LedLog

class LedsTestWrapper(LedsBase):
  
  ledCount = 0
  messages = []

  def __init__(self):
    self.started = False
    self.pixels = {}

  def __getitem__(self, key):
    return self.pixel[key]

  def __setitem__(self, key, value):
    self.pixels[key] = Color(value[1], value[0], value[2])

  #Curses specific helper methods
  def start(self):
    self.started = True

  def initialize(self, ledCount):
    self.ledCount = ledCount
    self.clear()

  def clear(self, show = False):
    for i in range(self.ledCount):
      self.pixels[i] = Color(0, 0, 0)
 
    if (show):
      self.refresh()

  def refresh(self):
    self.show()

  def fill(self, tupl):
    self.clear()
    pass

  def changeBrightness(self, value):
    print('Changing brightness to '+str(value))

  def count(self):
    return self.ledCount  

  def show(self):
    if (not self.started):
        pass
    pass

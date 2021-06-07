import curses
import datetime
import time
import sys
import threading
from io import StringIO
from common.ledsbase import LedsBase
from common.color import Color
from tests.terminalColorPrinter import get_print_rgb
from tests.ledLog import LedLog

class LedsTestWrapper(LedsBase):
  
  ledCount = 0
  messages = []

  def __init__(self):
    self.started = False
    self.pixels = {}
    self.sc = curses.initscr()
    self.setStdOut()

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
    pass

  def getLength(self):
    return self.ledCount  

  def setStdOut(self):
    self.stdResult = StringIO()
    self.stdPosition = 0
    sys.stdout = self.stdResult

  def processStdOut(self, y, maxY):
    currentStreamPosition = self.stdResult.tell()

    if (self.stdPosition != currentStreamPosition):
      ledLog = LedLog(datetime.datetime.now().time(), self.stdResult.getvalue(), 0)
      self.messages.append(ledLog)
      self.setStdOut()

    #Clear messages which could not fit to the screen
    maxMessagesOnScreen = len(self.messages) - maxY - y - 2
    if (maxMessagesOnScreen > 0):
      self.messages = self.messages[maxMessagesOnScreen:]

    for index, msg in enumerate(reversed(self.messages)):
      self.sc.addstr(y + index, 0, msg.print(maxY))

  def doesFitScreen(self, maxX, maxY, amount):
    lines = (amount / (maxX + 1)) + 1
    spare = amount % (maxX + 1)
    if (lines > 1):
      lines = (lines - 1) * 2
      if (spare > 0):
        lines = lines + 1
    return lines < maxY

  def show(self):
    if (not self.started):
      return

    """Screen setup"""
    maxY, maxX = self.sc.getmaxyx()
    maxX = maxX - 2
    maxY = maxY - 1
    if (self.doesFitScreen(maxX, maxY, self.getLength() * 2)):
      strToPrint = '■ '
      strLen = 2
    else:
      strToPrint = '■'
      strLen = 1
    """End of Screen setup"""

    isReversed = False
    cornerIndex = 0
    x = 0 - strLen
    y = 0

    for index, pixel in self.pixels.items():
      newIncX = x + strLen
      newDecX = x - strLen

      if (not isReversed):
        if (x < maxX):
          x = newIncX
        else:
          if (cornerIndex < 2):
            y = y + 1
            cornerIndex = cornerIndex + 1
          else:
            isReversed = not isReversed
            cornerIndex = 0
            x = newDecX
      elif (isReversed):
        if (x > 0):
          x = newDecX
        else:
          if (cornerIndex < 2):
            y = y + 1
            cornerIndex = cornerIndex + 1
          else:
            isReversed = not isReversed
            cornerIndex = 0
            x = newIncX

      self.sc.addstr(y, x, strToPrint, curses.color_pair(get_print_rgb(pixel.r, pixel.g, pixel.b)))

    self.processStdOut(y + 1, maxY)
      # try:
      #   self.sc.addstr(y, x, strToPrint, curses.color_pair(get_print_rgb(pixel.r, pixel.g, pixel.b)))
      # except:
      #   print("EXEPT x:"+str(self.doesFitScreen(maxX, maxY, len(self.pixels))))
      #   time.sleep(10)
      #   pass

    self.sc.refresh()
    #self.sc.erase() 
    self.sc.clear()
    time.sleep(0.1)
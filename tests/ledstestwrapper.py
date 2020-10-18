import curses
import time
import sys
import threading
from common.ledsbase import LedsBase
from sty import bg, rs

LED_OFF_CHAR = '□'
LED_ON_CHAR = '■'

class LedsTestWrapper(LedsBase):
  
  ledCount = 0

  def __init__(self):
    self.started = False
    self.pixels = {}
    self.sc = curses.initscr()

  def __getitem__(self, key):
    return self.pixel[key]    

  def __setitem__(self, key, value):
    r = value[0]
    g = value[1]
    b = value[2]
    self.pixels[key] = bg(r,g,b) + LED_ON_CHAR + bg.rs

  #Curses specific helper methods
  def start(self):
    self.started = True

  def replacer(self, s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
      raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
      return newstring + s
    if index > len(s):  # add it to the end
      return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

  def initialize(self, ledCount):
    self.ledCount = ledCount
    self.clear()

  def clear(self, show = False):
    for i in range(self.ledCount):
      self.pixels[i] = bg(0,0,0) + LED_OFF_CHAR + bg.rs
 
    if (show):
      self.refresh()

  def refresh(self):
    self.show()

  def fill(self, tupl):
    self.clear()
    pass

  def getLength(self):
    return self.ledCount  

  def show(self):
    if (not self.started):
      return

    maxY, maxX = self.sc.getmaxyx()
    x = 0
    y = 1
    line = " " * maxX
    res = []
    for y in range(maxY):
      res.append(line)

    inverse = False
    newLine = False
    yChanged = False

    for i, pixel in enumerate(self.pixels):
      if (y % 2 == 0 or newLine):
        y = y + 1
        yChanged = True
        newLine = False
      elif (inverse):
        x = x - 1
      else:
        x = x + 1

      #print("TEST:"+res[y-1][x-1])
      res[y-1] = self.replacer(res[y-1], str(i), x-1)

      if not yChanged:        
        if x >= maxX - 1:
          inverse = True
          newLine = True
        elif x <= 1 and inverse:
          inverse = False
          newLine = True
      else:
        yChanged = False
    
    output = ""
    for line in res:
      output += line + '\n'

    print(output, end='\r')

    key = self.sc.getch()
    if key == ord('q'):
      sys.exit()
 
    time.sleep(0.01)

  def changeBrightness(self, value):
    pass

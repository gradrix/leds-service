#!python3

import threading
import curses
import os
import sys
from ledservice import LedService
from controller import Controller
from settings import Settings
from tests.ledstestwrapper import LedsTestWrapper

LED_COUNT = 360

def cursesWrapper(window):
    #Turn off cursor blinking
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
      curses.init_pair(i + 1, i, -1)

try:
  curses.wrapper(cursesWrapper)

  leds = LedsTestWrapper()
  leds.initialize(LED_COUNT)

  settings = Settings()
  settings.ledCount = LED_COUNT
  settings.openFromFile()
  settings.isOn = True

  controller = Controller(leds, settings)

  ledSvc = LedService("localhost", "9001", controller)
  thread = threading.Thread(target=ledSvc.start, args=())
  leds.start()
  thread.start()

except:
  curses.endwin()
  os.system('reset')
  sys.exit()

finally:
  curses.endwin()
  os.system('reset')
  sys.exit()

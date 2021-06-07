#!python3

import threading
import curses
import os
import sys
from tests.testcontroller import TestController
import builtins
builtins.IS_TEST_ENV = True
from ledservice import LedService
from tests.ledstestwrapper import LedsTestWrapper

leds = LedsTestWrapper()
controller = TestController(leds)

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
  ledSvc = LedService("localhost", "9090", controller)
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

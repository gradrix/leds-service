#!/usr/local/bin/python3.7

import threading
import curses
from tests.testcontroller import TestController
import builtins
builtins.IS_TEST_ENV = True
from ledservice import LedService
from tests.ledstestwrapper import LedsTestWrapper

leds = LedsTestWrapper()
controller = TestController(leds)

try:
  ledSvc = LedService("localhost", "1800", controller)
  thread = threading.Thread(target=ledSvc.start, args=())
  leds.start()
  thread.start()
  leds.show()

except:
  curses.nocbreak()
  curses.echo()
  curses.endwin()

finally:
  curses.endwin()

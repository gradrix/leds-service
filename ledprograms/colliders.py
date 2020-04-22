import random
import time
import datetime
from common.ledprogrambase import LedProgramBase

MIN_SIZE = 5
MAX_SIZE = 15
OBJ_AMOUNT = 15

class Colliders(LedProgramBase):
    
    #Constructor
    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.sticks = []
        for i in range(OBJ_AMOUNT):
            self.spawnSingle()
    #end

    #LedProgramBase implementition
    modeIndex = 0
    modeName = "Colliders"
    minSpeed = 0
    maxSpeed = 100

    def show(self):
        speed = (101 - self.settings.speed)
        for i, stick in enumerate(self.sticks):
            self.collisionDetection(stick, i)
            stick.step(speed)
        self.drawAll()
        self.leds.refresh()
    #end

    def isSpaceAvailable(self, startPos, endPos):
        for stick in self.sticks:
            if ((startPos >= stick.startPos or endPos >= stick.startPos)
                and (startPos <= stick.endPos or endPos <= stick.endPos)):             
                return False
        return True

    def spawnSingle(self):
        retries = 10
        spaceIsFree = False

        while (not spaceIsFree and retries > 0):
            size = random.randint(MIN_SIZE, MAX_SIZE)
            startPos = random.randint(0, self.settings.ledCount)
            spaceIsFree = self.isSpaceAvailable(startPos, startPos + size)
            if (spaceIsFree):
                stick = Stick(startPos, size, self.settings.ledCount)
                self.sticks.append(stick)
                break
            retries -= 1

    def deleteSingle(self):
        self.sticks.pop()

    def drawAll(self):
        self.leds.clear()
        for stick in self.sticks:
            for i in range(stick.startPos, stick.endPos):
                if (i < self.leds.getLength() and i >= 0):
                  self.leds[i] = stick.color.toRGB()

    def collisionDetection(self, cStick, currentIndex):
        for i, stick in enumerate(self.sticks):
            if ((i != currentIndex)
                and (((cStick.endPos >= stick.startPos and cStick.startPos < stick.startPos)
                    and ((cStick.direction and (not stick.direction
                             or (stick.direction and cStick.velocity < stick.velocity))) 
                        or (not cStick.direction and not stick.direction and cStick.velocity > stick.velocity)))
                    or ((cStick.startPos <= stick.endPos and cStick.endPos > stick.endPos)
                    and ((not cStick.direction and (stick.direction 
                            or (not stick.direction and cStick.velocity < stick.velocity)))
                        or (cStick.direction and stick.direction and cStick.velocity > stick.velocity))))):
                if (cStick.direction != stick.direction):
                    currentDirection = cStick.direction
                    cStick.direction = not currentDirection
                    stick.direction = currentDirection
                
                currentLastMov = cStick.lastMove                
                currentVelocity = cStick.velocity

                cStick.velocity = stick.velocity
                stick.velocity = currentVelocity
 
                cStick.lastMove = stick.lastMove
                stick.lastMove = currentLastMov

                #Setting random colors on impact
                stick.setRandomColor()
                cStick.setRandomColor() 
                    
class Stick:

    def __init__(self, startPos, size, ledCount):
        self.size = size
        self.ledCount = ledCount
        self.startPos = startPos
        self.endPos = self.startPos + size
        self.velocity = random.randint(1,300)
        self.direction = bool(random.getrandbits(1))
        self.lastMove = datetime.datetime.now()
        self.setRandomColor()

    def edgeDetection(self):
        if ((self.startPos <= 0 and not self.direction) or (self.endPos >= self.ledCount and self.direction)):
            self.direction = not self.direction

    def setRandomColor(self):
        self.color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def step(self,speed):
        timeDelta = datetime.datetime.now() - self.lastMove
        millSecs = int(timeDelta.total_seconds() * 1000)        
        #millSecs = int(timeDelta.total_seconds() * 1000 * speed))
        if (millSecs > self.velocity):
            self.edgeDetection()

            if (self.direction):
                self.startPos += 1
                self.endPos += 1
            else:
                self.startPos -= 1
                self.endPos -= 1
            self.lastMove = datetime.datetime.now()

class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def toRGB(self):
      return (self.r, self.g, self.b)

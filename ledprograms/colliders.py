import random
import time
import datetime
from common.color import Color
from common.ledprogrambase import LedProgramBase

MIN_SIZE = 5
MAX_SIZE = 15
OBJ_AMOUNT = 15

class Colliders(LedProgramBase):
    
    #Constructor
    def __init__(self, settings, leds):
        super().__init__(settings, leds)
        self.initialize()
    #end

    #LedProgramBase implementition
    modeIndex = 1
    modeName = "Colliders"
    minSpeed = 0
    maxSpeed = 100

    def initialize(self):
        self.sticks = []
        for i in range(OBJ_AMOUNT):
            self.spawnSingle()

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
                if (self.settings.color == ""):
                    color = Color.generateRandom()
                else:
                    color = Color.fromHex(self.settings.color)                
                stick = Stick(startPos, size, self.settings.ledCount, color)
                self.sticks.append(stick)
                break
            retries -= 1

    def deleteSingle(self):
        self.sticks.pop()

    def drawAll(self):
        self.leds.clear()
        for stick in self.sticks:
            stickRGB = stick.color.toRGB()
            for i in range(stick.startPos, stick.endPos):
                if (i < self.leds.getLength() and i >= 0):                    
                    self.leds[i] = stickRGB

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
                if (self.settings.color == ""):
                    stick.color = Color.generateRandom()
                    cStick.color = Color.generateRandom()
                    
class Stick:

    def __init__(self, startPos, size, ledCount, color):
        self.size = size
        self.ledCount = ledCount
        self.startPos = startPos
        self.endPos = self.startPos + size
        self.velocity = random.randint(1,300)
        self.direction = bool(random.getrandbits(1))
        self.lastMove = datetime.datetime.now()
        self.color = color

    def edgeDetection(self):
        if ((self.startPos <= 0 and not self.direction) or (self.endPos >= self.ledCount and self.direction)):
            self.direction = not self.direction

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
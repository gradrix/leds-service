import random

class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def toRGB(self):
        return (self.r, self.g, self.b)

    @staticmethod
    def fromHex(hexStr):
        rgbTuple = tuple(int(hexStr[i:i+2], 16) for i in (0, 2, 4))
        return Color(rgbTuple[0], rgbTuple[1], rgbTuple[2])

    @staticmethod
    def generateRandom():
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
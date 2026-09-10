import random

class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def toRGB(self):
        return (self.b, self.r, self.g)

    @staticmethod
    def fromHex(hexStr):
        if not isinstance(hexStr, str):
            return Color(255, 255, 255)
        s = hexStr.strip()
        if s.startswith('#'):
            s = s[1:]
        if len(s) != 6:
            return Color(255, 255, 255)
        for ch in s:
            if not ('0' <= ch <= '9' or 'a' <= ch <= 'f' or 'A' <= ch <= 'F'):
                return Color(255, 255, 255)
        number = int(s, 16)
        r = (number >> 16) & 255
        g = (number >> 8) & 255
        b = number & 255
        return Color(r, g, b)

    @staticmethod
    def generateRandom():
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

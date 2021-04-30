class LedLog:

    currentPosition = 0

    def __init__(self, time, message, position):
        self.time = str(time.replace(microsecond=0))
        self.message = message.strip('\n')
        self.msgLength = len(message)
        self.position = position

    def print(self, maxLen):
        msg = self.time + "> "
        realMsgLen = maxLen - len(msg) + len(self.message)
        return msg + self.message[self.position:realMsgLen] + " Rlen:" + str(realMsgLen)
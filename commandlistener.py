import sys
import asyncore
import socket
import threading
import time
import signal
import os

class CommandHandler(asyncore.dispatcher):

    def __init__(self, sock, callBack):
      super().__init__(sock)      
      self.callBack = callBack

    def handle_read(self):
        try:
            data = self.recv(100)
            if (len(data) == 0):    # EOF
                pass
            else:
                dataStr = data.decode("ascii")
                returnStr = self.callBack(dataStr)
                self.send(returnStr.encode("ascii"))
        except Exception as e:
            print("CommandHandler Error: "+str(e))
            pass

    def handle_close(self):
      self.close()

    def readable(self):
      return True

class CommandListener(asyncore.dispatcher):

    def __init__(self, host, port, callback):
        print("Starting leds-service <-s> leds-web TCP server on: "+str(host)+":"+str(port))
        self.callBack = callback
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, int(port)))
        self.listen(5)

    def handle_accept(self):
        try:
            pair = self.accept()
            if pair is not None:
                sock, addr = pair
                sock.settimeout(10)
                handler = CommandHandler(sock, self.callBack) 
        except Exception as e:
            print("CommandListener Error: "+str(e))
            pass

    def startListening(self):
        asyncore.loop(timeout = 10)

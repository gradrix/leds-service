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
                ledStatus = self.callBack(dataStr)
                ledStatusStr = "B:"+(str(ledStatus.brightness))+";"
                ledStatusStr += "O:"+(str(ledStatus.isOn))+";"
                ledStatusStr += "M:"+(str(ledStatus.mode))+";"
                ledStatusStr += "T:"+(str(ledStatus.toggle))+";"
                ledStatusStr += "S:"+(str(ledStatus.speed))+";"
                self.send(ledStatusStr.encode("ascii"))
        except Exception as e:
            print("CommandListener.CommandHandler Error: "+str(e))
            pass

    def handle_close(self):
      self.close()

    def readable(self):
      return True

class Server(asyncore.dispatcher):

    def __init__(self, host, port, callback):
        print("Starting leds-service <-> leds-web TCP server on: "+str(host)+":"+str(port))
        self.callBack = callback
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        try:
            pair = self.accept()
            if pair is not None:
                sock, addr = pair
                sock.settimeout(10)
                handler = CommandHandler(sock, self.callBack) 
        except Exception as e:
            print("CommandListener.Server Error: "+str(e))
            pass

class CommandListener:

    def __init__(self, ip, port, callBack):
        self.ip = ip
        self.port = int(port)
        self.server = Server(ip, self.port, callBack)

    def listen(self):
        asyncore.loop(timeout = 10)

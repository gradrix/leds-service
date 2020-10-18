import sys
import asyncore
import socket
import threading
import time
import signal
import os

# -----------------------------
# TCP Server to receive/send program commands
# -----------------------------
class CommandListenerTCPServer(asyncore.dispatcher):

    def __init__(self, host, port, callback):
        asyncore.dispatcher.__init__(self)
        self.callBack = callback
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, int(port)))
        self.address = self.socket.getsockname()
        print("Starting leds-service <-> leds-web TCP server on: "+str(host)+":"+str(port))
        self.listen(5)

    def handle_accept(self):
        try:
            pair = self.accept()
            if pair is not None:
                sock, addr = pair
                sock.settimeout(10)
                ClientHandler(sock, self.callBack) 
        except Exception as e:
            print("CommandListenerTCPServer Error: "+str(e))
            pass

    def startListening(self):
        asyncore.loop()

class ClientHandler(asyncore.dispatcher):

    def __init__(self, sock, callBack):
        self.callBack = callBack
        asyncore.dispatcher.__init__(self, sock)

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
            print("ClientHandler Error: "+str(e))
            pass

    def handle_close(self):
      self.close()

    def readable(self):
      return True


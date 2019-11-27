#!/usr/bin/python3.5

import sys
import asyncore
import socket
import threading
import time
import signal
import os

class DevNullHandler(asyncore.dispatcher_with_send):
    "Eat all received data"
    
    def __init__(self, sock, callBack):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.callBack = callBack

    def handle_read(self):
        try:
            data = self.recv(40)
            if (len(data) == 0):    # EOF
                pass
            else:
                dataStr = data.decode("utf-8")
                ledStatus = self.callBack(dataStr)
                ledStatusStr = "B:"+(str(ledStatus.brightness))+";"
                ledStatusStr += "O:"+(str(ledStatus.isOn))+";"
                ledStatusStr += "M:"+(str(ledStatus.mode))+";"
                ledStatusStr += "T:"+(str(ledStatus.toggle))+";"
                ledStatusStr += "S:"+(str(ledStatus.speed))+";"
                self.send(ledStatusStr.encode("utf-8"))
        except Exception as e:
            print("ComandListener error: "+str(e))
            pass

    def handle_close(self):
        self.close()

    def getData(self):
        return self.data

class Server(asyncore.dispatcher):
    handler = DevNullHandler

    def __init__(self, host, port, callBack):
        asyncore.dispatcher.__init__(self)
        self.callBack = callBack
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        try:
            pair = self.accept()
        
            if pair is not None:
                sock, addr = pair
                sock.settimeout(10)
                handler = self.handler(sock, self.callBack) 
        except Exception as e:
            print("handle_accept err... : "+str(e))
            pass

class CommandListener:

    def __init__(self, ip, port, callBack):
        self.ip = ip
        self.port = int(port)
        self.server = Server(ip, self.port, callBack)

    def listen(self):
        print("Listening on %s:%d..." % (self.ip, self.port))
        asyncore.loop(timeout = 10)

import sys
import time
import zmq

# ------------------------------------------- #
# ZMQ Server to receive/send program commands #
# ------------------------------------------- #

class CommandListenerServer():

    def __init__(self, host, port, callback):
        self.callBack = callback
        
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        connection = ("tcp://*:%s" % port)
        self.socket.bind(connection)
        
        print("Starting leds-service ZMQ server on: "+str(connection))

    def startListening(self):
        while 1:
            try:
                data = self.socket.recv().decode('ascii')
                returnStr = self.callBack(data)
                #print(str(data)+ " -> "+str(returnStr))
                self.socket.send(returnStr.encode('ascii'))
            except Exception as e:
                print("ZQM Server error: "+str(e))

import zmq
import time
import multiprocessing

class CommandClient():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        print('Initializing new gpio client with '+str(ip)+':'+str(port))

    def sendWorker(self, request, queue):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.SNDTIMEO, 1000)
        socket.setsockopt(zmq.RCVTIMEO, 1000)
        socket.setsockopt(zmq.LINGER, 0)
        target = "tcp://"+str(self.ip)+":"+str(self.port)
        socket.connect(target)

        result = queue.get()
        try:
            socket.send(request.encode('ascii'))
            result['response'] = socket.recv().decode('ascii')
            queue.put(result)
        except Exception as e:
            print('Error while sending message to '+str(target)+' -> '+str(e))
            pass
        finally:
            queue.put(result)
            context.term()

    def send(self, request, timeout=5):
        begin = time.time()
        queue = multiprocessing.Queue()
        queue.put({'response': ''})
        p = multiprocessing.Process(target=self.sendWorker, args=(request,queue,))
        p.start()

        while p.is_alive():
            if ((time.time() - begin) > timeout):
                p.terminate()
            time.sleep(0.1)
        else:
            try:            
                result = queue.get(False)
                return result['response']
            except Exception as e:
                print('ZMQ error: '+str(e))
                return ""

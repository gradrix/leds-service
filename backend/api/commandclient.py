import zmq
import time
import multiprocessing

class CommandClient():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def sendWorker(self, request, queue):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt( zmq.LINGER, 0);
        socket.connect("tcp://"+str(self.ip)+":"+str(self.port))

        result = queue.get()
        try:
            socket.send(request.encode('ascii'))
            result['response'] = socket.recv().decode('ascii')
        except Exception as e:
            print(e)
            pass
        queue.put(result)

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
            except:
                return ""

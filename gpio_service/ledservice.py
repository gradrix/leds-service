import signal
import threading
from concurrent import futures

import grpc

import gpio_api.led_service_pb2_grpc
from gpio_service.ledcontrolservicer import LedControlServicer

# Each browser watching the strip holds one worker (web_api caps viewers at MAX_VIEWERS).
GRPC_WORKERS = 10


class LedService:

    def __init__(self, port, controller):
        self.port = port
        self.controller = controller

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=GRPC_WORKERS))
        gpio_api.led_service_pb2_grpc.add_LedControlServicer_to_server(LedControlServicer(self.controller), server)

        print("Starting gRPC server on port " + str(self.port) + "...")
        server.add_insecure_port("[::]:" + str(self.port))
        server.start()

        stop = threading.Event()
        for signum in (signal.SIGTERM, signal.SIGINT):
            signal.signal(signum, lambda *_: stop.set())
        try:
            self.controller.run(stop)
        finally:
            self.controller.flush()
            server.stop(0)

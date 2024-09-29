import grpc
from concurrent import futures

import gpio_api.led_service_pb2
import gpio_api.led_service_pb2_grpc
from gpio_service.ledcontrolservicer import LedControlServicer

# -----------------------------
# Main program entry point
# -----------------------------
class LedService:

    def __init__(self, port, controller):
        self.port = port
        self.controller = controller

    # -----------------------------
    #  Starts GRPC server and begins led program
    # -----------------------------
    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
        gpio_api.led_service_pb2_grpc.add_LedControlServicer_to_server(LedControlServicer(self.controller), server)

        print("Starting gRPC server on port "+str(self.port)+"...")
        server.add_insecure_port('[::]:'+str(self.port))
        server.start()

        try:
            while True:
                self.controller.show()
        except KeyboardInterrupt:
            server.stop(0)

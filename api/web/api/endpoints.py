from flask import jsonify, request
import grpc
from google.protobuf.empty_pb2 import Empty
from gpio-service.api.led_service_pb2 import GetStatusResponse
from gpio-service.api.led_service_pb2_grpc import LedControlStub

def register_api(app):

    def call_grpc_service():
        with grpc.insecure_channel('localhost:9001') as channel:
            stub = LedControlStub(channel)
            
            request_obj = Empty()
            try:
                # Call the gRPC method
                response: GetStatusResponse = stub.GetStatus(request_obj)
                return jsonify({"status": response.status})
            except grpc.RpcError as e:
                return jsonify({"error": str(e)}), 500

    @app.route('/api/status/', methods=['GET'])
    def get_status():
        service_index = request.args.get('serviceIndex')

        res = call_grpc_service()
        print(res)
        return jsonify({"serviceIndex": service_index, "status": "Service is running!"})
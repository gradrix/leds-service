from flask import jsonify, request
import grpc
from google.protobuf.empty_pb2 import Empty
from gpio_api.led_service_pb2_grpc import LedControlStub
from gpio_api.led_service_pb2 import ChangeBrightnessRequest, ChangeModeRequest, ChangeToggleValueRequest, ChangeSpeedRequest, ChangeColorRequest, ToogleOnOffRequest

def register_api(app):

    def call_grpc_service(grpc_func):
        with grpc.insecure_channel('localhost:9001') as channel:
            # try:
            stub = LedControlStub(channel)    
            response = grpc_func(stub)
            return response
            # except grpc.RpcError as e:
            #     print(e, flush=True)
            #     return default_response

    def get_latest_status(serviceIndex):
        response = call_grpc_service(lambda rpc: rpc.GetStatus(request = Empty()))
        return jsonify({
            "isOn": response.is_on,
            "brightness": response.brightness,
            "mode": response.mode,
            "toggle": response.toggle,
            "speed": response.speed,
            "color": response.color,
            "service": serviceIndex
        })

    @app.route('/api/status/', methods=['GET'])
    def get_status():
        service_index = request.args.get('serviceIndex')
        return get_latest_status(service_index)
    
    @app.route('/api/layout/', methods=['GET'])
    def get_layout():
        service_index = request.args.get('serviceIndex')
        response = call_grpc_service(lambda rpc: rpc.GetMode(request = Empty()))
        modes_list = [{"id": mode.id, "name": mode.name} for mode in response.modes]
        return jsonify({
            "modeId": response.index,
            "minSpeed": response.min_speed,
            "maxSpeed": response.max_speed,
            "modes": modes_list
        })
    
    @app.route('/api/changestatus/', methods=['POST'])
    def change_status():
        data = request.json
        key = data.get('key')
        value = data.get('value')
        serviceIndex = data.get('serviceIndex')

        match key:
            case 'brightness':
                call_grpc_service(lambda rpc: rpc.ChangeBrightness(request = ChangeBrightnessRequest(new_brightness = value)))
            case 'mode':
                call_grpc_service(lambda rpc: rpc.ChangeMode(request = ChangeModeRequest(new_mode = value)))
            case 'toggle':
                call_grpc_service(lambda rpc: rpc.ChangeToggleValue(request = ChangeToggleValueRequest(new_toggle = value)))
            case 'speed':
                call_grpc_service(lambda rpc: rpc.ChangeSpeed(request = ChangeSpeedRequest(new_speed = value)))
            case 'color':
                call_grpc_service(lambda rpc: rpc.ChangeColor(request = ChangeColorRequest(new_color = value)))
            case 'isOn':
                call_grpc_service(lambda rpc: rpc.ToogleOnOff(request = ToogleOnOffRequest(is_on = value)))
            case _:
                raise ValueError("Invalid key")
        return get_latest_status(serviceIndex)

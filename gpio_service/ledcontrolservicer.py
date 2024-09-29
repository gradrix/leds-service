from google.protobuf.empty_pb2 import Empty

from gpio_service.controller import Controller
import gpio_api.led_service_pb2
import gpio_api.led_service_pb2_grpc

class LedControlServicer(gpio_api.led_service_pb2_grpc.LedControlServicer):
    def __init__(self, controller: Controller):
        self.controller = controller

    def GetStatus(self, request, context):
        print("GetStatus called", flush=True)

        return gpio_api.led_service_pb2.GetStatusResponse(
            brightness=self.controller.settings.brightness,
            speed=self.controller.settings.speed,
            is_on=self.controller.settings.isOn,
            mode=self.controller.settings.mode,
            toggle=self.controller.settings.toggle,
            color=self.controller.settings.color
        )

    def GetMode(self, request, context):
        layout = self.controller.repo.getModeLayout()
        modes=[gpio_api.led_service_pb2.Mode(id=mode[0], name=mode[1]) for mode in layout.modes]
        print(modes, flush=True)
        return gpio_api.led_service_pb2.GetModeResponse(
            index=layout.modeIndex,
            min_speed=layout.minSpeed,
            max_speed=layout.maxSpeed,
            modes=modes
        )

    def ResetSettings(self, request, context):
        self.controller.settings.reset()
        return Empty()

    def ToogleOnOff(self, request, context):
        self.controller.changeOnOff(request.is_on)
        return Empty()

    def ChangeBrightness(self, request, context):
        self.controller.changeBrightness(request.new_brightness)
        return Empty()

    def ChangeMode(self, request, context):
        self.controller.changeMode(request.new_mode)
        return Empty()
    
    def ChangeToggleValue(self, request, context):
        self.controller.changeToggleValue(request.new_toggle)
        return Empty()
    
    def ChangeSpeed(self, request, context):
        self.controller.changeSpeed(request.new_speed)
        return Empty()
    
    def ChangeColor(self, request, context):
        self.controller.changeColor(request.new_color)
        return Empty()
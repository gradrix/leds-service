from google.protobuf.empty_pb2 import Empty
from controller import Controller

import api.led_service_pb2
import api.led_service_pb2_grpc

class LedControlServicer(api.led_service_pb2_grpc.LedControlServicer):
    def __init__(self, controller: Controller):
        self.controller = controller

    def GetStatus(self, request, context):
        return api.led_service_pb2.GetStatusResponse(
            brightness=self.controller.settings.brightness,
            speed=self.controller.settings.speed,
            isOn=self.controller.settings.isOn,
            mode=self.controller.settings.mode,
            toggle=self.controller.settings.toggle,
            color=self.controller.settings.color
        )

    def GetMode(self, request, context):
        layout = self.controller.repo.getModeLayout()
        return api.led_service_pb2.GetModeResponse(
            name=layout.modeName,
            index=layout.modeIndex,
            minSpeed=layout.minSpeed,
            maxSpeed=layout.maxSpeed#,
            #modes=[led_service_pb2.LedMode(mode=mode[0], value=mode[1]) for mode in layout.modes]
        )

    def ResetSettings(self, request, context):
        self.controller.settings.reset()
        return Empty()

    def ToogleOnOff(self, request, context):
        self.controller.changeOnOff(request.isOn)
        return Empty()

    def ChangeBrightness(self, request, context):
        self.controller.changeBrightness(request.newBrightness)
        return Empty()

    def ChangeMode(self, request, context):
        self.controller.changeMode(request.newMode)
        return Empty()
    
    def ChangeToggleValue(self, request, context):
        self.controller.changeToggleValue(request.newToggleValue)
        return Empty()
    
    def ChangeSpeed(self, request, context):
        self.controller.changeSpeed(request.newSpeed)
        return Empty()
    
    def ChangeColor(self, request, context):
        self.controller.changeColor(request.newColor)
        return Empty()
import time

import grpc
from google.protobuf.empty_pb2 import Empty

from gpio_service.controller import Controller
import gpio_api.led_service_pb2 as pb
import gpio_api.led_service_pb2_grpc

MAX_FPS = 30
WAIT_SECONDS = 2


class LedControlServicer(gpio_api.led_service_pb2_grpc.LedControlServicer):
    def __init__(self, controller: Controller):
        self.controller = controller

    def status(self):
        settings = self.controller.settings
        return pb.GetStatusResponse(
            brightness=settings.brightness,
            speed=settings.speed,
            is_on=bool(settings.isOn),
            mode=settings.mode,
            color=settings.color,
        )

    def GetStatus(self, request, context):
        return self.status()

    def GetMode(self, request, context):
        layout = self.controller.getModeLayout()
        modes = [
            pb.Mode(id=p.modeIndex, name=p.modeName, uses_speed=p.usesSpeed, uses_color=p.usesColor)
            for p in layout.modes
        ]
        return pb.GetModeResponse(
            index=layout.modeIndex,
            min_speed=layout.minSpeed,
            max_speed=layout.maxSpeed,
            modes=modes,
        )

    def StreamFrames(self, request, context):
        fps = request.max_fps if 0 < request.max_fps <= MAX_FPS else MAX_FPS
        interval = 1 / fps
        bus = self.controller.bus
        with bus.subscribe():
            sequence = 0
            while context.is_active():
                started = time.monotonic()
                frame = bus.wait(sequence, WAIT_SECONDS)
                if frame is None:
                    continue
                sequence = frame.sequence
                yield pb.LedFrame(pixels=frame.pixels, level=frame.level, sequence=frame.sequence, status=self.status())
                time.sleep(max(0, interval - (time.monotonic() - started)))

    def ResetSettings(self, request, context):
        self.controller.resetSettings()
        return Empty()

    def ToogleOnOff(self, request, context):
        self.controller.changeOnOff(request.is_on)
        return Empty()

    def ChangeBrightness(self, request, context):
        self.controller.changeBrightness(request.new_brightness)
        return Empty()

    def ChangeMode(self, request, context):
        if not self.controller.changeMode(request.new_mode):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "unknown mode")
        return Empty()

    def ChangeSpeed(self, request, context):
        self.controller.changeSpeed(request.new_speed)
        return Empty()

    def ChangeColor(self, request, context):
        self.controller.changeColor(request.new_color)
        return Empty()

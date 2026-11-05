import base64
import json
import os
import re
import threading

from flask import Response, jsonify, request
import grpc
from google.protobuf.empty_pb2 import Empty
from gpio_api.led_service_pb2_grpc import LedControlStub
from gpio_api.led_service_pb2 import (
    ChangeBrightnessRequest, ChangeColorRequest, ChangeModeRequest, ChangeSpeedRequest,
    StreamFramesRequest, ToogleOnOffRequest,
)

GPIO_SERVICE_ADDRESS = os.environ.get("GPIO_SERVICE_ADDRESS", "localhost:9000")
RPC_TIMEOUT_SECONDS = 3
# Each viewer holds a web thread and a gRPC worker; keep spare ones for the controls.
MAX_VIEWERS = 6
DEFAULT_FPS = 30
INT32_MAX = 2**31 - 1
HEX_COLOR = re.compile(r"[0-9a-fA-F]{6}")


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def is_percent(value):
    return is_int(value) and 0 <= value <= 100


def is_mode_id(value):
    return is_int(value) and 0 <= value <= INT32_MAX


def is_color(value):
    return isinstance(value, str) and (value == "" or HEX_COLOR.fullmatch(value) is not None)


def is_bool(value):
    return isinstance(value, bool)


def status_json(response):
    return {
        "isOn": response.is_on,
        "brightness": response.brightness,
        "mode": response.mode,
        "speed": response.speed,
        "color": response.color,
    }


def sse(event, data):
    return "event: %s\ndata: %s\n\n" % (event, json.dumps(data, separators=(",", ":")))


def register_api(app):
    channels = {}
    viewers = threading.BoundedSemaphore(MAX_VIEWERS)

    def stub():
        # One channel per address and process: connecting anew per request is slow on a Pi.
        if GPIO_SERVICE_ADDRESS not in channels:
            channels[GPIO_SERVICE_ADDRESS] = grpc.insecure_channel(GPIO_SERVICE_ADDRESS)
        return LedControlStub(channels[GPIO_SERVICE_ADDRESS])

    changes = {
        "brightness": (is_percent, lambda rpc, v: rpc.ChangeBrightness(ChangeBrightnessRequest(new_brightness=v), timeout=RPC_TIMEOUT_SECONDS)),
        "mode": (is_mode_id, lambda rpc, v: rpc.ChangeMode(ChangeModeRequest(new_mode=v), timeout=RPC_TIMEOUT_SECONDS)),
        "speed": (is_percent, lambda rpc, v: rpc.ChangeSpeed(ChangeSpeedRequest(new_speed=v), timeout=RPC_TIMEOUT_SECONDS)),
        "color": (is_color, lambda rpc, v: rpc.ChangeColor(ChangeColorRequest(new_color=v), timeout=RPC_TIMEOUT_SECONDS)),
        "isOn": (is_bool, lambda rpc, v: rpc.ToogleOnOff(ToogleOnOffRequest(is_on=v), timeout=RPC_TIMEOUT_SECONDS)),
    }

    @app.errorhandler(grpc.RpcError)
    def gpio_error(error):
        if error.code() == grpc.StatusCode.INVALID_ARGUMENT:
            return jsonify({"error": error.details()}), 400
        return jsonify({"error": "gpio service unavailable"}), 503

    @app.route("/api/status/", methods=["GET"])
    def get_status():
        return jsonify(status_json(stub().GetStatus(Empty(), timeout=RPC_TIMEOUT_SECONDS)))

    @app.route("/api/layout/", methods=["GET"])
    def get_layout():
        response = stub().GetMode(Empty(), timeout=RPC_TIMEOUT_SECONDS)
        return jsonify({
            "modeId": response.index,
            "minSpeed": response.min_speed,
            "maxSpeed": response.max_speed,
            "modes": [
                {"id": m.id, "name": m.name, "usesSpeed": m.uses_speed, "usesColor": m.uses_color}
                for m in response.modes
            ],
        })

    @app.route("/api/changestatus/", methods=["POST"])
    def change_status():
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or data.get("key") not in changes:
            return jsonify({"error": "unknown key"}), 400
        valid, change = changes[data["key"]]
        if not valid(data.get("value")):
            return jsonify({"error": "invalid value"}), 400
        change(stub(), data["value"])
        return get_status()

    @app.route("/api/frames/", methods=["GET"])
    def frames():
        """Server-sent events: `status` when settings change, `frame` for each mirrored frame."""
        if not viewers.acquire(blocking=False):
            return jsonify({"error": "too many viewers"}), 503
        fps = request.args.get("fps", default=DEFAULT_FPS, type=int)
        call = stub().StreamFrames(StreamFramesRequest(max_fps=fps))

        def events():
            last = None
            yield "retry: 1500\n\n"
            try:
                for frame in call:
                    status = status_json(frame.status)
                    if status != last:
                        last = status
                        yield sse("status", status)
                    pixels = base64.b64encode(frame.pixels).decode("ascii")
                    yield sse("frame", {"pixels": pixels, "level": frame.level, "sequence": frame.sequence})
            except grpc.RpcError:
                yield sse("offline", {})

        response = Response(events(), mimetype="text/event-stream")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Accel-Buffering"] = "no"

        def finished():
            call.cancel()
            viewers.release()

        response.call_on_close(finished)
        return response

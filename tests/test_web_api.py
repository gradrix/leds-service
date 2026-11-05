"""Web API against a real gRPC server and render loop; only the strip is simulated."""
import base64
import json
import threading
from concurrent import futures

import grpc
import pytest
from flask import Flask

import gpio_api.led_service_pb2_grpc as pb_grpc
from api import endpoints
from gpio_service.controller import Controller
from gpio_service.ledcontrolservicer import LedControlServicer
from gpio_service.settings import Settings
from gpio_service.simulatedstrip import SimulatedStrip


@pytest.fixture
def stack(tmp_path, monkeypatch):
    monkeypatch.setattr("gpio_service.settings.STATE_FILE", str(tmp_path / "saved-data"))
    settings = Settings()
    settings.isOn = True
    settings.brightness = 50
    settings.mode = 1
    settings.color = "102030"
    controller = Controller(SimulatedStrip(360), settings)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_LedControlServicer_to_server(LedControlServicer(controller), server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    stop = threading.Event()
    loop = threading.Thread(target=controller.run, args=(stop,))
    loop.start()
    monkeypatch.setattr(endpoints, "GPIO_SERVICE_ADDRESS", "127.0.0.1:%d" % port)
    app = Flask(__name__)
    endpoints.register_api(app)
    yield app.test_client(), controller
    stop.set()
    controller.wake.set()
    loop.join()
    server.stop(0)


def post(client, key, value):
    return client.post("/api/changestatus/", json={"key": key, "value": value})


def read_events(response, wanted):
    """Parse SSE from a streaming response until `wanted` frame events have arrived."""
    events = []
    buffer = ""
    frames = 0
    for chunk in response.response:
        buffer += chunk.decode() if isinstance(chunk, bytes) else chunk
        while "\n\n" in buffer:
            block, buffer = buffer.split("\n\n", 1)
            fields = dict(line.split(": ", 1) for line in block.splitlines() if ": " in line)
            if "event" in fields:
                events.append((fields["event"], fields.get("data")))
                frames += fields["event"] == "frame"
        if frames >= wanted:
            break
    response.close()
    return events


def test_layout_describes_all_programs(stack):
    client, _ = stack
    layout = client.get("/api/layout/").get_json()
    assert [m["name"] for m in layout["modes"]] == ["Solid", "Colliders", "Rainbow", "Christmas", "Comet", "Aurora"]
    solid, colliders = layout["modes"][0], layout["modes"][1]
    assert solid["usesSpeed"] is False and solid["usesColor"] is True
    assert colliders["usesSpeed"] is True
    assert (layout["minSpeed"], layout["maxSpeed"]) == (0, 100)


def test_change_returns_the_new_status(stack):
    client, _ = stack
    body = post(client, "brightness", 33).get_json()
    assert body["brightness"] == 33


@pytest.mark.parametrize("key,value", [
    ("brightness", "high"),
    ("brightness", 1.5),
    ("brightness", True),
    ("speed", None),
    ("brightness", 101),
    ("brightness", -1),
    ("brightness", 4294967296),
    ("speed", 101),
    ("speed", -5),
    ("speed", 99999999999999999999),
    ("mode", 999),
    ("mode", -1),
    ("mode", 4294967296),
    ("toggle", 1),
    ("mode", "1"),
    ("isOn", 1),
    ("color", "red"),
    ("color", "12345"),
    ("nonsense", 1),
])
def test_bad_input_is_a_400_and_changes_nothing(stack, key, value):
    client, controller = stack
    response = post(client, key, value)
    assert response.status_code == 400
    assert controller.settings.brightness == 50 and controller.settings.color == "102030"
    assert controller.settings.mode == 1


def test_empty_body_is_a_400(stack):
    client, _ = stack
    assert client.post("/api/changestatus/", data="x", content_type="text/plain").status_code == 400


def test_empty_colour_means_random(stack):
    client, _ = stack
    assert post(client, "color", "").get_json()["color"] == ""


def test_frames_stream_carries_the_real_frame_and_level(stack):
    client, _ = stack
    response = client.get("/api/frames/?fps=10", buffered=False)
    assert response.mimetype == "text/event-stream"
    events = read_events(response, 1)
    status = json.loads(next(data for name, data in events if name == "status"))
    assert status["mode"] == 1
    payload = json.loads(next(data for name, data in events if name == "frame"))
    pixels = base64.b64decode(payload["pixels"])
    assert len(pixels) == 360 * 3
    assert pixels[:3] == bytes((0x10, 0x20, 0x30))
    assert payload["level"] == 64


def test_stream_pushes_status_changes_to_watchers(stack):
    client, controller = stack
    response = client.get("/api/frames/?fps=30", buffered=False)
    stream = iter(response.response)
    next(stream)
    post(client, "brightness", 80)
    response.close()
    response = client.get("/api/frames/?fps=30", buffered=False)
    events = read_events(response, 2)
    statuses = [json.loads(data) for name, data in events if name == "status"]
    assert statuses[-1]["brightness"] == 80


def test_viewer_cap_returns_503_and_a_closed_viewer_frees_its_slot(stack, monkeypatch):
    client, _ = stack
    held = [client.get("/api/frames/", buffered=False) for _ in range(endpoints.MAX_VIEWERS)]
    assert client.get("/api/frames/", buffered=False).status_code == 503
    held.pop().close()
    response = client.get("/api/frames/", buffered=False)
    assert response.status_code == 200
    for item in held + [response]:
        item.close()


def test_gpio_service_down_is_a_503_not_a_traceback(monkeypatch):
    monkeypatch.setattr(endpoints, "GPIO_SERVICE_ADDRESS", "127.0.0.1:1")
    monkeypatch.setattr(endpoints, "RPC_TIMEOUT_SECONDS", 0.2)
    app = Flask(__name__)
    endpoints.register_api(app)
    client = app.test_client()
    assert client.get("/api/status/").status_code == 503
    assert post(client, "brightness", 10).status_code == 503

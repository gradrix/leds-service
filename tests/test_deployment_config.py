import importlib
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]


def _load_endpoints():
    sys.path.insert(0, str(ROOT / "web_api"))
    sys.path.insert(0, str(ROOT))
    import api.endpoints as endpoints
    return importlib.reload(endpoints)


def test_web_api_dials_gpio_service_address_from_environment():
    with patch.dict(os.environ, {"GPIO_SERVICE_ADDRESS": "gpio:9000"}):
        endpoints = _load_endpoints()
    from flask import Flask

    app = Flask(__name__)
    endpoints.register_api(app)
    status = MagicMock(is_on=True, brightness=2, mode=1, speed=4, color="")
    stub = MagicMock()
    stub.GetStatus.return_value = status
    with patch.object(endpoints.grpc, "insecure_channel") as channel, \
         patch.object(endpoints, "LedControlStub", return_value=stub):
        response = app.test_client().get("/api/status/?serviceIndex=1")

    assert response.status_code == 200
    channel.assert_called_once_with("gpio:9000")


def test_web_api_defaults_to_local_gpio_service():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("GPIO_SERVICE_ADDRESS", None)
        endpoints = _load_endpoints()
    assert endpoints.GPIO_SERVICE_ADDRESS == "localhost:9000"


def test_settings_persist_to_configured_state_file(tmp_path):
    state_file = tmp_path / "state" / "saved-data"
    state_file.parent.mkdir()
    sys.path.insert(0, str(ROOT))
    with patch.dict(os.environ, {"LEDS_STATE_FILE": str(state_file)}):
        import gpio_service.settings as settings_module
        settings_module = importlib.reload(settings_module)
        settings = settings_module.Settings()
        settings.brightness = 7
        settings.saveToFile()

        restored = settings_module.Settings()
        restored.openFromFile()

    assert state_file.exists()
    assert restored.brightness == 7


def test_web_image_uses_threads_so_viewers_do_not_block_the_controls():
    dockerfile = (ROOT / "docker" / "web_api" / "Dockerfile").read_text()
    assert '"gthread"' in dockerfile
    threads = int(dockerfile.split('"--threads", "')[1].split('"')[0])
    from api.endpoints import MAX_VIEWERS
    assert threads > MAX_VIEWERS


def test_grpc_pool_outnumbers_viewers():
    from api.endpoints import MAX_VIEWERS
    from gpio_service.ledservice import GRPC_WORKERS
    assert GRPC_WORKERS > MAX_VIEWERS

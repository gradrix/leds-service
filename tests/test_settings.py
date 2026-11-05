import pickle

from gpio_service import settings as settings_module
from gpio_service.common.brightness import brightnessLevel


def load(path, monkeypatch):
    monkeypatch.setattr(settings_module, "STATE_FILE", str(path))
    settings = settings_module.Settings()
    settings.openFromFile()
    return settings


def test_legacy_state_keeps_the_same_physical_brightness_and_stays_off(tmp_path, monkeypatch):
    path = tmp_path / "saved-data"
    legacy = {"brightness": 18, "isOn": False, "mode": 2, "toggle": 0, "speed": 4, "color": ""}
    path.write_bytes(pickle.dumps(legacy))
    settings = load(path, monkeypatch)
    assert settings.isOn is False
    assert settings.mode == 2
    assert abs(brightnessLevel(settings.brightness) - int(18 * 255 / 100)) <= 2
    # Speed never did anything in Colliders, so the old 4 must not make it crawl.
    assert settings.speed == 50


def test_new_state_round_trips_without_migrating_twice(tmp_path, monkeypatch):
    path = tmp_path / "saved-data"
    monkeypatch.setattr(settings_module, "STATE_FILE", str(path))
    settings = settings_module.Settings()
    settings.brightness = 42
    settings.isOn = True
    settings.mode = 3
    settings.speed = 77
    settings.saveToFile()
    restored = load(path, monkeypatch)
    assert (restored.brightness, restored.mode, restored.speed) == (42, 3, 77)
    assert list(tmp_path.iterdir()) == [path]


def test_corrupt_state_falls_back_to_dim_and_dark(tmp_path, monkeypatch):
    # The strip is in a bedroom: losing the state must not light it at night.
    path = tmp_path / "saved-data"
    path.write_bytes(b"not a pickle")
    settings = load(path, monkeypatch)
    assert settings.mode == 1 and settings.brightness > 0
    assert settings.isOn is False


def test_brightness_curve():
    assert brightnessLevel(0) == 0
    assert brightnessLevel(1) >= 1
    assert brightnessLevel(100) == 255
    levels = [brightnessLevel(v) for v in range(101)]
    assert levels == sorted(levels)
    # Half the slider is a quarter of the power: fine control where a dim room needs it.
    assert 60 <= brightnessLevel(50) <= 68

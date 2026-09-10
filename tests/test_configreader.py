import pytest

from web_api.config.configreader import ConfigReader, GpioService


def _reset():
    ConfigReader.configs = []


def test_whitespace_around_keys_and_values():
    _reset()
    ConfigReader.initConfigs("  pin = 18 , port = 9000 , ledCount = 10 ")
    assert len(ConfigReader.configs) == 1
    svc = ConfigReader.configs[0]
    assert svc.pin == "18"
    assert svc.port == "9000"
    assert svc.ledCount == "10"


def test_empty_or_incomplete_required_fields_skipped():
    _reset()
    # First entry missing ledCount, second entry has empty pin value.
    ConfigReader.initConfigs(
        "pin=18,port=9000:pin=,port=9000,ledCount=10"
    )
    # Both entries are incomplete; no valid service should be produced.
    # The default fallback should kick in.
    assert len(ConfigReader.configs) == 1
    svc = ConfigReader.configs[0]
    assert svc.pin == "18"
    assert svc.port == "9000"
    assert svc.ledCount == "10"


def test_multiple_services_preserve_order_skip_incomplete():
    _reset()
    ConfigReader.initConfigs(
        "pin=1,port=2,ledCount=3:pin=,port=4,ledCount=5:pin=6,port=7,ledCount=8"
    )
    assert len(ConfigReader.configs) == 2
    assert ConfigReader.configs[0].pin == "1"
    assert ConfigReader.configs[0].port == "2"
    assert ConfigReader.configs[0].ledCount == "3"
    assert ConfigReader.configs[1].pin == "6"
    assert ConfigReader.configs[1].port == "7"
    assert ConfigReader.configs[1].ledCount == "8"


def test_defaults_and_repeated_parsing_replaces_prior_state():
    _reset()
    # First parse: empty config triggers default.
    ConfigReader.initConfigs("")
    assert len(ConfigReader.configs) == 1
    assert ConfigReader.configs[0].pin == "18"
    assert ConfigReader.configs[0].port == "9000"
    assert ConfigReader.configs[0].ledCount == "10"

    # Second parse replaces prior state entirely.
    ConfigReader.initConfigs("pin=20,port=8000,ledCount=5")
    assert len(ConfigReader.configs) == 1
    assert ConfigReader.configs[0].pin == "20"
    assert ConfigReader.configs[0].port == "8000"
    assert ConfigReader.configs[0].ledCount == "5"


def test_whitespace_incomplete_entry_not_selected():
    _reset()
    # Entry with whitespace-only values should be treated as incomplete.
    ConfigReader.initConfigs("pin=  ,port=  ,ledCount=  ")
    assert len(ConfigReader.configs) == 1
    svc = ConfigReader.configs[0]
    assert svc.pin == "18"
    assert svc.port == "9000"
    assert svc.ledCount == "10"


def test_whitespace_key_not_fallback():
    _reset()
    # A key with surrounding whitespace must be recognized, not dropped.
    # If the parser trims keys and the value is non-default, the result
    # must reflect the configured values, not the default fallback.
    ConfigReader.initConfigs("  pin = 20 , port = 8000 , ledCount = 5 ")
    assert len(ConfigReader.configs) == 1
    svc = ConfigReader.configs[0]
    assert svc.pin == "20"
    assert svc.port == "8000"
    assert svc.ledCount == "5"

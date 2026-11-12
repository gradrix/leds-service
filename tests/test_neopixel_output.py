"""The strip gets each pixel's true r,g,b in the green, red, blue byte order its WS2812 chips read."""
import sys
import types
from unittest.mock import MagicMock

STRIP_RGB, STRIP_GRB = 0x100800, 0x081000


def make_wrapper(monkeypatch):
    neopixel = MagicMock()
    module = types.ModuleType("rpi_ws281x")
    module.Adafruit_NeoPixel = MagicMock(return_value=neopixel)
    low = types.ModuleType("_rpi_ws281x")
    low.WS2811_STRIP_RGB = STRIP_RGB
    low.WS2811_STRIP_GRB = STRIP_GRB
    monkeypatch.setitem(sys.modules, "rpi_ws281x", module)
    monkeypatch.setitem(sys.modules, "_rpi_ws281x", low)
    sys.modules.pop("gpio_service.neopixelwrapper", None)
    from gpio_service.neopixelwrapper import NeopixelWrapper
    return NeopixelWrapper(18, 2), module.Adafruit_NeoPixel, neopixel


def test_the_library_orders_bytes_for_grb_chips(monkeypatch):
    _, constructor, _ = make_wrapper(monkeypatch)
    # Sending blue, red, green to these chips showed green as blue and blue as green.
    assert constructor.call_args.args[7] == STRIP_GRB


def test_write_passes_true_rgb_and_applies_brightness(monkeypatch):
    wrapper, _, neopixel = make_wrapper(monkeypatch)
    wrapper.write(bytes((10, 20, 30, 40, 50, 60)), 99)
    assert [c.args for c in neopixel.setPixelColorRGB.call_args_list] == [(0, 10, 20, 30), (1, 40, 50, 60)]
    neopixel.setBrightness.assert_called_once_with(99)
    neopixel.show.assert_called_once_with()

"""The physical strip must get exactly the bytes it got before the render-loop rewrite."""
import sys
import types
from unittest.mock import MagicMock


def make_wrapper(monkeypatch):
    neopixel = MagicMock()
    neopixel.numPixels.return_value = 2
    module = types.ModuleType("rpi_ws281x")
    module.Adafruit_NeoPixel = MagicMock(return_value=neopixel)
    low = types.ModuleType("_rpi_ws281x")
    low.WS2811_STRIP_RGB = 0
    monkeypatch.setitem(sys.modules, "rpi_ws281x", module)
    monkeypatch.setitem(sys.modules, "_rpi_ws281x", low)
    sys.modules.pop("gpio_service.neopixelwrapper", None)
    from gpio_service.neopixelwrapper import NeopixelWrapper
    return NeopixelWrapper(18, 2), neopixel


def test_write_keeps_the_strip_channel_order_and_applies_brightness(monkeypatch):
    wrapper, neopixel = make_wrapper(monkeypatch)
    wrapper.write(bytes((10, 20, 30, 40, 50, 60)), 99)
    # The old code passed Color.toRGB() == (b, r, g) to setPixelColorRGB.
    assert [c.args for c in neopixel.setPixelColorRGB.call_args_list] == [(0, 30, 10, 20), (1, 60, 40, 50)]
    neopixel.setBrightness.assert_called_once_with(99)
    neopixel.show.assert_called_once_with()

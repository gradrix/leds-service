BRIGHTNESS_MAX = 100
LEVEL_MAX = 255


def brightnessLevel(percent):
    """Slider percent to the strip's 0-255 level.

    The eye is far more sensitive to dim light, so the slider is squared: half way is a
    quarter of the power and the lower half stays usable. Anything above 0 stays visible.
    """
    if percent <= 0:
        return 0
    return max(1, round(LEVEL_MAX * (percent / BRIGHTNESS_MAX) ** 2))


def migrateLinearBrightness(percent):
    """Stored value from the old linear slider that gives the same physical brightness."""
    return round(BRIGHTNESS_MAX * (percent / BRIGHTNESS_MAX) ** 0.5)

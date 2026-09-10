import pytest
from gpio_service.common.color import Color


def test_bare_hex_non_default():
    c = Color.fromHex("ff0000")
    assert c.r == 255
    assert c.g == 0
    assert c.b == 0


def test_hash_prefixed_non_default():
    c = Color.fromHex("#00ff00")
    assert c.r == 0
    assert c.g == 255
    assert c.b == 0


def test_mixed_case():
    c = Color.fromHex("#AbCdEf")
    assert c.r == 0xAB
    assert c.g == 0xCD
    assert c.b == 0xEF


def test_whitespace():
    c = Color.fromHex("  #123456  ")
    assert c.r == 0x12
    assert c.g == 0x34
    assert c.b == 0x56


def test_malformed_length():
    c = Color.fromHex("#12345")
    assert c.r == 255
    assert c.g == 255
    assert c.b == 255


def test_trailing_data():
    c = Color.fromHex("#12345678")
    assert c.r == 255
    assert c.g == 255
    assert c.b == 255


def test_invalid_characters():
    c = Color.fromHex("#12345G")
    assert c.r == 255
    assert c.g == 255
    assert c.b == 255


def test_non_string():
    c = Color.fromHex(123456)
    assert c.r == 255
    assert c.g == 255
    assert c.b == 255


def test_fresh_fallback_objects():
    c1 = Color.fromHex("#12345")
    c2 = Color.fromHex("#12345")
    assert c1 is not c2
    assert c1.r == 255
    assert c1.g == 255
    assert c1.b == 255


def test_existing_channel_order():
    c = Color(10, 20, 30)
    assert c.r == 10
    assert c.g == 20
    assert c.b == 30
    assert c.toRGB() == (30, 10, 20)


def test_generate_random():
    c = Color.generateRandom()
    assert isinstance(c, Color)
    assert 0 <= c.r <= 255
    assert 0 <= c.g <= 255
    assert 0 <= c.b <= 255

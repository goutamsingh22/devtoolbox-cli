from __future__ import annotations

import pytest

from devtoolbox import color


def test_hex_to_rgb() -> None:
    assert color.hex_to_rgb("#ff0000") == (255, 0, 0)
    assert color.hex_to_rgb("fff") == (255, 255, 255)
    assert color.hex_to_rgb("#00FF00") == (0, 255, 0)


def test_rgb_to_hex() -> None:
    assert color.rgb_to_hex((255, 0, 0)) == "#ff0000"
    assert color.rgb_to_hex((0, 128, 255)) == "#0080ff"


def test_rgb_to_hsl() -> None:
    hue, saturation, lightness = color.rgb_to_hsl((255, 0, 0))
    assert hue == pytest.approx(0)
    assert saturation == pytest.approx(100)
    assert lightness == pytest.approx(50)


def test_hsl_to_rgb_round_trip() -> None:
    for rgb in [(255, 0, 0), (0, 255, 0), (0, 0, 255), (18, 52, 86), (255, 255, 255)]:
        assert color.hsl_to_rgb(color.rgb_to_hsl(rgb)) == rgb


def test_inspect_hex() -> None:
    info = color.inspect("#3498db")
    assert info["hex"] == "#3498db"
    assert info["rgb"] == [52, 152, 219]
    hue, saturation, lightness = info["hsl"]
    assert 190 <= hue <= 220
    assert 50 <= saturation <= 80
    assert 40 <= lightness <= 70


def test_inspect_rgb_text() -> None:
    assert color.inspect("rgb(255, 0, 0)")["hex"] == "#ff0000"


def test_invalid_hex() -> None:
    with pytest.raises(ValueError, match="invalid hex"):
        color.hex_to_rgb("#12")


def test_invalid_rgb_text() -> None:
    with pytest.raises(ValueError, match="invalid rgb"):
        color.rgb_from_text("rgb(1, 2)")


def test_rgb_channel_range() -> None:
    with pytest.raises(ValueError, match="out of range"):
        color.rgb_to_hex((256, 0, 0))

"""Tests für src.utils.image_utils."""
import numpy as np

from src.utils.image_utils import bgr_to_rgb, bytes_to_bgr, frame_to_bytes


def test_frame_to_bytes_returns_nonempty_jpeg():
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    data = frame_to_bytes(frame)

    assert isinstance(data, bytes)
    assert len(data) > 0
    # JPEG-Dateien beginnen mit dem SOI-Marker 0xFFD8
    assert data[:2] == b"\xff\xd8"


def test_bgr_to_rgb_swaps_channels():
    frame = np.zeros((2, 2, 3), dtype=np.uint8)
    frame[:, :, 0] = 10   # Blau-Kanal (BGR)
    frame[:, :, 2] = 200  # Rot-Kanal (BGR)

    rgb = bgr_to_rgb(frame)

    assert rgb[0, 0, 0] == 200  # jetzt Rot-Kanal an Position 0
    assert rgb[0, 0, 2] == 10   # jetzt Blau-Kanal an Position 2


def test_bytes_to_bgr_roundtrip():
    original = np.full((20, 20, 3), 128, dtype=np.uint8)
    encoded = frame_to_bytes(original)

    decoded = bytes_to_bgr(encoded)

    assert decoded.shape == original.shape
    # JPEG ist verlustbehaftet, daher nur ungefährer Wertevergleich
    assert abs(int(decoded[0, 0, 0]) - 128) < 10

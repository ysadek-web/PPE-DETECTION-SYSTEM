"""Tests für src.detection.draw_boxes und src.detection.detector."""
from unittest.mock import MagicMock

import numpy as np

from src.detection.detector import PPEDetector
from src.detection.draw_boxes import count_persons, draw_boxes
from src.utils.constants import CLASS_NAMES


def _make_box(class_name: str, xyxy=(5, 5, 20, 20), conf=0.9):
    """Baut ein Mock-Objekt, das sich wie eine YOLO-Box verhält."""
    box = MagicMock()
    box.cls = [CLASS_NAMES.index(class_name)]
    box.xyxy = [xyxy]
    box.conf = [conf]
    return box


def test_draw_boxes_flags_missing_items():
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    boxes = [_make_box("no helmet"), _make_box("vest")]

    _, missing = draw_boxes(frame, boxes)

    assert missing == ["no helmet"]


def test_draw_boxes_returns_frame_of_same_shape():
    frame = np.zeros((50, 50, 3), dtype=np.uint8)
    boxes = [_make_box("person")]

    annotated, _ = draw_boxes(frame, boxes)

    assert annotated.shape == frame.shape


def test_count_persons():
    boxes = [_make_box("person"), _make_box("person"), _make_box("helmet")]
    assert count_persons(boxes) == 2


def test_ppe_detector_annotate_aggregates_across_results():
    frame = np.zeros((60, 60, 3), dtype=np.uint8)

    fake_result_1 = MagicMock(boxes=[_make_box("no vest"), _make_box("person")])
    fake_result_2 = MagicMock(boxes=[_make_box("person")])

    detector = PPEDetector(model=MagicMock(), conf_threshold=0.4)
    annotated, missing, persons = detector.annotate(frame, [fake_result_1, fake_result_2])

    assert missing == ["no vest"]
    assert persons == 2
    assert annotated.shape == frame.shape


def test_ppe_detector_detect_frame_combines_run_and_annotate():
    frame = np.zeros((40, 40, 3), dtype=np.uint8)
    fake_result = MagicMock(boxes=[_make_box("no helmet")])
    mock_model = MagicMock(return_value=[fake_result])

    detector = PPEDetector(model=mock_model, conf_threshold=0.5)
    annotated, missing, persons = detector.detect_frame(frame)

    mock_model.assert_called_once_with(frame, conf=0.5, verbose=False)
    assert missing == ["no helmet"]
    assert persons == 0
    assert annotated.shape == frame.shape

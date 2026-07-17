"""Zeichnen von Bounding-Boxes und Extraktion fehlender PSA-Klassen."""
import cv2
import numpy as np

from src.utils.constants import CLASS_COLORS_BGR, CLASS_NAMES, MISSING_ITEMS


def draw_boxes(frame: np.ndarray, boxes) -> tuple[np.ndarray, list[str]]:
    """Zeichnet Bounding-Boxes auf den Frame und gibt die Liste erkannter
    fehlender Ausrüstungsklassen zurück.
    """
    detected_missing = []
    for box in boxes:
        cls_id = int(box.cls[0])
        name = CLASS_NAMES[cls_id].lower()
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        color = CLASS_COLORS_BGR.get(name, (255, 255, 255))

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        label = f"{name} {conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        if name in MISSING_ITEMS:
            detected_missing.append(name)

    return frame, detected_missing


def count_persons(boxes) -> int:
    """Zählt, wie viele 'person'-Boxen in einer YOLO-Box-Liste enthalten sind."""
    return sum(
        1 for box in boxes
        if CLASS_NAMES[int(box.cls[0])].lower() == "person"
    )

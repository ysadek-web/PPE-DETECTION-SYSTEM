"""Gemeinsame Erkennungslogik: kapselt YOLO-Modell-Inferenz und Annotation."""
import numpy as np

from src.detection.draw_boxes import count_persons, draw_boxes


class PPEDetector:
    """Kapselt ein geladenes YOLO-Modell für Inferenz + Annotation auf Frames."""

    def __init__(self, model, conf_threshold: float = 0.4):
        self.model = model
        self.conf_threshold = conf_threshold

    def run(self, frame: np.ndarray):
        """Führt reine YOLO-Inferenz aus und gibt die Rohergebnisse zurück."""
        return self.model(frame, conf=self.conf_threshold, verbose=False)

    def annotate(self, frame: np.ndarray, results) -> tuple[np.ndarray, list[str], int]:
        """Zeichnet alle Boxen der Ergebnisse in den Frame.

        Returns:
            annotierter_frame, fehlende_klassen, anzahl_erkannter_personen
        """
        all_missing: list[str] = []
        person_count = 0
        for result in results:
            frame, missing = draw_boxes(frame, result.boxes)
            all_missing.extend(missing)
            person_count += count_persons(result.boxes)
        return frame, all_missing, person_count

    def detect_frame(self, frame: np.ndarray) -> tuple[np.ndarray, list[str], int]:
        """Komfortmethode: führt Inferenz und Annotation in einem Schritt aus."""
        results = self.run(frame)
        return self.annotate(frame, results)

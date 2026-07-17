"""Erkennungs-Workflow für Einzelbilder (Upload-Tab & Kamera-Tab)."""
import numpy as np

from src.detection.detector import PPEDetector


def detect_image(model, frame: np.ndarray, conf_threshold: float = 0.4) -> tuple[np.ndarray, list[str]]:
    """Führt PSA-Erkennung auf einem einzelnen BGR-Frame aus.

    Returns:
        annotierter_frame, liste_der_fehlenden_ausruestungsklassen
    """
    detector = PPEDetector(model, conf_threshold)
    annotated, missing, _ = detector.detect_frame(frame.copy())
    return annotated, missing

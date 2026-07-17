"""Hilfsfunktionen für Bild-/Frame-Konvertierung."""
import cv2
import numpy as np


def frame_to_bytes(frame: np.ndarray, ext: str = ".jpg") -> bytes:
    """Kodiert einen BGR-Frame (np.ndarray) als Bilddatei-Bytes."""
    success, buffer = cv2.imencode(ext, frame)
    if not success:
        raise ValueError("Frame konnte nicht kodiert werden.")
    return buffer.tobytes()


def bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    """Konvertiert einen BGR-Frame (OpenCV) in RGB (für Anzeige mit Streamlit)."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def bytes_to_bgr(data: bytes) -> np.ndarray:
    """Dekodiert Bild-Bytes (z. B. aus einem Streamlit-Uploader) zu einem BGR-Frame."""
    file_bytes = np.frombuffer(data, np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

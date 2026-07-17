"""Datei-Hilfsfunktionen: temporäre Dateien, Output-Speicherung, Aufräumen."""
import os
import shutil
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

from src.utils.config import OUTPUT_ALERTS_DIR, OUTPUT_IMAGES_DIR, OUTPUT_VIDEOS_DIR


def _timestamped_name(prefix: str, ext: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:6]}{ext}"


def save_temp_upload(data: bytes, suffix: str = ".mp4") -> str:
    """Schreibt hochgeladene Bytes in eine temporäre Datei und gibt den Pfad zurück."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        return tmp.name


def cleanup_temp_file(path: str) -> None:
    """Löscht eine temporäre Datei, falls sie existiert (Fehler werden ignoriert)."""
    try:
        if path and os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass


def save_output_image(image_bytes: bytes, prefix: str = "image") -> Path:
    """Speichert annotierte Bild-Bytes unter outputs/images/ und gibt den Pfad zurück."""
    out_path = OUTPUT_IMAGES_DIR / _timestamped_name(prefix, ".jpg")
    out_path.write_bytes(image_bytes)
    return out_path


def save_output_video(temp_path: str, prefix: str = "video") -> Path:
    """Verschiebt eine annotierte Video-Datei nach outputs/videos/.

    Nutzt shutil.move statt os.replace, da temp_path und das Zielverzeichnis
    (z. B. in Docker durch ein gemountetes Volume) auf unterschiedlichen
    Dateisystemen liegen können und os.replace dann fehlschlagen würde.
    """
    out_path = OUTPUT_VIDEOS_DIR / _timestamped_name(prefix, ".mp4")
    shutil.move(temp_path, str(out_path))
    return out_path


def save_alert_snapshot(image_bytes: bytes) -> Path:
    """Speichert einen Schnappschuss eines Verstoßes unter outputs/alerts/ (Audit-Trail)."""
    out_path = OUTPUT_ALERTS_DIR / _timestamped_name("alert", ".jpg")
    out_path.write_bytes(image_bytes)
    return out_path

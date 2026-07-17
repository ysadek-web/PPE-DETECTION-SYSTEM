"""Erkennungs-Workflow für Videos: Frame-für-Frame-Analyse mit Fortschritts-Callback."""
from dataclasses import dataclass
from typing import Callable, Optional

import cv2
import numpy as np

from src.detection.detector import PPEDetector


@dataclass
class VideoAnalysisResult:
    """Ergebnis einer vollständigen Video-Analyse."""
    output_path: str
    total_frames: int
    total_persons: int
    total_violations: int
    unique_missing_items: set


def process_video(
    model,
    input_path: str,
    output_path: str,
    conf_threshold: float = 0.4,
    skip_frames: int = 2,
    on_progress: Optional[Callable[[int, int, np.ndarray], None]] = None,
) -> VideoAnalysisResult:
    """Analysiert ein Video Frame für Frame und schreibt die annotierte Version
    nach `output_path`.

    `on_progress`, falls gesetzt, wird nach jedem Frame mit
    (frame_idx, total_frames, frame) aufgerufen -- z. B. um eine
    Streamlit-Fortschrittsanzeige zu aktualisieren.
    """
    detector = PPEDetector(model, conf_threshold)

    cap = cv2.VideoCapture(input_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    total_violations = 0
    total_persons = 0
    unique_missing: set = set()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % skip_frames == 0:
                frame, missing, persons = detector.detect_frame(frame)
                total_violations += len(missing)
                total_persons += persons
                unique_missing.update(missing)

            writer.write(frame)

            if on_progress is not None:
                on_progress(frame_idx, total_frames, frame)

            frame_idx += 1
    finally:
        cap.release()
        writer.release()

    return VideoAnalysisResult(
        output_path=output_path,
        total_frames=frame_idx,
        total_persons=total_persons,
        total_violations=total_violations,
        unique_missing_items=unique_missing,
    )

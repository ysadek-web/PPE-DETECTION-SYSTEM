"""Laden und Verwalten des YOLO-Modells."""
from pathlib import Path

import streamlit as st
from ultralytics import YOLO


@st.cache_resource(show_spinner=False)
def load_model(path: str) -> YOLO:
    """Lädt ein YOLO-Modell vom angegebenen Pfad und cached es über Reruns hinweg."""
    return YOLO(path)


def model_path_exists(path: str) -> bool:
    """Prüft, ob unter dem angegebenen Pfad eine Modell-Datei existiert."""
    return bool(path) and Path(path).exists()

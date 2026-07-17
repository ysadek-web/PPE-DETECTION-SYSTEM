"""Zentrale Konfiguration: Umgebungsvariablen, Pfade, Session-State-Defaults, Logging."""
import logging
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ─── Pfade ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[2]  # Projekt-Root

load_dotenv(BASE_DIR / ".env")

WEIGHTS_DIR = BASE_DIR / "weights"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUT_IMAGES_DIR = OUTPUTS_DIR / "images"
OUTPUT_VIDEOS_DIR = OUTPUTS_DIR / "videos"
OUTPUT_ALERTS_DIR = OUTPUTS_DIR / "alerts"
LOGS_DIR = BASE_DIR / "logs"
DATA_INPUT_DIR = BASE_DIR / "data" / "input"

for _dir in (OUTPUT_IMAGES_DIR, OUTPUT_VIDEOS_DIR, OUTPUT_ALERTS_DIR, LOGS_DIR, DATA_INPUT_DIR, WEIGHTS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ─── Defaults aus Umgebungsvariablen (.env) ────────────────────────────────
DEFAULT_MODEL_PATH = os.getenv("MODEL_PATH", str(WEIGHTS_DIR / "best.pt"))
DEFAULT_EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
DEFAULT_EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")
DEFAULT_EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
DEFAULT_EMAIL_COOLDOWN = int(os.getenv("EMAIL_COOLDOWN", "30"))
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

SESSION_STATE_DEFAULTS = {
    "model": None,
    "model_path": DEFAULT_MODEL_PATH,
    "email_sender": DEFAULT_EMAIL_SENDER,
    "email_receiver": DEFAULT_EMAIL_RECEIVER,
    "email_password": DEFAULT_EMAIL_PASSWORD,
    "send_email_flag": True,
    "last_email_time": 0,
    "email_cooldown": DEFAULT_EMAIL_COOLDOWN,
}


def init_session_state() -> None:
    """Initialisiert alle benötigten Felder in st.session_state, falls noch nicht vorhanden."""
    for key, default in SESSION_STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def setup_logging() -> logging.Logger:
    """Konfiguriert Logging in logs/app.log sowie auf die Konsole."""
    logger = logging.getLogger("ppe_detection")
    if logger.handlers:
        return logger  # bereits konfiguriert (z. B. bei Streamlit-Rerun)

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(LOGS_DIR / "app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

"""CSS-Styling für die Streamlit-Oberfläche."""
from pathlib import Path

import streamlit as st

_CSS_PATH = Path(__file__).resolve().parents[2] / "assets" / "css" / "style.css"


def apply_custom_css() -> None:
    """Lädt assets/css/style.css und injiziert es in die Streamlit-Seite."""
    css = _CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

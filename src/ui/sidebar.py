"""Sidebar: optionales Logo, Modell-Laden, E-Mail-Einstellungen, Klassen-Legende."""
from pathlib import Path

import streamlit as st

from src.models.yolo_model import load_model, model_path_exists
from src.utils.constants import CLASS_COLORS_BGR

_LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "images" / "logo.png"


def render_sidebar() -> None:
    with st.sidebar:
        if _LOGO_PATH.exists():
            st.image(str(_LOGO_PATH), use_container_width=True)

        st.markdown("## 🦺 PPE-System")
        st.markdown("---")

        st.markdown("### 🤖 YOLO-Modell")
        model_path = st.text_input(
            "Pfad zum Modell (.pt)",
            value=st.session_state.model_path,
            placeholder="weights/best.pt",
        )
        if st.button("Modell laden"):
            if model_path_exists(model_path):
                with st.spinner("Lade Modell …"):
                    st.session_state.model = load_model(model_path)
                    st.session_state.model_path = model_path
                st.success("Modell geladen ✓")
            else:
                st.error("Dateipfad nicht gefunden!")

        if st.session_state.model:
            st.markdown('<div class="ok-box">Modell aktiv ✓</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">Kein Modell geladen</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📧 E-Mail-Einstellungen")
        st.session_state.email_sender = st.text_input("Absender", value=st.session_state.email_sender)
        st.session_state.email_receiver = st.text_input("Empfänger", value=st.session_state.email_receiver)
        st.session_state.email_password = st.text_input(
            "App-Passwort", type="password", value=st.session_state.email_password
        )
        st.session_state.send_email_flag = st.toggle("E-Mail senden", value=st.session_state.send_email_flag)
        st.session_state.email_cooldown = st.slider(
            "Cooldown (Sek.)", 10, 300, st.session_state.email_cooldown
        )

        st.markdown("---")
        st.markdown("### 🎨 Erkannte Klassen")
        for name, color in CLASS_COLORS_BGR.items():
            r, g, b = color[2], color[1], color[0]
            dot = f'<span style="color:rgb({r},{g},{b})">⬤</span>'
            st.markdown(f'{dot} <span class="info-badge">{name}</span>', unsafe_allow_html=True)

"""Einstiegspunkt der PPE-Erkennungssystem-Streamlit-App."""
import streamlit as st

from src.ui.image_tab import render_image_tab
from src.ui.sidebar import render_sidebar
from src.ui.styles import apply_custom_css
from src.ui.video_tab import render_video_tab
from src.ui.webcam_tab import render_webcam_tab
from src.utils.config import init_session_state, setup_logging
from src.utils.constants import PAGE_ICON, PAGE_TITLE

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

setup_logging()
init_session_state()
apply_custom_css()

render_sidebar()

st.markdown("# 🦺 PPE-Erkennungssystem")
st.markdown("*Persönliche Schutzausrüstung – KI-gestützte Echtzeit-Überwachung*")
st.markdown("---")

tab_img, tab_vid, tab_cam = st.tabs([
    "📷  Bilderkennung",
    "🎬  Videoerkennung",
    "📹  Webcam / Echtzeit",
])

with tab_img:
    render_image_tab()

with tab_vid:
    render_video_tab()

with tab_cam:
    render_webcam_tab()

st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#8b949e; font-size:13px;">'
    'Entwickelt von <strong style="color:#f0b429">Yassine Sadek</strong> · '
    'PPE-Erkennungssystem v2.0 · Powered by YOLOv8 + Streamlit'
    "</div>",
    unsafe_allow_html=True,
)

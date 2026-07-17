"""Tab: Bilderkennung (Datei-Upload)."""
import streamlit as st

from src.detection.image_detector import detect_image
from src.notifications.email_sender import send_alert_email
from src.utils.constants import SUPPORTED_IMAGE_TYPES, WARNINGS_DE
from src.utils.file_utils import save_alert_snapshot, save_output_image
from src.utils.image_utils import bgr_to_rgb, bytes_to_bgr, frame_to_bytes


def render_image_tab() -> None:
    st.markdown("## 📷 Bilderkennung")
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        uploaded_img = st.file_uploader(
            "Bild hochladen", type=SUPPORTED_IMAGE_TYPES, key="img_uploader"
        )
        conf_thresh = st.slider("Konfidenz-Schwellenwert", 0.1, 1.0, 0.4, 0.05, key="img_conf")

        if uploaded_img and st.button("🔍 Erkennung starten", key="btn_img"):
            if not st.session_state.model:
                st.error("Bitte zuerst ein Modell laden!")
            else:
                frame = bytes_to_bgr(uploaded_img.read())

                with st.spinner("Analyse läuft …"):
                    annotated, all_missing = detect_image(
                        st.session_state.model, frame, conf_thresh
                    )

                annotated_rgb = bgr_to_rgb(annotated)
                col2.image(annotated_rgb, caption="Erkennungsergebnis", use_container_width=True)

                img_bytes = frame_to_bytes(annotated)
                save_output_image(img_bytes)

                if all_missing:
                    for item in set(all_missing):
                        st.markdown(
                            f'<div class="warning-box">{WARNINGS_DE.get(item, item)}</div>',
                            unsafe_allow_html=True,
                        )
                    save_alert_snapshot(img_bytes)
                    if st.session_state.send_email_flag:
                        ok, msg = send_alert_email(st.session_state, img_bytes)
                        st.success(msg) if ok else st.warning(msg)
                else:
                    st.markdown(
                        '<div class="ok-box">✅ Alle Sicherheitsausrüstungen erkannt – kein Verstoß!</div>',
                        unsafe_allow_html=True,
                    )

                st.download_button(
                    "⬇ Ergebnis herunterladen",
                    data=img_bytes,
                    file_name="PPE_Ergebnis.jpg",
                    mime="image/jpeg",
                )

    with col2:
        if not uploaded_img:
            st.markdown(
                """
                <div style="border:1px dashed #30363d; border-radius:12px;
                            padding:60px; text-align:center; color:#8b949e; margin-top:20px;">
                  <div style="font-size:56px;">🖼️</div>
                  <div style="font-size:18px; margin-top:12px;">
                    Lade ein Bild hoch und starte die Erkennung
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

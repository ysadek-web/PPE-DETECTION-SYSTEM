"""Tab: Webcam / Kamera-Foto-Erkennung."""
import streamlit as st

from src.detection.image_detector import detect_image
from src.notifications.email_sender import send_alert_email
from src.utils.constants import WARNINGS_DE
from src.utils.file_utils import save_alert_snapshot, save_output_image
from src.utils.image_utils import bgr_to_rgb, bytes_to_bgr, frame_to_bytes


def render_webcam_tab() -> None:
    st.markdown("## 📹 Webcam-Erkennung")

    st.info(
        """
        **Hinweis:** Streamlit läuft im Browser – dauerhafter Webcam-Zugriff
        erfordert `streamlit-webrtc`. Alternativ: Foto über den Browser aufnehmen
        und hier analysieren.
        """
    )

    cam_img = st.camera_input("📸 Foto aufnehmen")

    if cam_img:
        if not st.session_state.model:
            st.error("Bitte zuerst ein Modell laden!")
        else:
            frame = bytes_to_bgr(cam_img.getvalue())

            with st.spinner("Analysiere …"):
                annotated, all_missing = detect_image(st.session_state.model, frame, 0.4)

            col_a, col_b = st.columns(2)
            col_a.image(cam_img, caption="Original", use_container_width=True)
            col_b.image(bgr_to_rgb(annotated), caption="Erkennung", use_container_width=True)

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
                    st.info(msg)
            else:
                st.markdown(
                    '<div class="ok-box">✅ Alle Sicherheitsausrüstungen vorhanden!</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")
    st.markdown("### 🔄 Kontinuierliche Loop-Erkennung (lokale Webcam)")
    st.markdown(
        """
        Für echte Echtzeit-Erkennung über eine lokale Webcam kann eine
        `cv2.VideoCapture(0)`-Schleife genutzt werden, die dieselben Funktionen
        aus `src.detection` wiederverwendet (siehe `PPEDetector` / `detect_image`).
        """
    )

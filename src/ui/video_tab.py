"""Tab: Videoerkennung (Datei-Upload, Frame-für-Frame-Analyse)."""
import streamlit as st

from src.detection.video_detector import process_video
from src.notifications.email_sender import send_alert_email
from src.utils.constants import SUPPORTED_VIDEO_TYPES, WARNINGS_DE
from src.utils.file_utils import cleanup_temp_file, save_output_video, save_temp_upload
from src.utils.image_utils import bgr_to_rgb


def render_video_tab() -> None:
    st.markdown("## 🎬 Videoerkennung")

    uploaded_vid = st.file_uploader(
        "Video hochladen", type=SUPPORTED_VIDEO_TYPES, key="vid_uploader"
    )
    col_v1, col_v2 = st.columns(2)
    conf_v = col_v1.slider("Konfidenz-Schwellenwert", 0.1, 1.0, 0.4, 0.05, key="vid_conf")
    skip_frames = col_v2.slider("Frames überspringen (Geschwindigkeit)", 1, 10, 2)

    if uploaded_vid and st.button("🎬 Video analysieren", key="btn_vid"):
        if not st.session_state.model:
            st.error("Bitte zuerst ein Modell laden!")
            return

        tmp_in_path = save_temp_upload(uploaded_vid.read(), suffix=".mp4")
        tmp_out_path = tmp_in_path.replace(".mp4", "_out.mp4")

        progress_bar = st.progress(0)
        status_text = st.empty()
        preview_slot = st.empty()

        def _on_progress(frame_idx: int, total_frames: int, frame) -> None:
            progress_bar.progress(min(frame_idx / max(total_frames, 1), 1.0))
            status_text.text(f"Verarbeite Frame {frame_idx} / {total_frames} …")
            if frame_idx % (skip_frames * 10) == 0:
                preview_slot.image(
                    bgr_to_rgb(frame),
                    caption=f"Frame {frame_idx}/{total_frames}",
                    use_container_width=True,
                )

        result = process_video(
            model=st.session_state.model,
            input_path=tmp_in_path,
            output_path=tmp_out_path,
            conf_threshold=conf_v,
            skip_frames=skip_frames,
            on_progress=_on_progress,
        )
        cleanup_temp_file(tmp_in_path)

        st.success("✅ Videoanalyse abgeschlossen!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Analysierte Frames", result.total_frames)
        c2.metric("Erkannte Personen", result.total_persons)
        c3.metric(
            "Verstöße erkannt",
            result.total_violations,
            delta=f"-{result.total_violations}" if result.total_violations else None,
            delta_color="inverse",
        )

        if result.unique_missing_items:
            for item in result.unique_missing_items:
                st.markdown(
                    f'<div class="warning-box">{WARNINGS_DE.get(item, item)}</div>',
                    unsafe_allow_html=True,
                )
            if st.session_state.send_email_flag:
                ok, msg = send_alert_email(st.session_state)
                st.info(msg)

        with open(tmp_out_path, "rb") as f:
            video_bytes = f.read()

        saved_path = save_output_video(tmp_out_path)
        st.caption(f"Gespeichert unter: `{saved_path}`")

        st.download_button(
            "⬇ Annotiertes Video herunterladen",
            data=video_bytes,
            file_name="PPE_Video_Ergebnis.mp4",
            mime="video/mp4",
        )

"""E-Mail-Benachrichtigungen bei erkannten PSA-Verstößen."""
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.utils.config import SMTP_HOST, SMTP_PORT

EMAIL_SUBJECT = "🦺 Warnung: Fehlende Sicherheitsausrüstung!"
EMAIL_BODY = (
    "Das System hat fehlende PSA (persönliche Schutzausrüstung) erkannt.\n"
    "Bitte sofort Maßnahmen ergreifen!"
)


def can_send(last_email_time: float, cooldown_seconds: int) -> bool:
    """Prüft, ob der Cooldown seit der letzten E-Mail abgelaufen ist."""
    return (time.time() - last_email_time) >= cooldown_seconds


def send_email(
    sender: str,
    receiver: str,
    password: str,
    image_bytes: bytes | None = None,
) -> tuple[bool, str]:
    """Baut eine Warn-E-Mail zusammen und verschickt sie per SMTP."""
    if not sender or not receiver or not password:
        return False, "E-Mail-Zugangsdaten unvollständig – bitte in den Einstellungen ergänzen."

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = EMAIL_SUBJECT
    msg.attach(MIMEText(EMAIL_BODY, "plain"))

    if image_bytes:
        img_attachment = MIMEImage(image_bytes)
        img_attachment.add_header(
            "Content-Disposition", 'attachment; filename="Warnung_Bild.jpg"'
        )
        msg.attach(img_attachment)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        return True, "E-Mail erfolgreich gesendet ✓"
    except Exception as exc:  # noqa: BLE001 - konkrete SMTP-Fehlermeldung dem Nutzer zeigen
        return False, f"E-Mail-Fehler: {exc}"


def send_alert_email(session_state, image_bytes: bytes | None = None) -> tuple[bool, str]:
    """Orchestriert Cooldown-Prüfung + Versand auf Basis von st.session_state
    (oder einem beliebigen Mapping mit .get()/[]-Zugriff, z. B. in Tests).
    """
    if not session_state.get("send_email_flag", True):
        return False, "E-Mail-Versand ist deaktiviert."

    if not can_send(session_state.get("last_email_time", 0), session_state.get("email_cooldown", 30)):
        return False, "E-Mail-Cooldown aktiv – bitte warten."

    ok, msg = send_email(
        sender=session_state.get("email_sender", ""),
        receiver=session_state.get("email_receiver", ""),
        password=session_state.get("email_password", ""),
        image_bytes=image_bytes,
    )
    if ok:
        session_state["last_email_time"] = time.time()
    return ok, msg

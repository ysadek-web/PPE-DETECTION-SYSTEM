"""Tests für src.notifications.email_sender."""
import time
from unittest.mock import MagicMock, patch

from src.notifications.email_sender import can_send, send_alert_email, send_email


def test_can_send_true_after_cooldown():
    assert can_send(last_email_time=time.time() - 100, cooldown_seconds=30) is True


def test_can_send_false_within_cooldown():
    assert can_send(last_email_time=time.time(), cooldown_seconds=30) is False


def test_send_email_missing_credentials_fails_fast():
    ok, msg = send_email(sender="", receiver="a@b.com", password="")
    assert ok is False
    assert "unvollständig" in msg


@patch("src.notifications.email_sender.smtplib.SMTP")
def test_send_email_success(mock_smtp):
    server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = server

    ok, msg = send_email(sender="a@gmail.com", receiver="b@gmail.com", password="secret")

    assert ok is True
    server.login.assert_called_once_with("a@gmail.com", "secret")
    server.sendmail.assert_called_once()


@patch("src.notifications.email_sender.smtplib.SMTP", side_effect=RuntimeError("Verbindung fehlgeschlagen"))
def test_send_email_smtp_error_is_reported(mock_smtp):
    ok, msg = send_email(sender="a@gmail.com", receiver="b@gmail.com", password="secret")
    assert ok is False
    assert "Verbindung fehlgeschlagen" in msg


def test_send_alert_email_respects_disabled_flag():
    session_state = {"send_email_flag": False}
    ok, msg = send_alert_email(session_state)
    assert ok is False
    assert "deaktiviert" in msg


def test_send_alert_email_respects_cooldown():
    session_state = {
        "send_email_flag": True,
        "last_email_time": time.time(),
        "email_cooldown": 60,
    }
    ok, msg = send_alert_email(session_state)
    assert ok is False
    assert "Cooldown" in msg

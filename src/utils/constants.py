"""Anwendungsweite Konstanten für das PPE-Erkennungssystem."""

CLASS_NAMES = [
    "boots", "gloves", "helmet", "helmet on",
    "no boots", "no glove", "no helmet", "no vest",
    "person", "vest",
]

MISSING_ITEMS = {"no boots", "no glove", "no helmet", "no vest"}

CLASS_COLORS_BGR = {
    "boots":     (0, 255, 0),
    "gloves":    (255, 0, 0),
    "helmet":    (0, 0, 255),
    "helmet on": (0, 200, 100),
    "no boots":  (0, 165, 255),
    "no glove":  (128, 0, 128),
    "no helmet": (147, 20, 255),
    "no vest":   (255, 255, 0),
    "person":    (130, 0, 75),
    "vest":      (128, 128, 0),
}

WARNINGS_DE = {
    "no boots":  "⚠️ Bitte tragen Sie Ihre Sicherheitsstiefel.",
    "no glove":  "⚠️ Bitte tragen Sie Ihre Handschuhe.",
    "no helmet": "⚠️ Bitte setzen Sie Ihren Helm auf.",
    "no vest":   "⚠️ Bitte tragen Sie Ihre Warnweste.",
}

SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png", "bmp"]
SUPPORTED_VIDEO_TYPES = ["mp4", "avi", "mov", "mkv"]

PAGE_TITLE = "PPE-Erkennungssystem"
PAGE_ICON = "🦺"

"""Pytest-Konfiguration: stellt sicher, dass das Projekt-Root im sys.path liegt,
damit `import src...` aus den Tests funktioniert – unabhängig davon, von wo
`pytest` aufgerufen wird.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sys
from pathlib import Path

def obtener_ruta_base():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

# Rutas de carpetas
BASE_DIR = obtener_ruta_base()
RUTA_INPUT = BASE_DIR / "input"
RUTA_OUTPUT = BASE_DIR / "output"
RUTA_CONFIG = RUTA_INPUT / "config.xlsx"
RUTA_LOGS = BASE_DIR / "logs"
RUTA_LOG_FILE = RUTA_LOGS / "app.log"

__all__ = [
    "BASE_DIR",
    "RUTA_INPUT",
    "RUTA_OUTPUT",
    "RUTA_CONFIG",
    "RUTA_LOGS",
    "RUTA_LOG_FILE",
]
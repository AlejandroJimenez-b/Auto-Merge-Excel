import logging
from utils.paths import RUTA_LOGS, RUTA_LOG_FILE
import sys

# ==========================================================
# CONFIGURACION DE LOGGINGS
# ==========================================================
def asegurar_logs():
    #Crear carpeta de logs si no existe
    RUTA_LOGS.mkdir(parents=True, exist_ok=True)

# Configura logging a archivo y consola
def configurar_logging():
    logger = logging.getLogger("AutoMergeExcel")

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(RUTA_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


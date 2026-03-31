from utils.paths import RUTA_INPUT
import logging
logger = logging.getLogger("AutoMergeExcel")

def verificar_carpetas():
    try:
        RUTA_INPUT.mkdir(parents=True, exist_ok=True)
        logger.info(f"Carpeta input verificada: {RUTA_INPUT}")
        return True
    except Exception as e:
        logger.error(f"Error creando carpeta input: {e}")
        return False


def obtener_excels():
    archivos_excel = sorted([
        f for f in RUTA_INPUT.glob("*.xlsx")
        if f.name.lower() != "config.xlsx"
    ])

    if len(archivos_excel) == 0:
        logger.warning("No hay archivos Excel en la carpeta input")
        logger.warning(f"Ruta esperada: {RUTA_INPUT.resolve()}")
        return []

    logger.info(f"Leyendo archivos desde: {RUTA_INPUT.resolve()}")
    logger.info(f"Se encontraron {len(archivos_excel)} archivos")

    for archivo in archivos_excel:
        logger.info(f" - {archivo.name}")

    return archivos_excel
import logging
import pandas as pd

from utils.logger import asegurar_logs,configurar_logging
from utils.file_manager import verificar_carpetas, obtener_excels

from core.config_manager import (
    crear_config_si_no_existe,
    cargar_configuracion,
    aplicar_sugerencias_config
)

from core.heuristics import detectar_columnas_automaticas
from core.excel_reader import leer_excel_seguro, columnas_compatibles
from core.excel_transformer import fusionar_dataframes
from core.excel_writer import guardar_resultado, calcular_metricas, guardar_resumen


def main():

    # ==========================================================
    # 1. LOGGING
    # ==========================================================
    asegurar_logs()
    configurar_logging()
    logger = logging.getLogger("AutoMergeExcel")
    logger.info("=== INICIO PROCESO AUTOMERGE EXCEL ===")

    # ==========================================================
    # 2. ENTORNO
    # ==========================================================
    if not verificar_carpetas():
        logger.error("Error en verificación de carpetas")
        return

    # ==========================================================
    # 3. CONFIG
    # ==========================================================
    crear_config_si_no_existe()
    mapeo = cargar_configuracion()

    # ==========================================================
    # 4. OBTENER ARCHIVOS
    # ==========================================================
    archivos = obtener_excels()

    if not archivos:
        logger.warning("No hay archivos para procesar")
        return

    # ==========================================================
    # 5. HEURÍSTICA (solo cabeceras del primer archivo)
    # ==========================================================
    try:
        df_preview = pd.read_excel(archivos[0], nrows=0)
        df_preview.columns = [str(col).strip().lower() for col in df_preview.columns]

        sugerencias = detectar_columnas_automaticas(df_preview.columns)

        if sugerencias:
            logger.info("Aplicando sugerencias heurísticas...")
            aplicar_sugerencias_config(sugerencias)

            # recargar config tras cambios
            mapeo = cargar_configuracion()
        else:
            logger.info("Heurística: sin sugerencias")

    except Exception as e:
        logging.warning(f"No se pudo aplicar heurística: {e}")

    # ==========================================================
    # 6. LECTURA DE ARCHIVOS
    # ==========================================================
    lista_dfs = []

    for archivo in archivos:

        df = leer_excel_seguro(archivo, mapeo)

        if df is not None:
            lista_dfs.append(df)

    if not lista_dfs:
        logger.error("No hay datos válidos tras la lectura")
        return

    # ==========================================================
    # 7. VALIDACIÓN
    # ==========================================================
    if not columnas_compatibles(lista_dfs):
        logger.error("Columnas incompatibles entre archivos")
        return

    # ==========================================================
    # 8. TRANSFORMACIÓN
    # ==========================================================
    df_final = fusionar_dataframes(lista_dfs)

    if df_final is None:
        logger.error("Error en la fusión de datos")
        return

    # ==========================================================
    # 9. MÉTRICAS
    # ==========================================================
    df_final, metricas, resumen = calcular_metricas(df_final)

    # ==========================================================
    # 10. SALIDA
    # ==========================================================
    guardar_resultado(df_final)
    guardar_resumen(metricas, resumen)

    logger.info("=== FIN PROCESO ===")


# ENTRY POINT
if __name__ == "__main__":
    main()
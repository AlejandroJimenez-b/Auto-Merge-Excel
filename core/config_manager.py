import sys
import pandas as pd
import logging

from utils.paths import RUTA_CONFIG
from utils.normalizer import normalizar_columna


COLUMNAS_REQUERIDAS = {"producto", "precio", "cantidad"}
logger = logging.getLogger("AutoMergeExcel")

def crear_config_si_no_existe():

    if not RUTA_CONFIG.exists():

        logger.warning("No existe config.xlsx. Creando plantilla...")

        df_config = pd.DataFrame({
            "campo_interno": ["producto", "precio", "cantidad"],
            "columna_excel": ["", "", ""],
            "descripcion": [
                "Nombre del producto o servicio",
                "Precio unitario",
                "Cantidad vendida"
            ]
        })

        df_config.to_excel(RUTA_CONFIG, index=False)

        logger.info("Se ha creado una plantilla de configuración.")
        logger.info(f"Plantilla creada en: {RUTA_CONFIG.resolve()}")

        logger.info("Edite config.xlsx -> 'columna_excel' para indicar qué columnas corresponden a:")
        logger.info("producto | precio | cantidad")
        logger.info("Después vuelva a ejecutar el programa.")

        sys.exit(0)


def cargar_configuracion():

    try:

        logger.info("Cargando archivo config.xlsx")

        df = pd.read_excel(RUTA_CONFIG, dtype=str)

        df.columns = [normalizar_columna(c) for c in df.columns]

        if not {"campo_interno", "columna_excel"}.issubset(df.columns):

            logger.critical(
                "config.xlsx debe contener las columnas: campo_interno | columna_excel"
            )
            sys.exit(1)

        df["campo_interno"] = df["campo_interno"].apply(normalizar_columna)
        df["columna_excel"] = df["columna_excel"].fillna("").apply(normalizar_columna)

        if set(df["campo_interno"]) != COLUMNAS_REQUERIDAS:

            logger.critical(
                f"config.xlsx debe contener exactamente: {COLUMNAS_REQUERIDAS}"
            )
            sys.exit(1)

        if df["campo_interno"].duplicated().any():

            logger.critical("Hay campos internos duplicados en config.xlsx")
            sys.exit(1)

        columnas_definidas = df[df["columna_excel"] != ""]["columna_excel"]

        if columnas_definidas.duplicated().any():

            logger.critical("Hay columnas_excel duplicadas en config.xlsx")
            sys.exit(1)

        df_validas = df[df["columna_excel"] != ""]

        mapeo = dict(zip(df_validas["columna_excel"], df_validas["campo_interno"]))

        logger.info("Archivo config.xlsx cargado correctamente")

        return mapeo

    except Exception as e:

        logger.critical(f"Error leyendo config.xlsx: {e}")
        sys.exit(1)


def aplicar_sugerencias_config(sugerencias):

    if not RUTA_CONFIG.exists():
        return

    try:

        df_config = pd.read_excel(RUTA_CONFIG, dtype=str)

        df_config.columns = [normalizar_columna(c) for c in df_config.columns]

        if not {"campo_interno", "columna_excel"}.issubset(df_config.columns):
            logger.error("config.xlsx inválido al aplicar sugerencias")
            return

        df_config["campo_interno"] = df_config["campo_interno"].apply(normalizar_columna)
        df_config["columna_excel"] = df_config["columna_excel"].fillna("").apply(normalizar_columna)

        cambios = False

        for campo, columna_detectada in sugerencias.items():

            fila = df_config["campo_interno"] == campo

            if df_config.loc[fila].empty:
                continue

            valor_actual = df_config.loc[fila, "columna_excel"].values[0]

            columna_detectada = normalizar_columna(columna_detectada)

            if columna_detectada in df_config["columna_excel"].values:
                continue

            if valor_actual == "":

                df_config.loc[fila, "columna_excel"] = columna_detectada
                cambios = True

                logger.info(
                    f"Auto-mapeo aplicado -> Sistema: '{campo}' | Excel: '{columna_detectada}'"
                )

        if cambios:

            df_config.to_excel(RUTA_CONFIG, index=False)
            logger.info("config.xlsx actualizado con sugerencias automáticas.")

        else:

            logger.info("No fue necesario modificar config.xlsx")

    except Exception as e:

        logger.error(f"No se pudieron aplicar sugerencias al config: {e}")

import pandas as pd
import logging

from core.config_manager import COLUMNAS_REQUERIDAS
from utils.normalizer import normalizar_columna
logger = logging.getLogger("AutoMergeExcel")

def leer_excel_seguro(ruta_archivo, mapeo):

    try:

        df = pd.read_excel(ruta_archivo, dtype=str)

        df.columns = [normalizar_columna(col) for col in df.columns]

        logger.info(f"{ruta_archivo.name} columnas detectadas: {list(df.columns)}")

        # aplicar mapeo
        df = df.rename(columns=mapeo)

        if not COLUMNAS_REQUERIDAS.issubset(set(df.columns)):

            faltantes = COLUMNAS_REQUERIDAS - set(df.columns)

            logger.error(
                f"{ruta_archivo.name} no contiene columnas obligatorias: {faltantes}"
            )

            return None

        if df.empty:

            logger.warning(f"{ruta_archivo.name} está vacío")
            return None

        df = limpiar_datos(df, ruta_archivo.name)

        if df.empty:

            logger.warning(f"{ruta_archivo.name} no tiene filas válidas")
            return None

        return df

    except PermissionError:

        logger.error(f"{ruta_archivo.name} está abierto. Ciérralo.")
        return None

    except Exception as e:

        logger.error(f"Error leyendo {ruta_archivo.name}: {e}")
        return None


def limpiar_datos(df, nombre_archivo):

    filas_validas = []

    for i, fila in df.iterrows():

        try:

            fila_dict = fila.to_dict()

            producto = str(fila_dict.get("producto", "")).strip()
            precio = float(str(fila_dict.get("precio", "0")).replace(",", "."))
            cantidad = int(float(str(fila_dict.get("cantidad", "0"))))

            if cantidad <= 0 or precio < 0:
                raise ValueError

            fila_dict["producto"] = producto
            fila_dict["precio"] = precio
            fila_dict["cantidad"] = cantidad

            filas_validas.append(fila_dict)

        except (ValueError, TypeError):

            logger.warning(
                f"Fila inválida eliminada en {nombre_archivo} (fila {i+2})"
            )

    return pd.DataFrame(filas_validas)


def columnas_compatibles(lista_dfs):

    if not lista_dfs:
        return False

    columnas_base = set(lista_dfs[0].columns)

    for i, df in enumerate(lista_dfs[1:], start=2):

        if set(df.columns) != columnas_base:

            logger.error(f"El archivo #{i} tiene columnas diferentes")
            logger.error(f"Esperadas: {columnas_base}")
            logger.error(f"Encontradas: {set(df.columns)}")

            return False

    return True
import pandas as pd
import logging
logger = logging.getLogger("AutoMergeExcel")


def fusionar_dataframes(lista_dfs):

    if not lista_dfs:
        logger.error("No hay dataframes para fusionar")
        return None

    # eliminar None
    lista_dfs = [df for df in lista_dfs if df is not None]

    if not lista_dfs:
        logger.error("Todos los dataframes son inválidos")
        return None

    # validar columnas
    columnas_base = set(lista_dfs[0].columns)

    for df in lista_dfs:
        if set(df.columns) != columnas_base:
            logger.error("Columnas incompatibles entre archivos")
            return None

    # copia defensiva
    lista_dfs = [df.copy() for df in lista_dfs]

    df_final = pd.concat(lista_dfs, ignore_index=True)

    logger.info(
        f"Fusión completada | archivos: {len(lista_dfs)} | filas totales: {len(df_final)}"
    )

    return df_final
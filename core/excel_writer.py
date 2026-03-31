from utils.paths import RUTA_OUTPUT
import pandas as pd
import logging
logger = logging.getLogger("AutoMergeExcel")

# GUARDAR RESULTADO

def guardar_resultado(df):

    try:
        RUTA_OUTPUT.mkdir(parents=True, exist_ok=True)

        ruta_salida = RUTA_OUTPUT / "resultado.xlsx"

        df.to_excel(ruta_salida, index=False)

        logger.info(f"Archivo generado en: {ruta_salida}")

    except Exception as e:

        logger.error(f"Error guardando resultado: {e}")

# CALCULO DE METRICAS

def calcular_metricas(df):
    df = df.copy()

    df["total"] = df["precio"] * df["cantidad"]

    # ===== MÉTRICAS GLOBALES =====
    total_facturacion = df["total"].sum()
    total_unidades = df["cantidad"].sum()
    productos_unicos = df["producto"].nunique()

    if total_unidades > 0:
        precio_promedio_ponderado = total_facturacion / total_unidades
    else:
        precio_promedio_ponderado = 0

    metricas_globales = pd.DataFrame({
        "Metrica": [
            "Facturacion total",
            "Unidades totales",
            "Productos unicos",
            "Precio promedio ponderado"
        ],
        "Valor": [
            total_facturacion,
            total_unidades,
            productos_unicos,
            precio_promedio_ponderado
        ]
    })

    # ===== MÉTRICAS POR PRODUCTO =====
    resumen_producto = (
        df.groupby("producto", as_index=False)
        .agg({
            "cantidad": "sum",
            "total": "sum"
        })
    )

    resumen_producto["precio_promedio"] = (
        resumen_producto["total"] / resumen_producto["cantidad"]
    )

    return df, metricas_globales, resumen_producto

# GUARDAR RESUMEN

def guardar_resumen(metricas_globales, resumen_producto):
    ruta_resumen = RUTA_OUTPUT / "resumen.xlsx"

    with pd.ExcelWriter(ruta_resumen) as writer:
        metricas_globales.to_excel(writer, sheet_name="Metricas Globales", index=False)
        resumen_producto.to_excel(writer, sheet_name="Por Producto", index=False)

    logger.info(f"Resumen generado en: {ruta_resumen}")
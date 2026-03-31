from difflib import SequenceMatcher
import logging
from utils.normalizer import normalizar_columna
logger = logging.getLogger("AutoMergeExcel")

PALABRAS_CLAVE = {
    "producto": ["producto", "item", "articulo", "servicio", "nombre"],
    "precio": ["precio", "price", "coste", "valor", "importe", "precio_unitario"],
    "cantidad": ["cantidad", "qty", "unidades", "cantidad_vendida", "stock"]
}

def similitud(a, b):
    return SequenceMatcher(None, str(a), str(b)).ratio()


def calcular_score(columna, palabra):

    col = normalizar_columna(columna)
    palabra = normalizar_columna(palabra)

    score_similitud = similitud(col, palabra)

    contiene = 1 if palabra in col else 0
    empieza = 1 if col.startswith(palabra) else 0

    score_total = (
        score_similitud * 0.5 +
        contiene * 0.3 +
        empieza * 0.2
    )

    return score_total


def detectar_columnas_automaticas(columnas_excel):

    sugerencias = {}
    columnas_usadas = set()

    for campo, palabras in PALABRAS_CLAVE.items():

        mejor_columna = None
        mejor_score = 0

        for columna in columnas_excel:

            col_normalizada = normalizar_columna(columna)

            for palabra in palabras:

                score = calcular_score(col_normalizada, palabra)

                if palabra in col_normalizada:
                    score = max(score, 0.9)

                if score > mejor_score:
                    mejor_score = score
                    mejor_columna = columna

        if mejor_score > 0.6 and mejor_columna not in columnas_usadas:

            sugerencias[campo] = mejor_columna
            columnas_usadas.add(mejor_columna)

            logger.info(
                f"Heurística -> Excel: '{mejor_columna}' | Sistema: '{campo}' | score={mejor_score:.2f}"
            )

        # 🔥 FALLBACK INTELIGENTE
        else:

            # buscar mejor columna disponible no usada
            fallback_columna = None
            fallback_score = 0

            for columna in columnas_excel:

                if columna in columnas_usadas:
                    continue

                # score genérico (sin palabras clave)
                score = similitud(normalizar_columna(columna), campo)

                if score > fallback_score:
                    fallback_score = score
                    fallback_columna = columna

            if fallback_columna:

                sugerencias[campo] = fallback_columna
                columnas_usadas.add(fallback_columna)

                logger.warning(
                    f"Fallback aplicado -> Excel: '{fallback_columna}' | Sistema: '{campo}' | score={fallback_score:.2f}"
                )

    return sugerencias

import re

# Normaliza los nombres de las columnas excel
def normalizar_columna(nombre):
    nombre = str(nombre).strip().lower()

    # reemplazar espacios por _
    nombre = nombre.replace(" ","_")

    # Eliminar caracteres raros
    nombre = re.sub(r"[^a-z0-9_]", "", nombre)

    return nombre
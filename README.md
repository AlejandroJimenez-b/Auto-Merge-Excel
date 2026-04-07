# AutoMergeExcel

**AutoMergeExcel** es una herramienta de escritorio desarrollada en **Python** para procesar datos en Excel, pensada para **unificar múltiples archivos en un único conjunto de datos consolidado**, además de generar **métricas de los resultados y resúmenes automáticamente**.

Este proyecto nació con una idea muy práctica:  
**convertir una tarea manual, repetitiva en un flujo de trabajo limpio, reutilizable y escalable**.

---

## ¿Por qué existe este proyecto?

En muchas empresas, los archivos Excel siguen siendo una de las formas más habituales de almacenar información, como por ejemplo:

- ventas de productos
- movimientos de stock
- registros de compras
- tablas de precios

El problema es que estos archivos suelen venir de **personas, departamentos o sistemas distintos**, y casi nunca llegan con una estructura totalmente limpia o estandarizada.

Ahí es donde entra **AutoMergeExcel**.

Esta herramienta permite al usuario:

- colocar varios archivos Excel dentro de la carpeta `input/`
- unificarlos automáticamente
- validar su estructura y contenido
- calcular métricas útiles
- exportar tanto el resultado de cálculos de los datos combinados como un resumen de dicho negocio

---

## Funcionalidades principales

### Mapeo flexible de columnas
El programa **no da por hecho nombres de columnas fijos**.

En lugar de eso, el usuario configura qué columnas de sus Excel corresponden a los campos internos obligatorios:

- `producto`
- `precio`
- `cantidad`

Esto hace que la herramienta sea **mucho más adaptable** a distintas estructuras de archivo utilizadas por diferentes empresas o usuarios.

---

### Plantilla de configuración automática
En la primera ejecución, el programa genera automáticamente todo lo necesario para empezar a trabajar:

- `input/`
- `output/`
- `logs/`
- `config.xlsx`

Esto hace que el proyecto sea **usable desde el primer momento**, sin necesidad de preparar manualmente carpetas o archivos base.

---

### Sugerencias inteligentes mediante heurísticas
Si el usuario todavía no ha configurado correctamente `config.xlsx`, el sistema intenta detectar coincidencias probables de forma automática.

Por ejemplo, columnas como:

- `item`
- `price`
- `qty`

pueden ser sugeridas como equivalencias de:

- `producto`
- `precio`
- `cantidad`

Esto mejora bastante la experiencia de uso y reduce conflictos entre columnas, especialmente para usuarios no técnicos.

---

### Limpieza y validación de datos
Antes de unificar los datos, el programa valida cada fila.

Puede detectar y descartar automáticamente registros inválidos como:

- filas vacías
- valores numéricos incorrectos
- precios negativos
- cantidades nulas o no válidas

De esta forma, el resultado final es **mucho más fiable y limpio**.

---

### Generación automática de métricas de negocio
Además de combinar archivos, el software calcula automáticamente métricas útiles como:

- facturación total
- unidades totales vendidas
- número de productos únicos
- precio medio ponderado

También genera un **resumen agrupado por producto**.

---

### Salida separada para datos y resumen
El proyecto genera dos archivos de salida:

- `resultado.xlsx` → datos unificados -> `output/`
- `resumen.xlsx` → métricas y resumen de negocio -> `output/`

Esta separación hace que la herramienta sea **más profesional, más clara y más útil en un entorno real**.

---

### Sistema de logs
La aplicación incluye un sistema de logging estructurado que registra:

- el flujo de ejecución
- advertencias
- problemas detectados
- filas inválidas
- errores de configuración
- estado final del procesamiento

Esto facilita mucho el **mantenimiento, la depuración y la escalabilidad del proyecto**.

---

## Estructura del proyecto

```bash
AutoMergeExcel/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── core/
│   ├── config_manager.py
│   ├── excel_reader.py
│   ├── excel_transformer.py
│   ├── excel_writer.py
│   ├── file_manager.py
│   └── heuristics.py
│
├── utils/
│   ├── logger.py
│   ├── normalizer.py
│   └── paths.py
│
├── input/
│   └── .gitkeep
│
├── output/
│   └── .gitkeep
│
└── logs/
    └── .gitkeep

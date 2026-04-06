## Proyecto ETL – Calidad del Aire (Colombia vs Global)

## Integrantes

* Melissa Palacios
* Diego Valencia
* Waldor Drada
* Jorge Andrés Rivas

## Descripción del Proyecto

Este proyecto desarrolla un proceso **ETL (Extract, Transform, Load)** para integrar datos de calidad del aire provenientes de Colombia y del contexto global.

El objetivo es construir un dataset limpio, estructurado y listo para análisis, permitiendo realizar comparaciones entre ciudades y países.


## Objetivo

Integrar y estandarizar múltiples fuentes de datos de calidad del aire para facilitar análisis comparativos y estudios de ciencia de datos.

## Problema

Los datos de calidad del aire:

* Están dispersos en diferentes fuentes
* Tienen estructuras distintas
* Presentan inconsistencias y valores nulos

Esto dificulta su uso para análisis y toma de decisiones.

## Fuentes de Datos

### 🇨🇴 Datos Abiertos Colombia

* Información de estaciones de monitoreo del aire
* Variables: Año, Municipio, Contaminante, Promedio

###  Global Air Pollution (Kaggle)

* Datos de calidad del aire a nivel mundial
* Variables: País, Ciudad, AQI, PM2.5, NO2, O3, CO

---

##  Proceso ETL

### 1. Extract (Extracción)

* Carga de datos desde archivos CSV usando Python
* Uso de pandas para manejo de datos

### 2. Transform (Transformación)

* Limpieza de datos
* Eliminación de valores nulos
* Conversión de tipos de datos
* Estandarización de nombres de columnas
* Transformación de formato (pivot en dataset Colombia)
* Selección de contaminantes relevantes:

  * PM2.5, PM10, NO2, SO2, O3, CO

### 3. Load (Carga)

Se generan los siguientes archivos:

* `colombia_limpio.xlsx`
* `global_limpio.xlsx`
* `dataset_integrado_calidad_aire.xlsx`

---

## Pipeline ETL

El pipeline fue desarrollado en **Python** y estructurado en funciones:

* `extract_data()` → extracción
* `transform_colombia()` → limpieza Colombia
* `transform_global()` → limpieza global
* `integrate_data()` → integración
* `save_XLSX()` → exportación
* `main()` → ejecución completa

Diseño modular, reproducible y escalable

---

## Calidad de Datos

Se identificaron problemas como:

* Valores nulos
* Datos duplicados
* Tipos de datos incorrectos
* Diferencias en estructura

Se aplicaron reglas de validación como:

* No nulos en País y Ciudad
* Valores numéricos en contaminantes
* No duplicados por País–Ciudad–Año

---

## Resultado Final

* Dataset integrado con:

  * 24,133 registros
  * 10 variables

Variables principales:

* País, Ciudad, Año
* PM2.5, PM10, NO2, SO2, O3, CO
* AQI

---

## Análisis (Power BI)

Se construyó un dashboard que permitió:

* Comparación Colombia vs mundo
* Identificación de países más contaminados
* Análisis por ciudades
* Tendencias temporales

### Hallazgos clave

* Colombia tiene menor PM2.5 que el promedio global
* Alta contaminación en Asia y Medio Oriente
* Tendencia decreciente en Colombia

---

## Limitaciones

* Datos incompletos en algunas variables
* Diferencias metodológicas entre fuentes
* No comparabilidad directa absoluta
* Datos históricos (no en tiempo real)

---

## Tecnologías Utilizadas

* Python
* Pandas
* Power BI
* Excel


##  Conclusión

El proyecto demuestra la importancia de los procesos ETL en ciencia de datos, permitiendo transformar datos heterogéneos en información útil para análisis y toma de decisiones.

El pipeline desarrollado garantiza:

* Calidad de datos
* Reproducibilidad
* Escalabilidad

---

## Nota

Este proyecto fue desarrollado como entrega final del curso **ETL – Universidad Autónoma de Occidente (2026)**.

import pandas as pd
from pathlib import Path

import unicodedata

def limpiar_texto(texto):
    if pd.isna(texto):
        return texto
    
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.upper()
    texto = texto.strip()
    
    return texto

def get_paths():
    base_path = Path(__file__).resolve().parent

    paths = {
        "colombia": base_path / "data/raw/Calidad_Del_Aire_En_Colombia.csv",
        "global": base_path / "data/raw/global_air_pollution_dataset.csv",
        "output_integrado": base_path / "data/output/dataset_integrado_calidad_aire.csv",
        "output_colombia": base_path / "data/output/colombia_limpio.csv",
        "output_global": base_path / "data/output/global_limpio.csv"
    }

    return paths


# =========================================================
# 2) EXTRACT
# =========================================================

def extract_data(paths):
    """Carga los datasets de Colombia y global desde archivos CSV."""
    try:
        colombia = pd.read_csv(paths["colombia"])
        global_air = pd.read_csv(paths["global"])
        print("✅ Archivos cargados correctamente.")
        return colombia, global_air
    except FileNotFoundError as e:
        print(f"❌ Error: no se encontró un archivo.\n{e}")
        raise
    except Exception as e:
        print(f"❌ Error inesperado al cargar los datos.\n{e}")
        raise


# =========================================================
# 3) QUALITY REPORT
# =========================================================

def quality_report(colombia, global_air):
    """Muestra un reporte básico de calidad de datos."""
    print("\n==============================")
    print("REPORTE DE CALIDAD DE DATOS")
    print("==============================")

    print("\n--- DATASET COLOMBIA ---")
    print("Dimensiones:", colombia.shape)
    print("\nColumnas:")
    print(list(colombia.columns))
    print("\nTipos de datos:")
    print(colombia.dtypes)
    print("\nValores nulos:")
    print(colombia.isna().sum())
    print("\nDuplicados:", colombia.duplicated().sum())

    if "Variable" in colombia.columns:
        print("\nVariables encontradas:")
        print(colombia["Variable"].unique())

    print("\n--- DATASET GLOBAL ---")
    print("Dimensiones:", global_air.shape)
    print("\nColumnas:")
    print(list(global_air.columns))
    print("\nTipos de datos:")
    print(global_air.dtypes)
    print("\nValores nulos:")
    print(global_air.isna().sum())
    print("\nDuplicados:", global_air.duplicated().sum())


# =========================================================
# 4) TRANSFORM - COLOMBIA
# =========================================================

def transform_colombia(colombia):
    columnas_necesarias = ["Variable", "Promedio", "Nombre del Municipio", "Año"]
    for col in columnas_necesarias:
        if col not in colombia.columns:
            raise ValueError(f"❌ Falta la columna '{col}' en el dataset de Colombia.")

    contaminantes = ["PM2.5", "PM10", "NO2", "SO2", "O3", "CO"]

    colombia_filtrado = colombia[colombia["Variable"].isin(contaminantes)].copy()

    colombia_filtrado["Promedio"] = (
        colombia_filtrado["Promedio"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    colombia_filtrado["Promedio"] = pd.to_numeric(
        colombia_filtrado["Promedio"],
        errors="coerce"
    )

    colombia_pivot = colombia_filtrado.pivot_table(
        index=["Nombre del Municipio", "Año"],
        columns="Variable",
        values="Promedio",
        aggfunc="mean"
    ).reset_index()

    colombia_limpio = colombia_pivot.rename(columns={
        "Nombre del Municipio": "Ciudad"
    })

    colombia_limpio["Pais"] = "Colombia"
    colombia_limpio.columns.name = None

    for col in colombia_limpio.select_dtypes(include="object").columns:
        colombia_limpio[col] = colombia_limpio[col].apply(limpiar_texto)

    print("\n--- TRANSFORMACIÓN COLOMBIA ---")
    print("Filas después del filtrado y pivot:", colombia_limpio.shape)

    return colombia_limpio


# =========================================================
# 5) TRANSFORM - GLOBAL
# =========================================================

def transform_global(global_air):

    columnas_necesarias = [
        "Country", "City", "AQI Value", "CO AQI Value",
        "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"
    ]

    for col in columnas_necesarias:
        if col not in global_air.columns:
            raise ValueError(f"❌ Falta la columna '{col}' en el dataset global.")

    global_air = global_air.dropna(subset=["Country", "City"]).copy()

    columnas_numericas = ["CO AQI Value", "Ozone AQI Value", "NO2 AQI Value", "PM2.5 AQI Value"]

    for col in columnas_numericas:
        global_air[col] = (
            global_air[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        global_air[col] = pd.to_numeric(global_air[col], errors="coerce")

    global_air = global_air.rename(columns={
        "Country": "Pais",
        "City": "Ciudad",
        "AQI Value": "AQI",
        "CO AQI Value": "CO",
        "Ozone AQI Value": "O3",
        "NO2 AQI Value": "NO2",
        "PM2.5 AQI Value": "PM2.5"
    })

    global_limpio = global_air[["Pais", "Ciudad", "AQI", "PM2.5", "NO2", "O3", "CO"]].copy()

    for col in global_limpio.select_dtypes(include="object").columns:
        global_limpio[col] = global_limpio[col].apply(limpiar_texto)

    return global_limpio


# =========================================================
# 6) INTEGRACIÓN
# =========================================================

def integrate_data(colombia_limpio, global_limpio):
    """Integra las dos fuentes de datos en un solo dataset."""
    dataset_integrado = pd.concat(
        [colombia_limpio, global_limpio],
        ignore_index=True,
        sort=False
    )

    print("\n--- INTEGRACIÓN FINAL ---")
    print("Dimensiones dataset integrado:", dataset_integrado.shape)
    print("Columnas finales:")
    print(list(dataset_integrado.columns))

    return dataset_integrado


# =========================================================
# 7) REPORTE FINAL
# =========================================================

def final_report(dataset_integrado):
    """Muestra un resumen final del dataset integrado."""
    print("\n--- REPORTE FINAL DATASET INTEGRADO ---")
    print("Dimensiones:", dataset_integrado.shape)

    print("\nValores nulos:")
    print(dataset_integrado.isna().sum())

    print("\nPrimeras filas:")
    print(dataset_integrado.head())


# =========================================================
# 8) SAVE
# =========================================================

def save_excel(df, path_str, nombre):
    output_path = Path(path_str).with_suffix(".xlsx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(output_path, index=False)

    print(f"\n✅ {nombre} guardado en:")
    print(output_path.resolve())


# =========================================================
# 9) MAIN
# =========================================================

def main():
    print("Iniciando pipeline ETL...\n")

    # 1. Rutas
    paths = get_paths()

    # 2. Extracción
    colombia, global_air = extract_data(paths)

    # 3. Validación / exploración inicial
    quality_report(colombia, global_air)

    # 4. Transformación
    colombia_limpio = transform_colombia(colombia)
    global_limpio = transform_global(global_air)

    # 5. Guardar resultados intermedios
    save_excel(colombia_limpio, paths["output_colombia"], "colombia_limpio.xlsx")
    save_excel(global_limpio, paths["output_global"], "global_limpio.xlsx")
    # 6. Integración
    dataset_integrado = integrate_data(colombia_limpio, global_limpio)

    # 7. Reporte final
    final_report(dataset_integrado)

    # 8. Guardar resultado final
    save_excel(dataset_integrado, paths["output_integrado"], "dataset_integrado_calidad_aire.xlsx")

    print("\n🎉 ETL finalizado correctamente.")


if __name__ == "__main__":
    main()
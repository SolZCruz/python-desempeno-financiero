"""
02_desempeno_macrosector.py

Responde la pregunta principal del proyecto:
¿Qué macrosector tuvo el mejor desempeño financiero entre 2017 y 2018,
y qué región concentra ese desempeño?

Ejecutar directamente este script:
    python src/02_desempeno_macrosector.py

Lee desde data/processed/empresas_limpio.csv (generado por 01_carga_y_limpieza.py)
"""

from pathlib import Path
import pandas as pd
import json


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "empresas_limpio.csv"
RESULTADO_PATH = BASE_DIR / "data" / "processed" / "lider.json" 

COL_INGRESOS_2017 = "INGRESOS OPERACIONALES 2017"
COL_INGRESOS_2018 = "INGRESOS OPERACIONALES 2018"
COL_GANANCIA_2017 = "GANANCIA (PERDIDA) 2017"
COL_GANANCIA_2018 = "GANANCIA (PERDIDA) 2018"


def growth_by_macrosector(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula ingresos, ganancia y % de crecimiento 2017->2018 por macrosector.
    """
    resumen = df.groupby("MACROSECTOR", as_index=False).agg(
        ingresos_2017=(COL_INGRESOS_2017, "sum"),
        ingresos_2018=(COL_INGRESOS_2018, "sum"),
        ganancia_2017=(COL_GANANCIA_2017, "sum"),
        ganancia_2018=(COL_GANANCIA_2018, "sum"),
        num_empresas=("NIT", "count"),
    )

    resumen["crecimiento_ingresos_%"] = (
        (resumen["ingresos_2018"] - resumen["ingresos_2017"])
        / resumen["ingresos_2017"] * 100
    ).round(2)

    resumen["crecimiento_ganancia_%"] = (
        (resumen["ganancia_2018"] - resumen["ganancia_2017"]) 
        / resumen["ganancia_2017"].abs() * 100  
         #Se coloca el abs sin problema para la interpretacion del crecimiento porcentual, las ganancias para el año 2017 son positivas  (a nivel macrosector)    
    ).round(2)

    return resumen.sort_values("crecimiento_ingresos_%", ascending=False)


def top_region_by_macrosector(df: pd.DataFrame, macrosector: str) -> pd.DataFrame:
    """
    Dado el macrosector líder, se identifica en qué región se concentra
    su desempeño (ingresos/ganancia).
    """
    df_sector = df[df["MACROSECTOR"] == macrosector]

    resumen = df_sector.groupby("REGIÓN", as_index=False).agg(
        ingresos_2018=(COL_INGRESOS_2018, "sum"),
        ganancia_2018=(COL_GANANCIA_2018, "sum"),
        num_empresas=("NIT", "count"),
    )

    return resumen.sort_values("ingresos_2018", ascending=False)


if __name__ == "__main__":
    df = pd.read_csv(PROCESSED_PATH)

    resumen_macrosectores = growth_by_macrosector(df)
    print("=== Desempeño por macrosector (2017 -> 2018) ===")
    print(resumen_macrosectores.to_string(index=False))

    macrosector_lider = resumen_macrosectores.iloc[0]["MACROSECTOR"]
    print(f"\nMacrosector líder: {macrosector_lider}")

    resumen_region = top_region_by_macrosector(df, macrosector_lider)
    print(f"\n=== Región líder dentro de {macrosector_lider} ===")
    print(resumen_region.to_string(index=False))

    region_lider = resumen_region.iloc[0]["REGIÓN"]   # <-- AGREGADA
    print(f"Región líder: {region_lider}")

    # --- Verificación de las ganancias para saber su base ---
    resumen = growth_by_macrosector(df)
    print(resumen[["MACROSECTOR", "ganancia_2017", "ganancia_2018", "crecimiento_ganancia_%"]])

    resumen["ganancia_2017_negativa"] = resumen["ganancia_2017"] < 0
    print(resumen[resumen["ganancia_2017_negativa"]])

    resumen["ganancia_2018_negativa"] = resumen["ganancia_2018"] < 0
    print(resumen[resumen["ganancia_2018_negativa"]])

    # --- Guarda el resultado para que otros scripts lo usen automáticamente ---
    resultado = {
        "macrosector_lider": macrosector_lider,
        "region_lider": region_lider,
    }
    with open(RESULTADO_PATH, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\nResultado guardado en: {RESULTADO_PATH}")

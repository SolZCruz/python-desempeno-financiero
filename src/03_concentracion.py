"""
03_concentracion.py

Análisis complementario (cierre del proyecto):
¿Qué tan concentrado está el desempeño del macrosector/región líder
en pocas empresas?

Ejecutar directamente este script:
    python src/03_concentracion.py

Lee desde data/processed/empresas_limpio.csv (generado por 01_carga_y_limpieza.py)
"""

from pathlib import Path
import pandas as pd
import json


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "empresas_limpio.csv"
RESULTADO_PATH = BASE_DIR / "data" / "processed" / "lider.json"

COL_INGRESOS_2018 = "INGRESOS OPERACIONALES 2018"



def concentration_ratio(df: pd.DataFrame, value_col: str, top_pct: float = 0.1) -> float:
    """
    Calcula qué porcentaje del total de `value_col` es generado por
    el top_pct de empresas (ej. 0.1 = top 10%).
    """
    df_ordenado = df.sort_values(value_col, ascending=False)
    n_top = max(1, round(len(df_ordenado) * top_pct))

    total = df_ordenado[value_col].sum()
    total_top = df_ordenado.head(n_top)[value_col].sum()

    return round((total_top / total) * 100, 2)

if __name__ == "__main__":
    df = pd.read_csv(PROCESSED_PATH)

    with open(RESULTADO_PATH, "r", encoding="utf-8") as f:
        resultado = json.load(f)

    macrosector_lider = resultado["macrosector_lider"]
    region_lider = resultado["region_lider"]

    # Filtramos al grupo líder identificado en el paso 2
    df_grupo = df[
        (df["MACROSECTOR"] == macrosector_lider)
        & (df["REGIÓN"] == region_lider)
    ]

    print(f"=== Concentración dentro de {macrosector_lider} en {region_lider} ===")
    print(f"Total de empresas en el grupo: {len(df_grupo)}\n")

    for pct in [0.1, 0.2]:
        n_empresas = max(1, round(len(df_grupo) * pct))
        ratio = concentration_ratio(df_grupo, COL_INGRESOS_2018, top_pct=pct)
        print(
            f"El top {int(pct*100)}% de empresas ({n_empresas} empresas) "
            f"genera el {ratio}% de los ingresos del grupo"
        )
        
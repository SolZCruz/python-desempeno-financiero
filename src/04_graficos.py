"""
04_graficos.py

Genera las 6 gráficas del proyecto, cada una ligada a un paso del análisis.
Contiene tanto las funciones de graficación como el bloque de ejecución
que las llama en orden. Guarda los .png en reports/figures/.

Ejecutar directamente este script:
    python src/04_graficos.py
"""

import sys
from pathlib import Path
from importlib import import_module

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# Permite importar los módulos numerados (01, 02, 03) sin problema
sys.path.append(str(Path(__file__).resolve().parent))

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "empresas_limpio.csv"
FIGURES_DIR = BASE_DIR / "figures"

COL_INGRESOS_2018 = "INGRESOS OPERACIONALES 2018"
COL_GANANCIA_2018 = "GANANCIA (PERDIDA) 2018"
COL_NOMBRE = "RAZON SOCIAL"

COLOR_PRINCIPAL = "#7b2cbf"
COLOR_SECUNDARIO = "#dd2c45"


def _guardar(fig, save_path):
    if save_path:
        fig.savefig(save_path, bbox_inches="tight", dpi=150)
        print(f"Gráfico guardado en: {save_path}")


# ---------------------------------------------------------------------
# Funciones de graficación
# ---------------------------------------------------------------------

def plot_growth_by_macrosector(resumen: pd.DataFrame, save_path: str = None):
    """
    Gráfico 1: barras comparando % de crecimiento de ingresos y ganancia
    por macrosector (2017 -> 2018). Responde la pregunta principal:
    ¿qué macrosector tuvo el mejor desempeño?
    """
    resumen = resumen.sort_values("crecimiento_ingresos_%", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    x = range(len(resumen))
    width = 0.35

    ax.bar([i - width/2 for i in x], resumen["crecimiento_ingresos_%"],
           width, label="Crecimiento ingresos %", color=COLOR_PRINCIPAL)
    ax.bar([i + width/2 for i in x], resumen["crecimiento_ganancia_%"],
           width, label="Crecimiento ganancia %", color=COLOR_SECUNDARIO)

    ax.set_xticks(list(x))
    ax.set_xticklabels(resumen["MACROSECTOR"], rotation=45, ha="right")
    ax.set_ylabel("% de crecimiento 2017 -> 2018")
    ax.set_title("Crecimiento por macrosector (2017 -> 2018)")
    ax.legend()
    ax.yaxis.grid(True, linestyle="-", alpha=.15)
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


def plot_region_distribution(resumen_region: pd.DataFrame, macrosector: str, save_path: str = None):
    """
    Gráfico 2: ingresos 2018 por región dentro del macrosector líder.
    Responde: ¿dónde se concentra ese liderazgo?
    """
    resumen_region = resumen_region.sort_values("ingresos_2018", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(resumen_region["REGIÓN"], resumen_region["ingresos_2018"], color=COLOR_PRINCIPAL)
    ax.set_xlabel("Región")
    ax.set_ylabel("Ingresos 2018")
    ax.set_title(f"Ingresos 2018 por región — {macrosector}")
    ax.yaxis.grid(True, linestyle="-", alpha=.15)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


def plot_income_boxplot_by_macrosector(df: pd.DataFrame, income_col: str, save_path: str = None):
    """
    Gráfico 3 (contexto): boxplot de ingresos por macrosector, todos los
    sectores. Justifica por qué se usa % de crecimiento y no el total:
    hay sectores con alta dispersión (pocas empresas gigantes) vs otros
    más homogéneos.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    sb.boxplot(data=df, x=income_col, y="MACROSECTOR", orient="h", ax=ax, color=COLOR_PRINCIPAL)
    ax.set_xlabel("Ingresos 2018")
    ax.set_ylabel("Macrosector")
    ax.set_title("Distribución de ingresos por macrosector (2018)")
    ax.xaxis.grid(True, linestyle="-", alpha=.15)
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


def plot_top_companies(df_grupo: pd.DataFrame, income_col: str, name_col: str,
                        top_n: int = 10, save_path: str = None):
    """
    Gráfico 4: top N empresas del grupo líder por ingresos 2018.
    Le pone nombre a la concentración encontrada en el paso 3.
    """
    top = df_grupo.sort_values(income_col, ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(top[name_col], top[income_col], color=COLOR_SECUNDARIO)
    ax.invert_yaxis()
    ax.set_xlabel("Ingresos 2018")
    ax.set_title(f"Top {top_n} empresas por ingresos 2018 (grupo líder)")
    ax.xaxis.grid(True, linestyle="-", alpha=.15)
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


def plot_income_vs_profit(df_grupo: pd.DataFrame, income_col: str, profit_col: str, save_path: str = None):
    """
    Gráfico 5: dispersión ingresos vs ganancia de las empresas del grupo
    líder. Matiza la concentración: ¿las empresas más grandes son
    también las más rentables?
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df_grupo[income_col], df_grupo[profit_col], color=COLOR_PRINCIPAL, alpha=0.7)
    ax.set_xlabel("Ingresos 2018")
    ax.set_ylabel("Ganancia 2018")
    ax.set_title("Ingresos vs. Ganancia — empresas del grupo líder")
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.grid(True, linestyle="-", alpha=.15)
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


def plot_concentration_curve(df_grupo: pd.DataFrame, value_col: str, save_path: str = None):
    """
    Gráfico 6: curva de concentración (tipo Lorenz simplificada).
    Visualiza el % acumulado de ingresos vs % acumulado de empresas,
    ordenadas de mayor a menor ingreso. Es la evidencia visual del
    hallazgo de concentración del paso 3.
    """
    df_ordenado = df_grupo.sort_values(value_col, ascending=False).reset_index(drop=True)

    pct_empresas = (df_ordenado.index + 1) / len(df_ordenado) * 100
    pct_ingresos_acumulado = df_ordenado[value_col].cumsum() / df_ordenado[value_col].sum() * 100

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(pct_empresas, pct_ingresos_acumulado, color=COLOR_SECUNDARIO, linewidth=2, label="Concentración real")
    ax.plot([0, 100], [0, 100], color="grey", linestyle="--", label="Distribución equitativa")

    ax.set_xlabel("% acumulado de empresas")
    ax.set_ylabel("% acumulado de ingresos")
    ax.set_title("Curva de concentración de ingresos — grupo líder")
    ax.legend()
    ax.grid(True, linestyle="-", alpha=.15)
    plt.tight_layout()

    _guardar(fig, save_path)
    plt.show()


# ---------------------------------------------------------------------
# Ejecución: genera las 6 gráficas usando los pasos 1-3 del proyecto
# ---------------------------------------------------------------------

if __name__ == "__main__":
    macrosector_mod = import_module("02_desempeno_macrosector")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(PROCESSED_PATH)

    # --- Paso 2: desempeño por macrosector ---
    resumen_macrosectores = macrosector_mod.growth_by_macrosector(df)
    macrosector_lider = resumen_macrosectores.iloc[0]["MACROSECTOR"]
    resumen_region = macrosector_mod.top_region_by_macrosector(df, macrosector_lider)
    region_lider = resumen_region.iloc[0]["REGIÓN"]

    # --- Grupo líder (macrosector + región) para los gráficos 3-6 ---
    df_grupo = df[
        (df["MACROSECTOR"] == macrosector_lider) & (df["REGIÓN"] == region_lider)
    ]

    plot_growth_by_macrosector(
        resumen_macrosectores,
        save_path=FIGURES_DIR / "01_crecimiento_por_macrosector.png",
    )

    plot_region_distribution(
        resumen_region, macrosector_lider,
        save_path=FIGURES_DIR / "02_distribucion_regional.png",
    )

    plot_income_boxplot_by_macrosector(
        df, COL_INGRESOS_2018,
        save_path=FIGURES_DIR / "03_boxplot_ingresos_macrosector.png",
    )

    plot_top_companies(
        df_grupo, COL_INGRESOS_2018, COL_NOMBRE, top_n=10,
        save_path=FIGURES_DIR / "04_top_empresas.png",
    )

    plot_income_vs_profit(
        df_grupo, COL_INGRESOS_2018, COL_GANANCIA_2018,
        save_path=FIGURES_DIR / "05_ingresos_vs_ganancia.png",
    )

    plot_concentration_curve(
        df_grupo, COL_INGRESOS_2018,
        save_path=FIGURES_DIR / "06_curva_concentracion.png",
    )

    print("\nTodas las gráficas se generaron en:", FIGURES_DIR)
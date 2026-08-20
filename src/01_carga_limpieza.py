"""
01_carga_limpieza.py

Carga y limpieza del dataset de las 1000 empresas más grandes de Colombia.

Ejecutar directamente este script:
    python src/01_carga_y_limpieza.py

Lee desde data/raw/1000_empresas.csv y guarda el resultado limpio en
data/processed/empresas_limpio.csv
"""

from pathlib import Path
import pandas as pd

# Rutas del proyecto, relativas a este archivo (funcionan sin importar
# desde qué carpeta ejecutes el script)
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "1000_empresas.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "empresas_limpio.csv"


def load_raw_data(path: Path) -> pd.DataFrame:
    """
    Carga el CSV crudo desde la ruta indicada.

    Parameters
    ----------
    path : Path
        Ruta al archivo CSV.

    Returns
    -------
    pd.DataFrame
    """
    return pd.read_csv(path)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza los nombres de columnas: elimina saltos de línea,
    asteriscos y espacios extra.
    """
    df = df.copy()
    df.columns = (
        df.columns
        .str.replace("\n", " ", regex=False)
        .str.replace("*", "", regex=False)
        .str.strip()
    )
    return df


def load_and_clean(path: Path) -> pd.DataFrame:
    """
    Pipeline completo: carga + limpieza de nombres de columnas.
    Punto de entrada principal para el resto del proyecto.
    """
    df = load_raw_data(path)
    df = clean_column_names(df)
    return df


if __name__ == "__main__":
    df_limpio = load_and_clean(RAW_PATH)

    # Crea la carpeta processed si no existe
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_limpio.to_csv(PROCESSED_PATH, index=False)
    print(f"Dataset limpio guardado en: {PROCESSED_PATH}")
    print(f"Filas: {len(df_limpio)}, Columnas: {len(df_limpio.columns)}")

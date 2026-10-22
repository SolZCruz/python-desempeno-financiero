**Español** | [English](README.en.md)

# Análisis Financiero de las 1000 Empresas más Grandes de Colombia

Análisis exploratorio en Python (pandas, seaborn, matplotlib) sobre el desempeño financiero de las 1000 empresas más grandes de Colombia, comparando los años 2017 y 2018.

## Fuente de datos

[Datos Abiertos Colombia — 1000 Empresas más grandes del país](https://siis.ia.supersociedades.gov.co/MilEmpresas/index.html#/)

Información financiera individual (no consolidada) de empresas supervisadas por la Superintendencia de Sociedades, Superintendencia Financiera, Superintendencia Nacional de Salud, Superintendencia de Servicios Públicos y Superintendencia de Vigilancia y Seguridad Privada.

## Pregunta de análisis

**¿Qué macrosector tuvo el mejor desempeño financiero entre 2017 y 2018, y qué región concentra ese desempeño?**

Como cierre, se evalúa un punto de análisis de riesgo/concentración:

**¿Qué tan concentrado está ese desempeño en pocas empresas dentro del macrosector y región líderes?**

## Estructura del proyecto

La estructura sigue el orden del análisis, no una división técnica genérica: cada script en `src/` corresponde a un paso de la pregunta de negocio.

```
python-empresas-colombia-analytics/
├── data/
│   ├── raw/                        # Dataset original, sin modificar (no versionado)
│   └── processed/                  # Dataset limpio, listo para análisis (no versionado)
├── figures/                        # Gráficos exportados (.png), usados en resultados.md
├── src/
│   ├── 01_carga_y_limpieza.py      # Paso 1: carga y limpieza de columnas
│   ├── 02_desempeno_macrosector.py # Paso 2 y 3: crecimiento por macrosector + región líder
│   ├── 03_concentracion.py         # Paso 4: concentración empresarial (cierre)
│   └── 04_graficos.py              # Funciones de graficación + genera las 6 gráficas al ejecutarse
├── venv/                           # Entorno virtual (no versionado)
├── .gitignore
├── README.md
├── requirements.txt
└── resultados.md                   # Análisis y conclusiones (gráficas + texto, sin código)
```

## Flujo del análisis

| Paso | Script | Pregunta que responde |
|------|--------|------------------------|
| 1 | `01_carga_limpieza.py` | Datos limpios y consistentes, listos para analizar |
| 2 | `02_desempeno_macrosector.py` | ¿Qué macrosector tuvo el mejor desempeño 2017→2018? |
| 3 | `02_desempeno_macrosector.py` | ¿En qué región se concentra ese macrosector líder? |
| 4 | `03_concentracion.py` | Dentro de ese macrosector/región, ¿el desempeño depende de pocas empresas? |
| 5 | `04_graficos.py` | Visualización de los 4 pasos anteriores (6 gráficas) |
| 6 | `informe.md` | Conclusiones y limitaciones |

## Cómo ejecutar

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Coloca el archivo CSV del dataset en `data/raw/` y ejecuta los scripts en `src/` en orden (01 → 02 → 03 → 04). El resultado final, con gráficas y conclusiones, está en `informe.md`.

## Autora

Sol Zharick Cruz Ariza


[Español](README.md) | **English**

# Financial Analysis of the 1,000 Largest Companies in Colombia

Exploratory analysis in Python (pandas, seaborn, matplotlib) of the financial performance of the 1,000 largest companies in Colombia, comparing the years 2017 and 2018.

## Data source

[Open Data Colombia — 1,000 Largest Companies in the Country](https://siis.ia.supersociedades.gov.co/MilEmpresas/index.html#/)

Individual (non-consolidated) financial information of companies supervised by the Superintendencia de Sociedades (Superintendence of Companies), the Superintendencia Financiera (Financial Superintendence), the Superintendencia Nacional de Salud (National Health Superintendence), the Superintendencia de Servicios Públicos (Public Utilities Superintendence) and the Superintendencia de Vigilancia y Seguridad Privada (Private Security and Surveillance Superintendence).

## Analysis question

**Which macro-sector had the best financial performance between 2017 and 2018, and which region concentrates that performance?**

As a closing step, a risk/concentration point is evaluated:

**How concentrated is that performance in a few companies within the leading macro-sector and region?**

## Project structure

The structure follows the order of the analysis, not a generic technical split: each script in `src/` corresponds to one step of the business question.

```
python-empresas-colombia-analytics/
├── data/
│   ├── raw/                        # Original dataset, unmodified (not versioned)
│   └── processed/                  # Clean dataset, ready for analysis (not versioned)
├── figures/                        # Exported charts (.png), used in the results documents
├── src/
│   ├── 01_carga_y_limpieza.py      # Step 1: loading and column cleaning
│   ├── 02_desempeno_macrosector.py # Steps 2 and 3: growth by macro-sector + leading region
│   ├── 03_concentracion.py         # Step 4: corporate concentration (closing)
│   └── 04_graficos.py              # Plotting functions + generates the 6 charts when run
├── venv/                           # Virtual environment (not versioned)
├── .gitignore
├── README.md                       # Spanish version
├── README.en.md                    # English version
├── requirements.txt
├── resultados.md                   # Analysis and conclusions (charts + text, no code) — Spanish
└── resultados.en.md                # Analysis and conclusions (charts + text, no code) — English
```

## Analysis flow

| Step | Script | Question it answers |
|------|--------|---------------------|
| 1 | `01_carga_y_limpieza.py` | Clean, consistent data, ready to analyze |
| 2 | `02_desempeno_macrosector.py` | Which macro-sector had the best performance 2017→2018? |
| 3 | `02_desempeno_macrosector.py` | In which region is that leading macro-sector concentrated? |
| 4 | `03_concentracion.py` | Within that macro-sector/region, does performance depend on a few companies? |
| 5 | `04_graficos.py` | Visualization of the 4 previous steps (6 charts) |
| 6 | `resultados.en.md` | Conclusions and limitations |

## How to run

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Place the dataset's CSV file in `data/raw/` and run the scripts in `src/` in order (01 → 02 → 03 → 04). The final result, with charts and conclusions, is in [`resultados.en.md`](resultados.en.md).

## Author

Sol Zharick Cruz Ariza

# Minería de datos para decisiones comerciales

Proyecto del Segundo Examen de INF432 — Sistemas para el Soporte a la Toma de
Decisiones (UAGRM). Aplica CRISP-DM a RetailMarket Santa Cruz, una empresa
hipotética, en tres áreas de negocio.

| Área | Pregunta de negocio | Tipo | Notebook |
|---|---|---|---|
| A2. Segmentación de mercado | ¿Qué grupos de clientes existen y qué estrategia merece cada uno? | No supervisado | `01_Area_A2_Segmentacion.ipynb` |
| A1. Campañas de marketing | ¿A qué clientes contactar en la próxima campaña con presupuesto limitado? | Supervisado | `02_Area_A1_Marketing.ipynb` |
| A5. Nuevos nichos | ¿Hay grupos pequeños o casos aislados que la segmentación general no muestra? | No supervisado | `03_Area_A5_Nichos.ipynb` |

## Integrantes

1. Diogo Nicolas Rodríguez Gómez (221045686): datos y A1.
2. Yossy Carmelita Yanma Villarroel (217182844): A2.
3. [Completar nombre y registro]: A5 y evaluación.

## Cómo ejecutar

Requiere Python 3.12. Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Abre los notebooks en VS Code o Jupyter, elige el entorno `.venv` y ejecuta cada
uno con **Restart & Run All**, **en este orden**:

1. `00_Datos.ipynb`: genera los datos preparados que usan los demás.
2. `01_Area_A2_Segmentacion.ipynb`: genera los segmentos que usa A5.
3. `02_Area_A1_Marketing.ipynb`
4. `03_Area_A5_Nichos.ipynb`: tarda cerca de dos minutos.

Todas las rutas son relativas y la semilla es 1, así que los resultados se repiten.

Para revisar la calidad de los datos preparados:

```powershell
python verificacion_auditoria_datos.py
```

## Versiones

Python 3.12 y las librerías fijadas en `requirements.txt`: numpy 2.4.1, pandas
3.0.0, matplotlib 3.10.8, seaborn 0.13.2, scikit-learn 1.8.0, scipy 1.17.0,
ipython 9.9.0 e ipykernel 6.31.0.

## Estructura

- `data/raw/`: datos originales, sin modificar.
- `data/processed/`: datos preparados y asignaciones de A2 y A5.
- `reports/figures/`: figuras para el documento y las diapositivas.
- `reports/tables/`: tablas de resultados.
- `docs/`: notas para el equipo.

## Fuente de datos

Patel, A. (2021). *Customer Personality Analysis* [Conjunto de datos]. Kaggle.
https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis

Licencia: CC0: Public Domain. El archivo pesa cerca de 220 KB y está incluido en
`data/raw/marketing_campaign.csv`.

Los datos provienen del reto *iFood CRM Data Analyst Case* y son simulados: sirven
para aplicar el proceso, pero no describen a una empresa real.

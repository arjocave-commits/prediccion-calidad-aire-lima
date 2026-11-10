Análisis y predicción horaria de PM2.5 en Lima mediante Python, Machine Learning, SQL Server y Power BI.


Análisis y predicción de la calidad del aire en Lima

##Descripción

Proyecto de análisis de datos y Machine Learning enfocado en estudiar la contaminación atmosférica por material particulado fino (PM2.5) en Lima, Perú.

Se analizaron registros históricos de estaciones de monitoreo durante el periodo 2015–2024, con especial énfasis en San Juan de Lurigancho (SJL).

El objetivo principal fue identificar patrones de contaminación y desarrollar un modelo capaz de predecir la concentración de PM2.5 una hora después.

## Tecnologías utilizadas

- Python: Pandas, NumPy y Scikit-learn
- SQL Server: almacenamiento y consultas
- Power BI: visualización y dashboards
- Git y GitHub: control de versiones

## Metodología

1. Exploración de datos históricos de PM2.5.
3. Limpieza y preparación de series temporales.
4. Creación de variables temporales, rezagos y medias móviles.
5. Entrenamiento y evaluación de modelos predictivos.
6. Análisis mediante SQL Server.
7. Construcción de dashboards interactivos en Power BI.

## Resultados del Machine Learning

Se compararon cuatro enfoques para predecir PM2.5 una hora después.

Comparando el MAE Y el RMSE por modelo predictivo
| Baseline (persistencia) | 4.67 | 6.79 |
| Regresión lineal | 4.36 | 6.34 |
| Random Forest | 4.34 | 6.23 |
| Random Forest sin PM2.5 actual | 6.73 | 9.50 |

Random Forest obtuvo los menores errores, aunque su ventaja frente a la regresión lineal fue pequeña.

## Hallazgos principales

- Se identificaron diferencias en los niveles de contaminación entre estaciones y periodos.
- Se observaron patrones horarios y anuales de PM2.5.
- La concentración actual de PM2.5 fue la variable más influyente en Random Forest.
- Los cambios bruscos de contaminación representaron una dificultad para los modelos predictivos.

VISUALIZADO EN POWER BY 

## Limitaciones

- Los registros presentan periodos sin mediciones.
- Los datos de 2024 no abarcan el año completo.
- El modelo se desarrolló para SJL y no debe generalizarse automáticamente a otras estaciones.
- Las predicciones corresponden únicamente a una hora de anticipación.
- Los umbrales descriptivos utilizados en el dashboard no representan necesariamente categorías oficiales de calidad del aire.

## Estructura del repositorio

- `src/`: análisis, procesamiento y modelos predictivos.
- `sql/`: consultas de SQL Server.
- `dashboard/`: archivo Power BI y capturas de pantalla.

## Autor

Jorge Capcha Vertiz  
Estudiante de Ingeniería Industrial  
Interesado en Data Analytics, Machine Learning y automatización.

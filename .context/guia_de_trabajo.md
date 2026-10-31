================================================================================
GUÍA DE TRABAJO Y PROMPT DE CONTEXTO - PROYECTO INF432 (UAGRM)
================================================================================
ESTRUCTURA DEL PROYECTO:
- Asignatura: INF432 - Sistemas para el Soporte a la Toma de Decisiones.
- Metodología: CRISP-DM (Negocio, Datos, Preparación, Modelado, Evaluación, Despliegue).
- Repositorio Git: Código estructurado con rutas relativas a 'data/raw/' y 'data/processed/'.
- Semilla global: SEMILLA = 1 en todos los modelos y splits (70% train / 30% test).
- Regla de oro: No data leakage. El preprocesamiento y escalado (StandardScaler) 
  se aprende en Train y se aplica en Test.

DATASET SELECCIONADO:
- Customer Personality Analysis (Kaggle).
- Archivo base: data/raw/marketing_campaign.csv (~2.240 filas, 29 variables).

--------------------------------------------------------------------------------
REPARTO DE ROLES Y RESPONSABILIDADES:
--------------------------------------------------------------------------------

INTEGRANTE 1: INGENIERO DE DATOS & MODELADO SUPERVISADO (ÁREA A1)
• Cuadernos asignados:
  - 00_Datos.ipynb: Carga, diagnóstico de calidad (nulos, outliers, duplicados),
    codificación, ingeniería de variables, StandardScaler y exportación a 
    'data/processed/data_limpia.csv'.
  - 02_Area_A1_Marketing.ipynb: Clasificación supervisada (Variable 'Response').
    Modelos: kNN, Naive Bayes y Árbol de Decisión. Optimización con GridSearchCV
    para kNN y Árbol. Matriz de confusión en Test y análisis de costo negocio (FP vs FN).
• Secciones asignadas en Word:
  - Ficha del Proyecto (Anexo A).
  - Sección 3: Entendimiento de los datos (fuentes, diccionario y calidad).
  - Sección 4: Preparación de los datos.
  - Sección 5.2: Modelado Área 1 (Campañas de Marketing).
• Diapositivas asignadas: Diapositivas 4, 5, 8 y 9.

INTEGRANTE 2: ESPECIALISTA EN CLUSTERING & NEGOCIO (ÁREA A2)
• Cuaderno asignado:
  - 01_Area_A2_Segmentacion.ipynb: Segmentación no supervisada.
    Lectura desde 'data/processed/data_limpia.csv'.
    PCA obligatorio (varianza explicada, gráfico 2D, cargas principales).
    k-means con justificación de K mediante curva de silueta y criterio de negocio.
    Clustering Jerárquico con dendrograma para comparar.
    Perfilado de clústeres en unidades originales (groupby mean) y nombres comerciales.
• Secciones asignadas en Word:
  - Sección 1: Introducción y objetivos comerciales.
  - Sección 2: Entendimiento del negocio (preguntas, decisores y criterios de éxito).
  - Sección 5.1: Modelado Área 2 (Segmentación de Clientes).
  - Sección 7: Despliegue y plan de monitoreo.
• Diapositivas asignadas: Diapositivas 1, 2, 3, 6 y 7.

INTEGRANTE 3: ESPECIALISTA EN NICHOS & EVALUACIÓN (ÁREA A5)
• Cuaderno asignado:
  - 03_Area_A5_Nichos.ipynb: Detección de nichos y atípicos.
    Lectura desde 'data/processed/data_limpia.csv'.
    Reducción con t-SNE comparado frente a PCA.
    Algoritmo DBSCAN para identificar grupos densos pequeños y casos aislados (ruido).
    Perfilado de los nichos encontrados.
    Verificación final de reproducibilidad (Restart & Run All en todos los notebooks).
• Secciones asignadas en Word:
  - Resumen Ejecutivo (redactado al final para gerencia).
  - Sección 5.3: Modelado Área 3 (Nuevos Nichos).
  - Sección 6: Evaluación frente a criterios de éxito y análisis ético/sesgos.
  - Sección 8: Conclusiones y trabajo futuro.
  - Anexo B: Declaración de uso de herramientas de IA y fuentes.
• Diapositivas asignadas: Diapositivas 10, 11, 12, 13, 14, 15 y 16.
================================================================================
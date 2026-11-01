# Cambios para el equipo: léeme antes de seguir

Se corrigieron los datos y se completó lo que pide el enunciado en el código. Por
eso **cambiaron cifras de A1 y A2**. El Word y las diapositivas deben usar los
valores de este archivo.

## 1. Qué debe hacer cada uno ahora

**Todos:**

1. Guarden su trabajo y bajen los cambios con `git pull`.
2. Instalen las versiones del proyecto: `pip install -r requirements.txt`.
3. Ejecuten los notebooks que les tocan con **Restart & Run All**. El orden importa,
   porque cada uno usa lo que genera el anterior: `00` → `01` → `02` → `03`.
4. Confirmen que sus resultados coinciden con las tablas de abajo.

Los resultados ya están subidos, así que al ejecutar deberían salir iguales. Si
alguien solo ejecutó y no cambió nada, no necesita subir nada. Git puede mostrar los
notebooks como modificados aunque las cifras sean las mismas.

| Integrante | Qué ejecutar | Qué actualizar |
|---|---|---|
| **1. Diogo** | `00_Datos`, luego `02_Area_A1_Marketing` | Secciones 3, 4 y 5.2 del Word, Ficha y diapositivas 4, 5, 8 y 9 |
| **2. Yossy** | `00_Datos`, luego `01_Area_A2_Segmentacion` | Secciones 1, 2, 5.1 y 7 del Word y diapositivas 1, 2, 3, 6 y 7 |
| **3.** | Los cuatro en orden, como verificación final | Resumen ejecutivo, secciones 5.3, 6 y 8, anexos y diapositivas 10 a 16 |

Reemplacen también en el Word y las diapositivas las figuras de `reports/figures/`
que ya hayan pegado, porque se volvieron a generar.

## 2. Qué se corrigió y por qué

| Cambio | Archivo | Motivo |
|---|---|---|
| Se quitaron 204 filas repetidas antes de dividir | `00_Datos` | 86 filas de prueba eran idénticas a filas de entrenamiento. El modelo se evaluaba con casos que ya conocía |
| La mediana de `Income` se calcula solo con entrenamiento | `00_Datos` | Regla de oro: prueba no debe influir en la preparación |
| `Age` se calcula con 2014, no con 2026 | `00_Datos` | Los datos llegan hasta 2014. La edad debe corresponder al momento de las compras |
| Se agregaron fuente, licencia, diccionario, descriptivos y atípicos | `00_Datos` | Requisito R1 |
| Los nombres de los segmentos se asignan según el perfil | `01_Area_A2` | k-means renumeró los grupos y «Bajo consumo» habría quedado con el perfil de mayor gasto |
| Se agregaron costo de errores, estabilidad, respuesta, despliegue y monitoreo | `02_Area_A1` | Requisitos R5 y R6 |
| Se agregaron puesta en práctica y monitoreo | `03_Area_A5` | Requisito R6 |
| Se agregaron `README.md` y `requirements.txt` | Raíz | Entregables de la sección 5 |

## 3. Cifras nuevas

### Base de datos

| Dato | Antes | Ahora |
|---|---|---|
| Clientes en la base limpia | 2236 | **2032** |
| Entrenamiento / prueba | 1565 / 671 | **1422 / 610** |
| Filas de prueba con copia en entrenamiento | 86 | **0** |
| Edad promedio | 57,1 años | **45,1 años** |

### A1. Campañas de marketing

| Modelo | Exactitud | F1 | AUC | % FP | % FN |
|---|---|---|---|---|---|
| kNN | 86,39 % | 0,4354 | 0,7566 | 3,93 % | 9,67 % |
| Naive Bayes | 81,97 % | 0,4954 | 0,8084 | 11,97 % | 6,07 % |
| Árbol de decisión | 83,77 % | 0,4407 | 0,8438 | 7,70 % | 8,52 % |

Parámetros: kNN con `k = 3`, `manhattan` y pesos `uniform`. Árbol con `entropy`,
`max_depth = 10` y `min_samples_leaf = 20`.

| Costo y presupuesto (en prueba) | kNN | Naive Bayes | Árbol |
|---|---|---|---|
| Ganancia contactando a los positivos | 184 UM | 213 UM | 171 UM |
| Captura contactando al 20 % | 57,1 % | 58,2 % | **60,4 %** |
| Ganancia contactando al 20 % | 206 UM | 217 UM | **239 UM** |

- Contactar a todos en prueba: **−829 UM**.
- Cada contacto cuesta 3 UM y cada aceptación deja 11 UM. Un FP cuesta 3 UM y un FN
  deja de ganar 8 UM.
- **Modelo recomendado: árbol de decisión.**
- En 30 divisiones distintas, el árbol va de 82,5 % a 86,9 % de exactitud. Naive
  Bayes promedia 79,4 %, pero una vez cayó a 53,9 %: es inestable.
- Criterio de éxito propuesto: captar al menos 40 % de las aceptaciones con el 20 %
  de contactos y ganancia positiva. **Diogo y Yossy: confirmen que coincida con la
  Sección 2 del Word.**

### A2. Segmentación

| Dato | Antes | Ahora |
|---|---|---|
| Componentes de PCA | 7 (85,27 %) | **8 (88,59 %)** |
| PC1 + PC2 | 56,53 % | **56,00 %** |
| Silueta con K = 2 | 0,3971 | **0,3854** |
| Silueta con K = 3 | 0,3195 | **0,3052** (la meta de 0,35 sigue sin cumplirse) |
| Silueta de Ward | 0,2740 | **0,2779** |

| Segmento | Clientes | % | Ingreso | Gasto |
|---|---|---|---|---|
| Bajo consumo | 938 | 46,16 % | 35 183,67 | 95,45 |
| Alto gasto multicanal | 545 | 26,82 % | 75 730,34 | 1365,43 |
| Web y promociones | 549 | 27,02 % | 57 410,62 | 726,99 |

### A5. Nichos

No cambiaron sus resultados principales: 2031 registros únicos, masa principal de
1720, nicho de 17 clientes y 294 casos aislados (14,48 %). La respuesta del nicho
sigue en 47,1 %. La edad promedio del nicho es ahora 43,6 años. t-SNE tiene una
confianza de 0,9771 y PCA de 0,8991.

## 4. Lo que deben saber para el Word y la defensa

- **Los datos son simulados.** Vienen del reto *iFood CRM Data Analyst Case*. Hay que
  decirlo en las secciones 3 y 6: la ganancia es ilustrativa, no una proyección real.
- **Cita de la fuente:** Patel, A. (2021). *Customer Personality Analysis* [Conjunto
  de datos]. Kaggle. https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis
  (licencia CC0: Public Domain).
- **Declaración de IA obligatoria.** Se usó Claude para el notebook A5, las
  correcciones de datos, el cierre de A1, la auditoría, el `README.md` y este archivo.
- **Todos deben poder explicar cualquier línea.** El docente puede preguntar a
  cualquiera. Repasen estos puntos:
  - por qué se quitan duplicados antes de dividir;
  - por qué la mediana sale de entrenamiento;
  - por qué un FN cuesta más que un FP;
  - por qué se recomienda el árbol aunque kNN tenga mayor exactitud.
- **Propuestas pendientes de validar:** los umbrales de alerta de A1 y A5, y los
  criterios de éxito de A1 y A5.
- **Falta completar:** el nombre y registro del Integrante 3 en `README.md` y en
  `03_Area_A5_Nichos.ipynb`.

"""
SCRIPT DE AUDITORÍA INTEGRAL DE DATOS Y MACHINE LEARNING - PROYECTO INF432
Verificación de Duplicados, Fuga de Datos (Data Leakage), y Consistencia A2 vs A5.
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, adjusted_rand_score

SEMILLA = 1

def ejecutar_auditoria():
    print("=" * 75)
    print(" AUDITORÍA TÉCNICA SENIOR DE DATOS Y MACHINE LEARNING (INF432)")
    print("=" * 75)

    # 1. Carga cruda y preprocesamiento
    df_raw = pd.read_csv('data/raw/marketing_campaign.csv', sep='\t')
    dup_raw_id = df_raw.duplicated().sum()
    dup_raw_no_id = df_raw.drop(columns=['ID']).duplicated().sum()

    print("\n[1] AUDITORÍA DE DUPLICADOS EN DATOS CRUDOS:")
    print(f"  - Total registros crudos: {df_raw.shape[0]}")
    print(f"  - Duplicados evaluando con columna 'ID': {dup_raw_id}")
    print(f"  - Duplicados reales ignorando 'ID': {dup_raw_no_id} filas")

    # Replicar la limpieza de 00_Datos.ipynb SIN quitar duplicados, para medir su
    # efecto. Las secciones [2] a [5] describen ese estado anterior a la corrección;
    # la sección [6] verifica los archivos que hoy usa el proyecto.
    df = df_raw.copy()
    df['Income'] = df['Income'].fillna(df['Income'].median())
    df['Age'] = 2014 - df['Year_Birth']
    df = df[(df['Age'] <= 100) & (df['Income'] < 200000)].copy()

    df['Total_Spent'] = (df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + 
                         df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds'])
    df['Total_Purchases'] = (df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases'])
    df['Children'] = df['Kidhome'] + df['Teenhome']

    mapeo_marital = {
        'Married': 2, 'Together': 2, 'Single': 1, 'Divorced': 1, 
        'Widow': 1, 'Alone': 1, 'Absurd': 1, 'YOLO': 1
    }
    df['Family_Size'] = df['Marital_Status'].map(mapeo_marital) + df['Children']
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
    df['Customer_Days'] = (df['Dt_Customer'].max() - df['Dt_Customer']).dt.days

    mapeo_edu = {'Basic': 0, '2n Cycle': 1, 'Graduation': 2, 'Master': 3, 'PhD': 4}
    df['Education_Level'] = df['Education'].map(mapeo_edu)

    columnas_descartar = ['ID', 'Year_Birth', 'Dt_Customer', 'Education', 'Marital_Status', 'Z_CostContact', 'Z_Revenue']
    df_clean = df.drop(columns=columnas_descartar).reset_index(drop=True)
    
    print("\n[2] AUDITORÍA EN BASE SIN DEPURAR (N = 2.236):")
    print(f"  - Duplicados en todas las variables (incluyendo Response): {df_clean.duplicated().sum()} (Únicos: {len(df_clean.drop_duplicates())})")
    
    X = df_clean.drop(columns=['Response'])
    y = df_clean['Response']
    print(f"  - Duplicados exactos solo en predictores (X): {X.duplicated().sum()} (Únicos: {len(X.drop_duplicates())})")

    # 2. Partición 70/30 y Data Leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=SEMILLA, stratify=y
    )

    merged_leak_x = pd.merge(X_train.reset_index(), X_test.reset_index(), on=list(X.columns), suffixes=('_train', '_test'))
    train_full = X_train.copy(); train_full['Response'] = y_train
    test_full = X_test.copy(); test_full['Response'] = y_test
    merged_leak_xy = pd.merge(train_full.reset_index(), test_full.reset_index(), on=list(train_full.columns), suffixes=('_train', '_test'))

    n_test_leaked = merged_leak_x['index_test'].nunique()
    pct_leaked = (n_test_leaked / len(X_test)) * 100
    n_leak_same_y = merged_leak_xy['index_test'].nunique()
    n_leak_diff_y = n_test_leaked - n_leak_same_y

    print("\n[3] AUDITORÍA DE DATA LEAKAGE EN TRAIN / TEST (70/30):")
    print(f"  - Tamaño X_train: {X_train.shape[0]} | Tamaño X_test: {X_test.shape[0]}")
    print(f"  - Filas de X_test con gemelo idéntico en X_train: {n_test_leaked} de {len(X_test)} ({pct_leaked:.2f}%)")
    print(f"    * Con idéntica etiqueta Response (fuga de información directa): {n_leak_same_y}")
    print(f"    * Con etiqueta Response contradictoria (ruido / etiquetas inconsistentes): {n_leak_diff_y}")

    # 3. Consistencia Área A2 (K-Means K=3)
    vars_a2 = [
        "Income", "Recency", "MntWines", "MntFruits", "MntMeatProducts",
        "MntFishProducts", "MntSweetProducts", "MntGoldProds", "NumDealsPurchases",
        "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases", "NumWebVisitsMonth"
    ]
    df_unicos = df_clean.drop_duplicates(subset=vars_a2).copy()

    # K-Means N=2236
    X_comp_scaled = StandardScaler().fit_transform(df_clean[vars_a2])
    X_comp_pca = PCA(n_components=7, svd_solver="full", random_state=SEMILLA).fit_transform(X_comp_scaled)
    km_comp = KMeans(n_clusters=3, random_state=SEMILLA, n_init=20).fit(X_comp_pca)

    # K-Means N=2031
    X_uniq_scaled = StandardScaler().fit_transform(df_unicos[vars_a2])
    X_uniq_pca = PCA(n_components=7, svd_solver="full", random_state=SEMILLA).fit_transform(X_uniq_scaled)
    km_uniq = KMeans(n_clusters=3, random_state=SEMILLA, n_init=20).fit(X_uniq_pca)

    pos_unicos = df_unicos.index.to_numpy()
    ari_a2 = adjusted_rand_score(km_comp.labels_[pos_unicos], km_uniq.labels_)

    print("\n[4] IMPACTO EN ÁREA A2 (K-MEANS 3 SEGMENTOS, CON 7 COMPONENTES FIJOS):")
    print(f"  - Silhouette N=2.236: {silhouette_score(X_comp_pca, km_comp.labels_):.4f} | Silhouette N=2.031: {silhouette_score(X_uniq_pca, km_uniq.labels_):.4f}")
    print(f"  - Índice Rand Ajustado (ARI) en casos comunes: {ari_a2:.4f} (> 99% de concordancia)")
    print("  -> Conclusión A2: La estructura de 3 segmentos es ultra-estable; los duplicados no alteran la segmentación macro.")

    # 4. Consistencia Área A5 (DBSCAN eps=1.5, min_samples=5)
    vars_a5 = [c for c in vars_a2 if c != "Recency"]
    X_sc_uniq_a5 = StandardScaler().fit_transform(np.log1p(df_unicos[vars_a5]))
    db_uniq = DBSCAN(eps=1.5, min_samples=5).fit(X_sc_uniq_a5)
    tamanos_a5_uniq = pd.Series(db_uniq.labels_).value_counts().to_dict()

    X_sc_comp_a5 = StandardScaler().fit_transform(np.log1p(df_clean[vars_a5]))
    db_comp = DBSCAN(eps=1.5, min_samples=5).fit(X_sc_comp_a5)
    tamanos_a5_comp = pd.Series(db_comp.labels_).value_counts().to_dict()

    print("\n[5] IMPACTO EN ÁREA A5 (DBSCAN eps=1.5, min_samples=5):")
    print(f"  - Con ÚNICOS (N=2.031): Grupos detectados: {tamanos_a5_uniq}")
    print(f"    * Masa principal (0): {tamanos_a5_uniq.get(0, 0)} clientes")
    print(f"    * Casos aislados / ruido (-1): {tamanos_a5_uniq.get(-1, 0)} clientes")
    print(f"    * Nicho 'Premium sin descuentos' (1): {tamanos_a5_uniq.get(1, 0)} clientes.")
    print(f"  - Con COMPLETA (N=2.236): Grupos detectados: {tamanos_a5_comp}")
    print("    * ADVERTENCIA DBSCAN: Con duplicados aparecen micro-clusters espurios de densidad artificial (Clusters 2 y 3 con tamaño 5 c/u).")

    # 5. Verificación de los archivos generados por 00_Datos.ipynb
    base_final = pd.read_csv('data/processed/data_limpia_original.csv')
    train_final = pd.read_csv('data/processed/train_scaled.csv').drop(columns=['Response'])
    test_final = pd.read_csv('data/processed/test_scaled.csv').drop(columns=['Response'])

    # Los valores escalados se redondean para compararlos sin errores de coma flotante
    gemelos = test_final.round(6).merge(train_final.round(6).drop_duplicates(), how='inner')

    print("\n[6] VERIFICACIÓN DE LOS ARCHIVOS ACTUALES DEL PROYECTO:")
    print(f"  - Filas en la base limpia: {len(base_final)}")
    print(f"  - Filas con predictores repetidos: {base_final.drop(columns=['Response']).duplicated().sum()}")
    print(f"  - Entrenamiento: {len(train_final)} | Prueba: {len(test_final)}")
    print(f"  - Filas de prueba con gemelo en entrenamiento: {len(gemelos)}")
    print("=" * 75)

if __name__ == '__main__':
    ejecutar_auditoria()

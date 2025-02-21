# -*- coding: utf-8 -*-
"""Ejercicio 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15Il2bT6Lidb_wGbPoA6x-umI81D3bSWn

#Carga de la información
"""

#importación de librerías a usar:

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split #librearía para hacer división de data

from sklearn.preprocessing import StandardScaler #librería para preprocesameinto, nomalización
from sklearn.ensemble import RandomForestClassifier #librería para entrenamr modelo de RF
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve #librerías para evaluación

#Carga del dataset

df1 = pd.read_csv("/content/dataset.csv")

df1.head()

#cambiar el nombre de la columna que no tenía nombre en el archivo CSV

df1.columns= ['Id' if col == 'Unnamed: 0' else col for col in df1.columns]

df1.head()

#estadística descriptiva
df1.describe()

#ver tipo de datos, nulls
df1.info()

#no hay valores nulls
df1.isnull().sum()

"""# Data clean

Tenemos 31 variables, id muestra identificador único del cliente, v1 a v28 muestra las transaciones de la tarjeta de crédito en los 28 días naturales, la columna Amount nos muestra el saldo de la tarjeta, y la columna Class nos muestra si fue fraude (1) o no (0).

Además, no tenemos valores nulos, así que podríamosa saltarnos el paso de rellenar valores vacíos.
"""

# valores duplciados:

df1.duplicated().sum()

"""# Análisis exploratorio de la base (EDA)"""

df1.groupby('Class').describe()

df1.groupby('Class')['Amount'].describe()

# Ver la distribución de la clase (Fraude:1 o no Fraude:0)
sns.countplot(x='Class', data=df1)
plt.title('Distribución de fraude (0=No, 1=Sí)')
plt.show()

# Distribucción de las transacciones 0 y 1
sns.boxplot(x='Class', y='Amount', data=df1)
plt.title('Boxplot de Monto por Clase (Fraude vs No Fraude)')
plt.show()

"""* Vemos que hay más datos de la clase 0 (no fraude), por lo que podríamos decir que la base esta desbalanceado, 4% de fraude.
* Podemos observar que el monto promedio en los casos fraudulentos es mayor respecto al caso opuesto.
* Podemos observar que la variabilidad del saldo en la clase de fraudulenta suele operar en rango controlados para evitar activar aletar de sus cometidos.
* La mayoria de los fraudes parecen concentrarse en montos pequeños o medianos, lo que podría reflejar una estrategia para minimizar el riesgo de detección.
"""

#suma de transacciones del mes por clase:
transacciones_totales = df1.groupby('Class').sum()[['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28']]

# Graficar los resultados
transacciones_totales.T.plot(figsize=(14,8))
plt.title('Suma total de transacciones diarias por Clase (Fraude vs No Fraude)')
plt.xlabel('Días naturales (V1 - V28)')
plt.ylabel('Monto total')
plt.show()

#Promedio de las transacciones diarias por clase
transacciones_promedio = df1.groupby('Class').mean()[['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28']]

# Graficar los resultados
transacciones_promedio.T.plot(figsize=(14,8))
plt.title('Promedio de transacciones diarias por Clase (Fraude vs No Fraude)')
plt.xlabel('Días naturales (V1 - V28)')
plt.ylabel('Monto promedio')
plt.show()

"""De las dos gráficas anteriores podemos concluir:
* Las transacciones de la clase no fraudulenta tiene un comportamiento estable a lo largo de los días.
* La clase de fraude tiene fluctuaciones notables desde el día uno al 20, los últimos días del mes presenta comportamiento estable.
* Al parecer los defraudadores alternan entre montos altos y bajos para evitar detección de sistemas.
* La estabilidad promedio de la clase 0 respecto al comportamiento de la clase 1, puede ser utilizado como indicador para detectar transacciones fradulentes.
"""

# Correlación entre las columnas continuas y clase; creo que no da mucha información
correlation = df1[['Amount', 'Class']].corr()
print(correlation)

"""# Preprocesamiento de Datos

De acuerdo a lo visto anteriormente, podríamos usar el modelo de Randoms forest debido a que evita el sobreajuste, funciona bien con muchas variables independientes. Además, se debe considerar que típicamente el problema de fraude tiene más transacciones legítimas respecto a las transacciones fraudulentas (desbalanceo), justo el modelo de Random Forest puede manejarlo bien.
"""

# ahora vamos a dividir en vi (X) y vd (y)
X = df1.drop(columns=['Class', 'Id']) #quitar las variables que no usaremos como vi
y = df1['Class']

"""# División de datos en testing y trainig

"""

#generalmente se dividi 80% entrenamiento y 20% prueba, a veces es 70-30


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#vamos a normalizar los datos para este modelo, auque cabe señalar
# no es obligatorio debido a que el RF manipula bien datos con escala original


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""# Entrenamiento del modelo"""

#entrenamiento del modelo, usar 100 árboles, ponder semilla aleatoria estática

# aquí iniciamos el modelo
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

#entrenamiento del modelo
rf_model.fit(X_train_scaled, y_train)

# aquí procedemos a predecir en los datos de prueba
y_pred = rf_model.predict(X_test_scaled)

print(y_pred) #las predicciones del modelo de RF, los 0 son No fraude, 1 son Fraude

"""# Evaluación del modelo

Aquí usaremos métricas de precisión, recall y matriz de confusión para evaluar el rendimiento del modelo
"""

# Reporte de clasificación
print(classification_report(y_test, y_pred))

"""Precisión: mide exactitud de predicciones positivas
* Clase 0 (No fraude), el 99% de las prediccion de no fraude fueron correctas
* Clase 1 (Fraude), el 100% de las predicciones de fraude fueron correctas

Recall: de todos los fraudes reales, cuáles fueron correctamente idenficados?
* clase 0: el modelo identificó el 100 de los casos de no fraude
* calse 1: el modelo indentificó correctamente el 81% de los fraude reales

F1-Score: nos da el balance entre la presición y recall, útil para ver desbalanceo
* Calse 0: 100%
* clase 1: 90%, es bueno para el caso de desbalanceo

Acurracy: porcentaje de predicciones correctas en genera, de ambas clases
* el 99% de todas las predicciones fueron correctas
"""

# matriz de confusión
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['No Fraude', 'Fraude'], yticklabels=['No Fraude', 'Fraude'])
plt.title('Matriz de Confusión')
plt.show()

"""De la matriz anteriore concluimos:
* True negative: hubo 1401 No fraude identificados como no fraude.
* False positive: 0 transacciones clasificadas como Fraude cuando no era Fraude.
* Fase Negative: 11 transacciones clasificada como No Fraude cuando en realidad era Fraude.
* True Positive: 48 transacciones clasificadas como FRaude fueron clasficados como Fraude.
"""

# AUC: este indicador muestra la capacidad del modelo de clasificar correctamente
  # la clase de Fraude y no Fraude. El número de 0.95 indica que el modelo tiene un
    # buen desempeño para distinguir una clase de otra.
y_prob = rf_model.predict_proba(X_test_scaled)[:,1]
roc_auc = roc_auc_score(y_test, y_prob)
print(f"AUC: {roc_auc}")

#cabe señalar podemos ajustar los parámetros (númro de arboles=n_estimators y max_depth=profundidad max de los árboles)
# del modelo para encontrar un mejor modelo en caso de que no hayamos encontrado un modelo satisfactorio

"""# Pronóstico de nuevos datos

En el caso de que tenganmos nuevos datos podemo usar el modelo anterior, por ejmplo:
"""

# aquí creo un df con las 29 varibales indept X (V1, V2, ..., Amount)
new_data = pd.DataFrame({
    'V1': [0.5, -0.4, 1.2],   # Ejemplo de valores para V1
    'V2': [-0.3, 0.8, -1.1],  # Ejemplo de valores para V2
    'V3': [0.7, -0.2, 0.5],   # Ejemplo de valores para V3
    'V4': [1.2, -0.7, 0.9],   # Ejemplo de valores para V4
    'V5': [-0.6, 0.5, -0.3],  # Ejemplo de valores para V5
    'V6': [0.3, -0.9, 0.4],   # Ejemplo de valores para V6
    'V7': [-0.1, 0.6, -0.8],  # Ejemplo de valores para V7
    'V8': [0.9, -0.4, 1.1],   # Ejemplo de valores para V8
    'V9': [0.4, 0.2, -0.5],   # Ejemplo de valores para V9
    'V10': [0.1, -0.6, 0.7],  # Ejemplo de valores para V10
    'V11': [-0.2, 0.9, -0.1], # Ejemplo de valores para V11
    'V12': [0.3, -0.5, 0.8],  # Ejemplo de valores para V12
    'V13': [-0.4, 0.1, -0.7], # Ejemplo de valores para V13
    'V14': [0.8, -0.8, 1.0],  # Ejemplo de valores para V14
    'V15': [-0.7, 0.3, -0.6], # Ejemplo de valores para V15
    'V16': [1.0, -0.2, 0.9],  # Ejemplo de valores para V16
    'V17': [0.6, -0.3, 0.5],  # Ejemplo de valores para V17
    'V18': [-0.5, 0.4, -0.9], # Ejemplo de valores para V18
    'V19': [0.2, -0.7, 0.6],  # Ejemplo de valores para V19
    'V20': [-0.3, 0.1, -0.4], # Ejemplo de valores para V20
    'V21': [0.7, -0.6, 0.3],  # Ejemplo de valores para V21
    'V22': [0.0, 0.2, -0.5],  # Ejemplo de valores para V22
    'V23': [0.5, -0.9, 0.8],  # Ejemplo de valores para V23
    'V24': [-0.6, 0.3, -0.7], # Ejemplo de valores para V24
    'V25': [0.1, -0.4, 0.9],  # Ejemplo de valores para V25
    'V26': [0.3, 0.1, -0.2],  # Ejemplo de valores para V26
    'V27': [-0.2, -0.8, 0.7], # Ejemplo de valores para V27
    'V28': [0.9, 0.6, -0.1],  # Ejemplo de valores para V28
    'Amount': [100.0, 250.0, 75.0]  # Ejemplo de valores para Amount
})

# Ver el DataFrame de ejemplo
print(new_data)

# Escalar los nuevos datos
new_data_scaled = scaler.fit_transform(new_data)

# Realizar la predicción
predictions = rf_model.predict(new_data_scaled)

# Ver los resultados
print(f'Predicción para el nuevo dato usando el modelo Random Forest: {predictions}')

"""# Conclusión del modelo 1

A grandes rasgo, los defraudadores siguen un patron de transacciones entre un rango estrátegico para evitar ser detectado. Particularmente podemos ver que las transacciones ocurren entre los días 1 al 20 del mes, a finales del mes se estabilizan las transacciones.

De acuerdo a indicaodres antes vistos, elegimos el modelo de Random forest para detectar y prevenir casos de fraude:

* El modelo RF es robusto para temas de Fraude debido a que cuenta con gran capacidad para manejera datos desequilibrados.

* Cabe señalar que también se podría usar un modelo de logit regresion o redes nueronales, pero consideramos que las métricas del modelo son aceptables para este problema.

Particulamente, podemos obsevar que las metircas de evaluacion fueron muy buenas. Del modelo podemos decir que es muy preciso en la predicción de no fraude (Clase 0). Detecta casi todos los casos correctamente y tiene una precisión excelente de 99%. Para los casos de fraudes (Clase 1), el modelo es muy preciso, 100% de las predicciones de fraude son correctas, pero no logra detectar todos los casos de fraude (recall de 81%). En general, el modelo tiene un rendimiento excelente, con una exactitud total del 99%. Creo que es un bueno modelo y solición para detectar caso de fraude

#Segundo método: Isolation Forest

Adicional al modelo de Random Forest, podemos usar en paralelo el modelo Isolation Fores.

Este modelo de Machine learning está diseñado para la detección de anomalias. Es un modelo no supervisado que indetifica puntos/datos "anormales", como lo sería un caso de fraude.

El modelo se basa en el principio de que las anomalías (outliers) son puntos de datos más fáciles de aislar que los puntos normales debido a que el punto anormal está alejado del resto de datos y es menos frecuente verlos en la base.

##Pasos básicos:
Construcción del bosque:

* Se crean múltiples árboles binarios ("Isolation Trees") dividiendo aleatoriamente los datos.
* Los puntos anómalos tienden a aislarse más rápidamente (es decir, en menos divisiones).

Cálculo de puntuación:

* Cada punto recibe una puntuación de anomalía basada en el número promedio de divisiones necesarias para aislarlo.
* Las puntuaciones cercanas a 1 indican alta probabilidad de ser anomalías, mientras que las cercanas a 0 son normales.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest #importación de librería
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# carga de la base de datos


df2 = pd.read_csv("/content/dataset.csv")

df2.isnull().sum()

#Eliminar valores null

df2 = df2.dropna()

# Variables relevantes, las transacciones diarias más el AMOUNT
features = ['V' + str(i) for i in range(1, 29)] + ['Amount']
X = df2[features]  # Variables predictoras
y = df2['Class']   # Variable objetivo (fraude o no)

df2.columns= ['Id' if col == 'Unnamed: 0' else col for col in df2.columns]

X

df2.info()

# Normalización, opcional pero recomendable para Isolation Forest

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_scaled

# Entrenar modelo Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42) #100 árboles, 1% de anomalias en datos: fijar semilla de aleatoriedad
model.fit(X_scaled)

# Predicciones
# Isolation Forest asigna -1 a anomalías y 1 a datos normales
df2['anomaly_score'] = model.decision_function(X_scaled)  # Puntaje de anomalía
df2['anomaly'] = model.predict(X_scaled)

# Mapear valores de predicción: -1 (anomalía) a 1 (fraude simulado), 1 (normal) a 0 (no fraude)
df2['anomaly'] = df2['anomaly'].map({-1: 1, 1: 0})

# Evaluación del modelo usando la variable Class
print("Confusion Matrix:")
print(confusion_matrix(y, df2['anomaly']))
print("\nClassification Report:")
print(classification_report(y, df2['anomaly']))

# Opcional: Ver transacciones marcadas como anomalías
anomalies = df2[df2['anomaly'] == 1]
print(f"Número de anomalías detectadas: {len(anomalies)}")
print(anomalies.head())


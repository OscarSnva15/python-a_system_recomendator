#0. cargamos librerias necesarias para la implementacion del modelo.
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# 1. Cargar los datos, dataFrame llamado  data con una columna fraude que indica si es fraude (1) o no (0).
data = pd.DataFrame({
    'monto': [100, 200, 150, 300, 50, 500],
    'hora': [10, 14, 3, 22, 1, 18],
    'fraude': [0, 0, 1, 0, 1, 0]
})

#2.  Preparar los datos
X = data.drop('fraude', axis=1) # Caracteristicas X (input)
y = data['fraude']  # Etiquetas Y(output)

# Escalar las características (importante para la regresión logística)
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 3. Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Entrenar el modelo de Regresión Logística
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. Realizar predicciones
y_pred = model.predict(X_test)

# 6. Evaluar el modelo
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))
print("\nPrecisión del modelo:", accuracy_score(y_test, y_pred))
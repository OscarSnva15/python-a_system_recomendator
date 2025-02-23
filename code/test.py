#librerias del metodo de machine learning, regresion logistica(fraude)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
#librerias del metodo de explicabilidad
import lime
import lime.lime_tabular
import numpy as np
#librerias del análisis de importancia global de las características 




def modelo_fraude():
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

    return data, X_train, model, X_test, y_test

def metodo_explicabilidad(data, X_train, model, X_test):
    
    # 1 Crear un explicador LIME
    explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data = X_train,  # Datos de entrenamiento
    feature_names= data.drop('fraude', axis=1).columns.tolist(), # Nombrs de las caracterís.
    class_names=['No Fraude', 'Fraude'],  # Nombres de las clases
        mode='classification'  # Modo de clasificación
    )
    # 2 Seleccionar una instancia para explicar (por ejemplo, la primera instancia del conjunto de prueba)
    instance_index = 0
    instance = X_test[instance_index]
    #3 Explicar la predicción para esta instancia, haciendo función del modelo predictivo
    exp = explainer.explain_instance(
        data_row=instance, predict_fn=model.predict_proba 
    )

    # 4 Mostrar la explicación
    exp.show_in_notebook()  # Si estás en un entorno de notebook 
    exp.as_pyplot_figure()  # Para mostrar la explicación en un gráfico.
    return

def main():
    #modelo_ml
    data, X_train, model, X_test, y_test = modelo_fraude()
    #metodo de explicabilidad
    metodo_explicabilidad(data, X_train, model, X_test)
    # 1 Crear un explicador SHAP
    explainer = shap.LinearExplainer(model, X_train, feature_perturbation="interventional")
    # 2 Calcular los valores SHAP para el conjunto de prueba
    shap_values = explainer.shap_values(X_test)
    # Crear un Decision Plot para varias instancias
    shap.decision_plot(
    explainer.expected_value,  # Valor esperado del modelo
    shap_values[:10, :],  # Valores SHAP para las primeras 10 instancias
    feature_names=data.drop('fraude', axis=1).columns.tolist()  # Nombres de las características)

    return

if __name__ == "__main__":
    main()
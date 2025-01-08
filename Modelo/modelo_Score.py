import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score


class ModelosScore:
    def __init__(self, ruta_csv):
        self.ruta_csv = ruta_csv
        self.data = pd.read_csv(self.ruta_csv)
        self.columnas = ['Calorias', 'Grasas', 'Carbohidratos', 'Proteínas']
        self.X = self.data[self.columnas].values
        self.y = self.data['Grade'].values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                random_state=42)

        # Normalización
        self.scaler = StandardScaler()
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

    def entrenar(self, nombre_modelo):
        """Entrena y guarda el modelo especificado."""
        if nombre_modelo == 'Random Forest':
            modelo = RandomForestClassifier(random_state=42)
        elif nombre_modelo == 'Gradient Boosted Trees':
            modelo = GradientBoostingClassifier(random_state=42)
        elif nombre_modelo == 'XGBoost':
            modelo = XGBClassifier(eval_metric='mlogloss', random_state=42)
        else:
            raise ValueError("Modelo no válido.")

        modelo.fit(self.X_train, self.y_train)

        # Evaluar el modelo
        y_pred = modelo.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Accuracy del modelo {nombre_modelo}: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(self.y_test, y_pred))

        modelo.columnas_entrenamiento = self.columnas

        guardar = input(f"¿Deseas guardar el modelo {nombre_modelo}? (s/n): ").strip().lower()
        if guardar == 's':
            modelo_path = f"{nombre_modelo.replace(' ', '_')}.pkl"
            joblib.dump(modelo, modelo_path)
            print(f"Modelo guardado en: {modelo_path}")
        else:
            print(f"Modelo {nombre_modelo} no se ha guardado.")

    def predecir(self, ruta_modelo):
        """Realiza predicciones usando el modelo cargado."""
        try:
            modelo = joblib.load(ruta_modelo)
            print(f"Modelo {ruta_modelo} cargado correctamente.")

            # Verificar las columnas necesarias en el modelo
            if not hasattr(modelo, 'columnas_entrenamiento'):
                raise AttributeError("El modelo no contiene información sobre las columnas requeridas.")

            columnas_modelo = modelo.columnas_entrenamiento

            # Verificar que las columnas estén presentes en los datos
            if not all(col in self.data.columns for col in columnas_modelo):
                raise KeyError("Las columnas requeridas no están presentes en el archivo CSV.")

            # Filtrar las columnas necesarias
            data_filtrada = self.data[columnas_modelo].dropna()

            # Normalizar las características
            data_normalizada = self.scaler.transform(data_filtrada)

            # Realizar predicciones
            predicciones = modelo.predict(data_normalizada)

            # Si el modelo es XGBoost, convertir las predicciones numéricas a las etiquetas de NutriScore
            if isinstance(modelo, XGBClassifier):
                clases_originales = ['A', 'B', 'C', 'D', 'E']  # 0 --> A, 1 --> B...
                predicciones = [clases_originales[int(pred)] for pred in predicciones]

            # Mostrar resultados
            self.data['Predicción'] = predicciones
            columnas_resultado = ['Calorias', 'Grasas', 'Carbohidratos', 'Proteínas', 'Predicción']
            if 'Nombre' in self.data.columns:
                columnas_resultado.insert(0, 'Nombre')

            return self.data[columnas_resultado]

        except Exception as e:
            print(f"Error al predecir: {e}")
            return None

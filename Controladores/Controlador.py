from Modelo.Modelos import Modelos
from Modelo.modelo_Score import ModelosScore
import pandas as pd


class Controlador:
    def __init__(self):
        self.modelo = Modelos()
        self.modelo_score = None

    def entrenar_modelo_catergorias(self, ruta_csv, nombre_modelo, algoritmo=None):
        """Método para entrenar un modelo clásico o un modelo de NutriScore."""
        if algoritmo:  # Si se pasa un algoritmo clásico
            df = pd.read_csv(ruta_csv)
            if algoritmo == "Gradient Boosted Trees":
                precision = self.modelo.entrenar_gradient_boosted(df, nombre_modelo)
            elif algoritmo == "K-NN":
                precision = self.modelo.entrenar_k_nn(df, nombre_modelo)
            elif algoritmo == "Naive Bayes":
                precision = self.modelo.entrenar_naive_bayes(df, nombre_modelo)
            else:
                raise ValueError("Algoritmo no soportado")
            return f"Entrenamiento completado con precisión: {precision:.2f}"

        # Si no se pasa un algoritmo, entrenamos un modelo de NutriScore
        self.modelo_score = ModelosScore(ruta_csv)
        self.modelo_score.entrenar(nombre_modelo)
        return f"Entrenamiento del modelo {nombre_modelo} completado."

    def predecir_score(self, ruta_modelo, ruta_csv):
        """Método para realizar predicciones con el modelo guardado."""
        if self.modelo_score:
            return self.modelo_score.predecir(ruta_modelo)
        else:
            raise ValueError("No se ha entrenado un modelo de NutriScore.")

    def predecir_modelo_clasico(self, ruta_modelo, ruta_csv):
        """Método para predecir con un modelo clásico (ej. Random Forest, XGBoost)."""
        resultados = self.modelo.predecir(ruta_modelo, ruta_csv)
        return resultados
    def entrenar_modelo_score(self, ruta_csv,nombre_modelo):
        if nombre_modelo:  # Si se pasa un algoritmo clásico
            df = pd.read_csv(ruta_csv)
            if nombre_modelo == "Random Forest":
                precision = self.modelo_score.entrenar("Random Forest")
            elif nombre_modelo == "Gradient Boosted Trees":
                precision = self.modelo_score.entrenar("Gradient Boosted Trees")
            elif nombre_modelo == "XGBoost":
                precision = self.modelo_score.entrenar("XGBoost")
            else:
                raise ValueError("Algoritmo no soportado")
            return f"Entrenamiento completado con precisión: {precision:.2f}"

            # Si no se pasa un algoritmo, entrenamos un modelo de NutriScore
        self.modelo_score = ModelosScore(ruta_csv)
        self.modelo_score.entrenar(nombre_modelo)
        return f"Entrenamiento del modelo {nombre_modelo} completado."
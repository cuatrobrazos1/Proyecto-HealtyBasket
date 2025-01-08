from Modelo.Modelos import Modelos
import pandas as pd

class Controlador:
    def __init__(self):
        self.modelo = Modelos()

    def entrenar_modelo(self, ruta_csv, nombre_modelo, algoritmo):
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

    def predecir(self, ruta_modelo, ruta_csv):
        resultados = self.modelo.predecir(ruta_modelo, ruta_csv)
        return resultados

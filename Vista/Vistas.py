import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from Controlador import Controlador

# Crear instancia del controlador
controlador = Controlador()

def cargar_archivo():
    ruta = filedialog.askopenfilename(title="Seleccionar archivo")
    return ruta

# Crear ventana principal
root = tk.Tk()
root.title("HealthyBasket")
root.geometry("600x400")

# Cargar y mostrar el logo
logo_path = "logo_path.jpeg"
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((150, 150), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.pack(pady=10)
except FileNotFoundError:
    tk.Label(root, text="No se encontró el archivo del logo").pack(pady=10)

# Crear las pestañas
notebook = ttk.Notebook(root)

# Pestaña de Entrenamiento
frame_entrenamiento = ttk.Frame(notebook)
notebook.add(frame_entrenamiento, text="Entrenamiento")

# Pestaña de Predicción
frame_prediccion = ttk.Frame(notebook)
notebook.add(frame_prediccion, text="Predicción")

notebook.pack(expand=True, fill="both")

# --------------------
# Contenido: Entrenamiento
# --------------------

def ejecutar_entrenamiento():
    ruta_csv = entry_dataset_a.get()
    nombre_modelo = entry_resultado.get()
    algoritmo = combo_algoritmo.get()
    try:
        resultado = controlador.entrenar_modelo(ruta_csv, nombre_modelo, algoritmo)
        label_estado_entrenamiento.config(text=resultado)
    except Exception as e:
        label_estado_entrenamiento.config(text=f"Error: {str(e)}")

# Etiqueta y botón para cargar datasets
label_dataset_a = ttk.Label(frame_entrenamiento, text="Archivo de datos:")
label_dataset_a.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_dataset_a = ttk.Entry(frame_entrenamiento, width=40)
entry_dataset_a.grid(row=0, column=1, padx=10, pady=5)
button_cargar_a = ttk.Button(frame_entrenamiento, text="Abrir", command=lambda: entry_dataset_a.insert(0, cargar_archivo()))
button_cargar_a.grid(row=0, column=2, padx=10, pady=5)

# Selección del algoritmo
label_algoritmo = ttk.Label(frame_entrenamiento, text="Seleccionar Algoritmo:")
label_algoritmo.grid(row=1, column=0, padx=10, pady=5, sticky="w")
combo_algoritmo = ttk.Combobox(frame_entrenamiento, values=["Gradient Boosted Trees", "K-NN", "Naive Bayes"])
combo_algoritmo.grid(row=1, column=1, padx=10, pady=5)
combo_algoritmo.set("Gradient Boosted Trees")

# Nombre del modelo
label_resultado = ttk.Label(frame_entrenamiento, text="Nombre del modelo:")
label_resultado.grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_resultado = ttk.Entry(frame_entrenamiento, width=40)
entry_resultado.grid(row=2, column=1, padx=10, pady=5)

# Botón para ejecutar entrenamiento
button_ejecutar = ttk.Button(frame_entrenamiento, text="Entrenar", command=ejecutar_entrenamiento)
button_ejecutar.grid(row=3, column=1, pady=20)

# Estado del entrenamiento
label_estado_entrenamiento = ttk.Label(frame_entrenamiento, text="")
label_estado_entrenamiento.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

# --------------------
# Contenido: Predicción
# --------------------

def ejecutar_prediccion():
    ruta_modelo = entry_ruta_modelo.get()
    ruta_csv = entry_csv_prediccion.get()
    try:
        resultados = controlador.predecir(ruta_modelo, ruta_csv)
        resultado_texto = "\n".join(f"{row['Nombre']}: {row['Categoria_Predicha']}" for _, row in resultados.iterrows())
        label_estado_prediccion.config(text=resultado_texto)
    except Exception as e:
        label_estado_prediccion.config(text=f"Error: {str(e)}")

# Cargar modelo
label_ruta_modelo = ttk.Label(frame_prediccion, text="Ruta del modelo:")
label_ruta_modelo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_ruta_modelo = ttk.Entry(frame_prediccion, width=40)
entry_ruta_modelo.grid(row=0, column=1, padx=10, pady=5)
button_cargar_modelo = ttk.Button(frame_prediccion, text="Abrir", command=lambda: entry_ruta_modelo.insert(0, cargar_archivo()))
button_cargar_modelo.grid(row=0, column=2, padx=10, pady=5)

# Cargar CSV para predicción
label_csv_prediccion = ttk.Label(frame_prediccion, text="Archivo para predecir:")
label_csv_prediccion.grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_csv_prediccion = ttk.Entry(frame_prediccion, width=40)
entry_csv_prediccion.grid(row=1, column=1, padx=10, pady=5)
button_cargar_csv = ttk.Button(frame_prediccion, text="Abrir", command=lambda: entry_csv_prediccion.insert(0, cargar_archivo()))
button_cargar_csv.grid(row=1, column=2, padx=10, pady=5)

# Botón para ejecutar predicción
button_predecir = ttk.Button(frame_prediccion, text="Predecir", command=ejecutar_prediccion)
button_predecir.grid(row=2, column=1, pady=20)

# Estado de la predicción
label_estado_prediccion = ttk.Label(frame_prediccion, text="")
label_estado_prediccion.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# --------------------

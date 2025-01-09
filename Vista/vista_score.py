import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from Controladores.Controlador import Controlador


class vistaUi:
    def __init__(self):
        # Crear instancia de Controlador
        self.controlador = Controlador()  # Instancia el controlador

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("HealthyBasket")
        self.root.geometry("600x400")

        # Cargar y mostrar el logo
        self.logo_path = "Vista/logo_path.jpeg"
        try:
            self.logo_image = Image.open(self.logo_path)
            self.logo_image = self.logo_image.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.logo_label = tk.Label(self.root, image=self.logo_photo)
            self.logo_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(self.root, text="No se encontró el archivo del logo").pack(pady=10)

        # Crear las pestañas
        self.notebook = ttk.Notebook(self.root)

        # Pestaña de Entrenamiento
        self.frame_entrenamiento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_entrenamiento, text="Entrenamiento")

        # Pestaña de Predicción
        self.frame_prediccion = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_prediccion, text="Predicción")

        self.notebook.pack(expand=True, fill="both")

        # Llamar a los métodos para crear las interfaces
        self.crear_interfaz_entrenamiento()
        self.crear_interfaz_prediccion()

        # Botón para volver a vista inicial
        boton_volver = tk.Button(self.root, text="Volver", command=self.volver_a_inicial)
        boton_volver.pack(pady=20)

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo")
        return ruta

    def volver_a_inicial(self):
        """Cerrar la ventana actual y volver a la inicial."""
        from Vista.Vista_inicial import vistaini  # Importación diferida
        self.root.destroy()
        vistaini().get_root().mainloop()

    # -------------------------
    # Contenido: Entrenamiento
    # -------------------------

    def ejecutar_entrenamiento(self):
        ruta_csv = self.entry_dataset_a.get()
        nombre_modelo = self.entry_resultado.get()
        algoritmo = self.combo_algoritmo.get()
        try:
            resultado = self.controlador.entrenar_modelo_score(ruta_csv, nombre_modelo)
            self.label_estado_entrenamiento.config(text=resultado)
        except Exception as e:
            self.label_estado_entrenamiento.config(text=f"Error: {str(e)}")

    def crear_interfaz_entrenamiento(self):
        # Etiqueta y botón para cargar datasets
        self.label_dataset_a = ttk.Label(self.frame_entrenamiento, text="Archivo de datos:")
        self.label_dataset_a.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_dataset_a = ttk.Entry(self.frame_entrenamiento, width=40)
        self.entry_dataset_a.grid(row=0, column=1, padx=10, pady=5)
        button_cargar_a = ttk.Button(self.frame_entrenamiento, text="Abrir",
                                     command=lambda: self.entry_dataset_a.insert(0, self.cargar_archivo()))
        button_cargar_a.grid(row=0, column=2, padx=10, pady=5)

        # Selección del algoritmo
        self.label_algoritmo = ttk.Label(self.frame_entrenamiento, text="Seleccionar Algoritmo:")
        self.label_algoritmo.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.combo_algoritmo = ttk.Combobox(self.frame_entrenamiento,
                                            values=["Random Forest", "Gradient Boosted Trees", "XGBoost"])
        self.combo_algoritmo.grid(row=1, column=1, padx=10, pady=5)
        self.combo_algoritmo.set("Random Forest")

        # Nombre del modelo
        self.label_resultado = ttk.Label(self.frame_entrenamiento, text="Nombre del modelo:")
        self.label_resultado.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_resultado = ttk.Entry(self.frame_entrenamiento, width=40)
        self.entry_resultado.grid(row=2, column=1, padx=10, pady=5)

        # Botón para ejecutar entrenamiento
        button_ejecutar = ttk.Button(self.frame_entrenamiento, text="Entrenar", command=self.ejecutar_entrenamiento)
        button_ejecutar.grid(row=3, column=1, pady=20)

        # Estado del entrenamiento
        self.label_estado_entrenamiento = ttk.Label(self.frame_entrenamiento, text="")
        self.label_estado_entrenamiento.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    # -------------------------
    # Contenido: Predicción
    # -------------------------

    def ejecutar_prediccion(self):
        ruta_modelo = self.entry_ruta_modelo.get()
        ruta_csv = self.entry_csv_prediccion.get()
        try:
            resultados = self.controlador.predecir_score(ruta_modelo, ruta_csv)
            resultado_texto = "\n".join(
                f"{row['Nombre']}: {row['Categoria_Predicha']}" for _, row in resultados.iterrows())
            self.label_estado_prediccion.config(text=resultado_texto)
        except Exception as e:
            self.label_estado_prediccion.config(text=f"Error: {str(e)}")

    def crear_interfaz_prediccion(self):
        # Cargar modelo
        self.label_ruta_modelo = ttk.Label(self.frame_prediccion, text="Ruta del modelo:")
        self.label_ruta_modelo.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_ruta_modelo = ttk.Entry(self.frame_prediccion, width=40)
        self.entry_ruta_modelo.grid(row=0, column=1, padx=10, pady=5)
        button_cargar_modelo = ttk.Button(self.frame_prediccion, text="Abrir",
                                          command=lambda: self.entry_ruta_modelo.insert(0, self.cargar_archivo()))
        button_cargar_modelo.grid(row=0, column=2, padx=10, pady=5)

        # Cargar CSV para predicción
        self.label_csv_prediccion = ttk.Label(self.frame_prediccion, text="Archivo para predecir:")
        self.label_csv_prediccion.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_csv_prediccion = ttk.Entry(self.frame_prediccion, width=40)
        self.entry_csv_prediccion.grid(row=1, column=1, padx=10, pady=5)
        button_cargar_csv = ttk.Button(self.frame_prediccion, text="Abrir",
                                       command=lambda: self.entry_csv_prediccion.insert(0, self.cargar_archivo()))
        button_cargar_csv.grid(row=1, column=2, padx=10, pady=5)

        # Botón para ejecutar predicción
        button_predecir = ttk.Button(self.frame_prediccion, text="Predecir", command=self.ejecutar_prediccion)
        button_predecir.grid(row=2, column=1, pady=20)

        # Estado de la predicción
        self.label_estado_prediccion = ttk.Label(self.frame_prediccion, text="")
        self.label_estado_prediccion.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def get_root(self):
        return self.root  # Devuelve la instancia de la ventana principal

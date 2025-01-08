import tkinter as tk
from Controladores.Controlador import Controlador


class vistaini:
    def __init__(self):  # Constructor corregido
        # Crear instancia de Controlador
        self.controlador = Controlador()  # Instancia el controlador

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("HealthyBasket")
        self.root.geometry("600x400")

        # Crear el menú inicial
        self.mostrar_menu_principal()

    def mostrar_menu_principal(self):
        """Crear el menú inicial con opciones de Categoría y Score."""
        # Limpiar la ventana principal
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título del menú
        label_titulo = tk.Label(self.root, text="Menú Principal", font=("Arial", 16))
        label_titulo.pack(pady=20)

        # Botón para ir a la vista de Categorías
        boton_categoria = tk.Button(self.root, text="Categoría", font=("Arial", 14),
                                    command=self.mostrar_vista_categorias)
        boton_categoria.pack(pady=10)

        # Botón para ir a la vista de Score
        boton_score = tk.Button(self.root, text="Score", font=("Arial", 14),
                                command=self.mostrar_vista_score)
        boton_score.pack(pady=10)

    def mostrar_vista_categorias(self):
        """Abrir la ventana de Categorías."""
        from Vista.vista_categorias import vistaUi  # Importación diferida
        self.root.destroy()  # Cierra la ventana actual
        vistaUi().get_root().mainloop()  # Cargar la interfaz de vistaUi

    def mostrar_vista_score(self):
        """Abrir la ventana de Categorías."""
        from Vista.vista_score import vistaUi  # Importación diferida
        self.root.destroy()  # Cierra la ventana actual
        vistaUi().get_root().mainloop()  # Cargar la interfaz de vistaUi

    def get_root(self):
        return self.root

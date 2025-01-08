# main.py

# Importamos la clase vistaUi desde el módulo Vista
from Vista.Vista_inicial import vistaini


def main():
    # Crear una instancia de la clase vistaUi
    app = vistaini()

    # Ejecutar el ciclo principal de la interfaz gráfica
    app.get_root().mainloop()


if __name__ == "__main__":
    main()

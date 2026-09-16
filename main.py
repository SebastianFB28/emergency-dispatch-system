import tkinter as tk
from app.ui.main_window import MainWindow


def main():
    # Inicializamos la ventana principal de Tkinter
    root = tk.Tk()

    # Instanciamos nuestra vista principal pasándole la ventana raíz
    app = MainWindow(root)

    # Iniciamos el bucle principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
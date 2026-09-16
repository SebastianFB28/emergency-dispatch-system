import tkinter as tk
from app.ui.main_window import MainWindow
from app.services.emergency_service import EmergencyService


def main():
    # 1. Instanciamos el servicio (contiene nuestras 3 listas)
    emergency_service = EmergencyService()

    # Inicializamos la ventana principal de Tkinter
    root = tk.Tk()

    # Instanciamos nuestra vista principal pasándole la ventana raíz
    app = MainWindow(root, emergency_service)

    # Iniciamos el bucle principal de la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
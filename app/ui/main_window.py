import tkinter as tk
from tkinter import messagebox
from app.ui.registration_window import RegistrationWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Emergencia")
        self.root.geometry("400x350")
        self.root.config(bg="#f0f0f0") # Color de fondo

        self._build_ui()

    def _build_ui(self):
        # 1. Título
        title_label = tk.Label(
            self.root,
            text="SISTEMA DE EMERGENCIA",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(30, 10))

        # 2. Icono de Emergencia (Usamos un emoji grande como placeholder)
        icon_label = tk.Label(
            self.root,
            text="🚑",
            font=("Arial", 50),
            bg="#f0f0f0"
        )
        icon_label.pack(pady=(0, 20))

        # 3. Botón: Registrar su emergencia
        btn_register = tk.Button(
            self.root,
            text="Registrar su emergencia",
            font=("Arial", 12, "bold"),
            bg="#d9534f", # Color rojo tipo alerta
            fg="white",
            width=20,
            command=self.abrir_registro
        )
        btn_register.pack(pady=10)

        # 4. Botón: Salir
        btn_exit = tk.Button(
            self.root,
            text="Salir",
            font=("Arial", 12),
            bg="#5bc0de",
            fg="white",
            width=20,
            command=self.salir
        )
        btn_exit.pack(pady=10)

    def abrir_registro(self):
        # Este método se conectará luego con otra vista o servicio
        RegistrationWindow(self.root)

    def salir(self):
        # Cierra la aplicación de manera segura
        self.root.destroy()
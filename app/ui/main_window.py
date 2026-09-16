import tkinter as tk
from tkinter import messagebox
from app.ui.registration_window import RegistrationWindow
from app.ui.list_window import EmergencyListWindow


class MainWindow:
    def __init__(self, root, emergency_service):
        self.root = root
        self.root.title("Sistema de Emergencia")
        self.root.geometry("400x350")
        self.root.config(bg="#f0f0f0")
        self.emergency_service = emergency_service

        self._build_ui()

    def _build_ui(self):
        title_label = tk.Label(
            self.root,
            text="SISTEMA DE EMERGENCIA",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(30, 10))

        icon_label = tk.Label(
            self.root,
            text="🚑",
            font=("Arial", 50),
            bg="#f0f0f0"
        )
        icon_label.pack(pady=(0, 20))

        btn_register = tk.Button(
            self.root,
            text="Registrar su emergencia",
            font=("Arial", 12, "bold"),
            bg="#d9534f",
            fg="white",
            width=20,
            command=self.abrir_registro
        )
        btn_register.pack(pady=10)

        btn_list = tk.Button(
            self.root,
            text="Ver emergencias",
            font=("Arial", 12, "bold"),
            bg="#f0ad4e",
            fg="white",
            width=20,
            command=self.abrir_listado
        )
        btn_list.pack(pady=10)

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
        RegistrationWindow(self.root, self.emergency_service)

    def abrir_listado(self):
        EmergencyListWindow(self.root, self.emergency_service)

    def salir(self):
        self.root.destroy()
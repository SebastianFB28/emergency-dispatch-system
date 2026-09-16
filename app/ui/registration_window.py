import tkinter as tk
from tkinter import ttk, messagebox


class RegistrationWindow:
    def __init__(self, parent):
        # Toplevel crea una nueva ventana que "flota" sobre la ventana padre (parent)
        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Emergencia")
        self.window.geometry("450x450")
        self.window.config(bg="#f9f9f9")

        # Esto hace que el usuario no pueda interactuar con la ventana principal hasta cerrar esta
        self.window.grab_set()

        self._build_ui()

    def _build_ui(self):
        # Título
        lbl_title = tk.Label(
            self.window,
            text="Formulario de Registro",
            font=("Arial", 14, "bold"),
            bg="#f9f9f9"
        )
        lbl_title.pack(pady=(15, 10))

        # Contenedor para alinear los campos
        frame = tk.Frame(self.window, bg="#f9f9f9")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # 1. Nombre del reportante
        tk.Label(frame, text="Nombre del reportante:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = tk.Entry(frame, width=30)
        self.entry_name.grid(row=0, column=1, pady=5, padx=10)

        # 2. Dirección
        tk.Label(frame, text="Dirección del incidente:", bg="#f9f9f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_address = tk.Entry(frame, width=30)
        self.entry_address.grid(row=1, column=1, pady=5, padx=10)

        # 3. Descripción
        tk.Label(frame, text="Descripción:", bg="#f9f9f9").grid(row=2, column=0, sticky="nw", pady=5)
        self.text_desc = tk.Text(frame, width=22, height=4)
        self.text_desc.grid(row=2, column=1, pady=5, padx=10)

        # 4. Número de heridos (Usamos Spinbox para números)
        tk.Label(frame, text="Número de heridos:", bg="#f9f9f9").grid(row=3, column=0, sticky="w", pady=5)
        self.spin_heridos = tk.Spinbox(frame, from_=0, to=1000, width=10)
        self.spin_heridos.grid(row=3, column=1, sticky="w", pady=5, padx=10)

        # 5. Número de muertos
        tk.Label(frame, text="Número de muertos:", bg="#f9f9f9").grid(row=4, column=0, sticky="w", pady=5)
        self.spin_muertos = tk.Spinbox(frame, from_=0, to=1000, width=10)
        self.spin_muertos.grid(row=4, column=1, sticky="w", pady=5, padx=10)

        # 6. Tipo de emergencia (Combobox)
        tk.Label(frame, text="Tipo de emergencia:", bg="#f9f9f9").grid(row=5, column=0, sticky="w", pady=5)
        opciones_tipo = ["Robo", "Accidente de tráfico", "Terremoto", "Incendio", "Urgencia Médica", "Otro"]
        self.combo_tipo = ttk.Combobox(frame, values=opciones_tipo, state="readonly", width=27)
        self.combo_tipo.grid(row=5, column=1, pady=5, padx=10)
        self.combo_tipo.current(1)  # Deja "Accidente de tráfico" por defecto

        # Contenedor para botones
        btn_frame = tk.Frame(self.window, bg="#f9f9f9")
        btn_frame.pack(pady=15)

        # Botón Guardar
        btn_save = tk.Button(
            btn_frame, text="Guardar Emergencia", bg="#5cb85c", fg="white",
            font=("Arial", 10, "bold"), command=self.guardar_emergencia
        )
        btn_save.pack(side="left", padx=10)

        # Botón Cancelar
        btn_cancel = tk.Button(
            btn_frame, text="Cancelar", bg="#d9534f", fg="white",
            font=("Arial", 10, "bold"), command=self.window.destroy
        )
        btn_cancel.pack(side="right", padx=10)

    def guardar_emergencia(self):
        # 1. Extraer los datos de la vista
        nombre = self.entry_name.get().strip()
        direccion = self.entry_address.get().strip()
        descripcion = self.text_desc.get("1.0", tk.END).strip()
        heridos = self.spin_heridos.get()
        muertos = self.spin_muertos.get()
        tipo = self.combo_tipo.get()

        # 2. Validación básica
        if not nombre or not direccion or not descripcion:
            messagebox.showwarning("Campos incompletos", "Por favor, complete nombre, dirección y descripción.",
                                   parent=self.window)
            return

        # (Próximamente): Aquí llamaremos a nuestro archivo "emergency_service.py"
        # para guardar los datos en nuestra lista doblemente enlazada.

        # Por ahora solo imprimimos en consola y cerramos
        print(f"--- NUEVA EMERGENCIA ---")
        print(f"Reporta: {nombre} | Dir: {direccion}")
        print(f"Tipo: {tipo} | Heridos: {heridos} | Muertos: {muertos}")
        print(f"Desc: {descripcion}")

        messagebox.showinfo("Éxito", "La emergencia ha sido registrada correctamente.", parent=self.window)
        self.window.destroy()
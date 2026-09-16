import tkinter as tk
from tkinter import ttk, messagebox


class RegistrationWindow:
    # AÑADIMOS emergency_service COMO PARÁMETRO
    def __init__(self, parent, emergency_service):
        self.emergency_service = emergency_service

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Emergencia")
        self.window.geometry("450x450")
        self.window.config(bg="#f9f9f9")
        self.window.grab_set()

        self._build_ui()

    def _build_ui(self):
        # (Mantén todo el código de _build_ui exactamente igual que antes)
        # Título
        lbl_title = tk.Label(self.window, text="Formulario de Registro", font=("Arial", 14, "bold"), bg="#f9f9f9")
        lbl_title.pack(pady=(15, 10))

        frame = tk.Frame(self.window, bg="#f9f9f9")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(frame, text="Nombre del reportante:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_name = tk.Entry(frame, width=30)
        self.entry_name.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(frame, text="Dirección del incidente:", bg="#f9f9f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_address = tk.Entry(frame, width=30)
        self.entry_address.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(frame, text="Descripción:", bg="#f9f9f9").grid(row=2, column=0, sticky="nw", pady=5)
        self.text_desc = tk.Text(frame, width=22, height=4)
        self.text_desc.grid(row=2, column=1, pady=5, padx=10)

        tk.Label(frame, text="Número de heridos:", bg="#f9f9f9").grid(row=3, column=0, sticky="w", pady=5)
        self.spin_heridos = tk.Spinbox(frame, from_=0, to=1000, width=10)
        self.spin_heridos.grid(row=3, column=1, sticky="w", pady=5, padx=10)

        tk.Label(frame, text="Número de muertos:", bg="#f9f9f9").grid(row=4, column=0, sticky="w", pady=5)
        self.spin_muertos = tk.Spinbox(frame, from_=0, to=1000, width=10)
        self.spin_muertos.grid(row=4, column=1, sticky="w", pady=5, padx=10)

        tk.Label(frame, text="Tipo de emergencia:", bg="#f9f9f9").grid(row=5, column=0, sticky="w", pady=5)
        opciones_tipo = ["Robo", "Accidente de tráfico", "Terremoto", "Incendio", "Urgencia Médica", "Otro"]
        self.combo_tipo = ttk.Combobox(frame, values=opciones_tipo, state="readonly", width=27)
        self.combo_tipo.grid(row=5, column=1, pady=5, padx=10)
        self.combo_tipo.current(1)

        btn_frame = tk.Frame(self.window, bg="#f9f9f9")
        btn_frame.pack(pady=15)

        btn_save = tk.Button(btn_frame, text="Guardar Emergencia", bg="#5cb85c", fg="white", font=("Arial", 10, "bold"),
                             command=self.guardar_emergencia)
        btn_save.pack(side="left", padx=10)

        btn_cancel = tk.Button(btn_frame, text="Cancelar", bg="#d9534f", fg="white", font=("Arial", 10, "bold"),
                               command=self.window.destroy)
        btn_cancel.pack(side="right", padx=10)

    def guardar_emergencia(self):
        nombre = self.entry_name.get().strip()
        direccion = self.entry_address.get().strip()
        descripcion = self.text_desc.get("1.0", tk.END).strip()
        heridos = self.spin_heridos.get()
        muertos = self.spin_muertos.get()
        tipo = self.combo_tipo.get()

        if not nombre or not direccion or not descripcion:
            messagebox.showwarning("Campos incompletos", "Por favor, complete nombre, dirección y descripción.",
                                   parent=self.window)
            return

        # AQUÍ LLAMAMOS AL SERVICIO
        nodo, lista_destino = self.emergency_service.register_emergency(
            nombre, direccion, descripcion, heridos, muertos, tipo
        )

        # Mostramos los resultados reales
        mensaje_exito = f"Emergencia registrada con éxito.\n\n"
        mensaje_exito += f"Asignada a: {lista_destino}\n"
        mensaje_exito += f"Ticket asignado: #{nodo.ticket}\n"
        mensaje_exito += f"Prioridad calculada: {nodo.data.prioridad}/10"

        print(f"--- NUEVA EMERGENCIA ---")
        print(f"Lista: {lista_destino} | Ticket: {nodo.ticket} | Prioridad: {nodo.data.prioridad}")

        messagebox.showinfo("Éxito", mensaje_exito, parent=self.window)

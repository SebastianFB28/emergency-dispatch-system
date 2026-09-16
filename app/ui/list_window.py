import tkinter as tk
from tkinter import ttk, messagebox


class EmergencyListWindow:
    def __init__(self, parent, emergency_service):
        self.emergency_service = emergency_service
        self.selected_ticket = None
        self.selected_lista_nombre = None

        self.window = tk.Toplevel(parent)
        self.window.title("Listado de Emergencias")
        self.window.geometry("900x550")
        self.window.config(bg="#f9f9f9")
        self.window.grab_set()

        self._build_ui()
        self._cargar_datos()

    def _build_ui(self):
        lbl_title = tk.Label(
            self.window, text="Emergencias Registradas",
            font=("Arial", 14, "bold"), bg="#f9f9f9"
        )
        lbl_title.pack(pady=(15, 10))

        main_frame = tk.Frame(self.window, bg="#f9f9f9")
        main_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # ---------------- IZQUIERDA: formulario + botones ----------------
        left_frame = tk.Frame(main_frame, bg="#f9f9f9", width=260)
        left_frame.pack(side="left", fill="y", padx=(0, 15))
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="Detalle / Edición", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=(0, 10))

        form = tk.Frame(left_frame, bg="#f9f9f9")
        form.pack(fill="x")

        tk.Label(form, text="Ticket:", bg="#f9f9f9").grid(row=0, column=0, sticky="w", pady=4)
        self.lbl_ticket = tk.Label(form, text="-", bg="#f9f9f9", font=("Arial", 10, "bold"))
        self.lbl_ticket.grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(form, text="Nombre:", bg="#f9f9f9").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_nombre = tk.Entry(form, width=20)
        self.entry_nombre.grid(row=1, column=1, pady=4)

        tk.Label(form, text="Dirección:", bg="#f9f9f9").grid(row=2, column=0, sticky="w", pady=4)
        self.entry_direccion = tk.Entry(form, width=20)
        self.entry_direccion.grid(row=2, column=1, pady=4)

        tk.Label(form, text="Descripción:", bg="#f9f9f9").grid(row=3, column=0, sticky="nw", pady=4)
        self.text_descripcion = tk.Text(form, width=16, height=3)
        self.text_descripcion.grid(row=3, column=1, pady=4)

        tk.Label(form, text="Heridos:", bg="#f9f9f9").grid(row=4, column=0, sticky="w", pady=4)
        self.spin_heridos = tk.Spinbox(form, from_=0, to=1000, width=7)
        self.spin_heridos.grid(row=4, column=1, sticky="w", pady=4)

        tk.Label(form, text="Muertos:", bg="#f9f9f9").grid(row=5, column=0, sticky="w", pady=4)
        self.spin_muertos = tk.Spinbox(form, from_=0, to=1000, width=7)
        self.spin_muertos.grid(row=5, column=1, sticky="w", pady=4)

        tk.Label(form, text="Tipo:", bg="#f9f9f9").grid(row=6, column=0, sticky="w", pady=4)
        opciones_tipo = ["Robo", "Accidente de tráfico", "Terremoto", "Incendio", "Urgencia Médica", "Otro"]
        self.combo_tipo = ttk.Combobox(form, values=opciones_tipo, state="readonly", width=17)
        self.combo_tipo.grid(row=6, column=1, pady=4)

        btns_frame = tk.Frame(left_frame, bg="#f9f9f9")
        btns_frame.pack(pady=25, fill="x")

        tk.Button(
            btns_frame, text="Actualizar", bg="#5bc0de", fg="white",
            font=("Arial", 10, "bold"), command=self._actualizar_emergencia
        ).pack(fill="x", pady=5)

        tk.Button(
            btns_frame, text="Atender", bg="#5cb85c", fg="white",
            font=("Arial", 10, "bold")
        ).pack(fill="x", pady=5)

        tk.Button(
            btns_frame, text="Salir", bg="#d9534f", fg="white",
            font=("Arial", 10, "bold"), command=self.window.destroy
        ).pack(fill="x", pady=5)

        # ---------------- DERECHA: las tres listas, apiladas, mismo lado ----------------
        right_frame = tk.Frame(main_frame, bg="#f9f9f9")
        right_frame.pack(side="left", fill="both", expand=True)

        self.trees = {}
        columns = ("ticket", "nombre", "direccion", "tipo", "prioridad", "heridos", "muertos")
        headers = {
            "ticket": "Ticket",
            "nombre": "Reportante",
            "direccion": "Dirección",
            "tipo": "Tipo",
            "prioridad": "Prioridad",
            "heridos": "Heridos",
            "muertos": "Muertos",
        }
        widths = {
            "ticket": 55, "nombre": 100, "direccion": 110,
            "tipo": 100, "prioridad": 60, "heridos": 55, "muertos": 55,
        }

        for nombre_lista in ["Alta Prioridad", "Media Prioridad", "Baja Prioridad"]:
            tk.Label(
                right_frame, text=f"Lista Prioridad {nombre_lista.split()[0]}",
                font=("Arial", 11, "bold"), bg="#f9f9f9"
            ).pack(anchor="w", pady=(5, 2))

            tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=4)
            for col in columns:
                tree.heading(col, text=headers[col])
                tree.column(col, width=widths[col], anchor="center")
            tree.pack(fill="x", pady=(0, 10))

            tree.bind("<<TreeviewSelect>>", self._on_select)
            self.trees[nombre_lista] = tree

    def _cargar_datos(self):
        """Limpia y vuelve a llenar las tres tablas con los datos actuales."""
        datos = self.emergency_service.get_all_emergencies()

        for nombre_lista, tree in self.trees.items():
            # Limpiar filas existentes
            for item in tree.get_children():
                tree.delete(item)

            nodos = datos[nombre_lista]
            if not nodos:
                continue

            for nodo in nodos:
                emergencia = nodo.data
                tree.insert("", "end", values=(
                    nodo.ticket,
                    emergencia.nombre,
                    emergencia.direccion,
                    emergencia.tipo_emergencia,
                    emergencia.prioridad,
                    emergencia.heridos,
                    emergencia.muertos,
                ))

    def _on_select(self, event):
        """Cuando el usuario hace clic en una fila, se llenan los campos del formulario."""
        tree = event.widget
        seleccion = tree.selection()
        if not seleccion:
            return

        # Identificamos de cuál de las tres listas vino el clic
        nombre_lista = None
        for nombre, t in self.trees.items():
            if t is tree:
                nombre_lista = nombre
                break

        valores = tree.item(seleccion[0])["values"]
        ticket = valores[0]

        self.selected_ticket = ticket
        self.selected_lista_nombre = nombre_lista

        # Llenamos el formulario (el ticket NO se puede editar, solo se muestra)
        self.lbl_ticket.config(text=str(ticket))

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])

        self.entry_direccion.delete(0, tk.END)
        self.entry_direccion.insert(0, valores[2])

        self.text_descripcion.delete("1.0", tk.END)

        self.combo_tipo.set(valores[3])

        self.spin_heridos.delete(0, tk.END)
        self.spin_heridos.insert(0, valores[5])

        self.spin_muertos.delete(0, tk.END)
        self.spin_muertos.insert(0, valores[6])

        # La descripción no está en la tabla, así que la buscamos directo en el nodo
        lista_obj = self.emergency_service._obtener_lista_por_nombre(nombre_lista)
        nodo = lista_obj.search(ticket)
        if nodo:
            self.text_descripcion.insert("1.0", nodo.data.descripcion)

    def _actualizar_emergencia(self):
        """Toma los datos del formulario y actualiza la emergencia seleccionada."""
        if self.selected_ticket is None:
            messagebox.showwarning(
                "Sin selección",
                "Selecciona una emergencia de alguna lista primero.",
                parent=self.window
            )
            return

        nombre = self.entry_nombre.get().strip()
        direccion = self.entry_direccion.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()
        heridos = self.spin_heridos.get()
        muertos = self.spin_muertos.get()
        tipo = self.combo_tipo.get()

        if not nombre or not direccion or not descripcion:
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor, complete nombre, dirección y descripción.",
                parent=self.window
            )
            return

        nodo, nueva_lista = self.emergency_service.update_emergency(
            self.selected_lista_nombre, self.selected_ticket,
            nombre, direccion, descripcion, heridos, muertos, tipo
        )

        if nodo is None:
            messagebox.showerror("Error", "No se encontró la emergencia.", parent=self.window)
            return

        self._cargar_datos()

        messagebox.showinfo(
            "Actualizado",
            f"Emergencia #{nodo.ticket} actualizada.\n"
            f"Nueva prioridad: {nodo.data.prioridad}/10\n"
            f"Lista: {nueva_lista}",
            parent=self.window
        )
class Emergency:
    def __init__(self, nombre, direccion, descripcion, heridos, muertos, tipo_emergencia):
        self.nombre = nombre
        self.direccion = direccion
        self.descripcion = descripcion
        self.heridos = int(heridos)
        self.muertos = int(muertos)
        self.tipo_emergencia = tipo_emergencia

        # Inicializamos la prioridad en 0.
        # Más adelante haremos un método que la calcule basado en heridos/tipo.
        self.prioridad = 0

    def __str__(self):
        return f"[{self.tipo_emergencia}] Reporta: {self.nombre} | Prioridad: {self.prioridad}"
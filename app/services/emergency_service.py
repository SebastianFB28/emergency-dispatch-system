from app.models.emergency import Emergency
from app.data.doubly_linked_list import DoublyLinkedList


class EmergencyService:
    def __init__(self):
        # Inicializamos nuestras tres estructuras de datos (colas de prioridad)
        self.high_priority_list = DoublyLinkedList()  # Prioridad 8 a 10
        self.medium_priority_list = DoublyLinkedList()  # Prioridad 4 a 7
        self.low_priority_list = DoublyLinkedList()  # Prioridad 1 a 3

    def _calculate_priority(self, emergency):
        """
        Calcula la prioridad de 1 a 10 basándose en reglas de negocio.
        """
        # 1. Puntaje base según la gravedad típica del incidente
        base_scores = {
            "Terremoto": 3,
            "Incendio": 3,
            "Urgencia Médica": 2,
            "Accidente de tráfico": 1,
            "Robo": 2,
            "Otro": 1
        }

        # Obtenemos el puntaje base (si no coincide, por defecto es 1)
        score = base_scores.get(emergency.tipo_emergencia, 1)

        # 2. Agregamos peso por víctimas
        score += emergency.heridos * 2  # Cada herido suma 1 punto
        score += emergency.muertos * 1  # Cada muerto suma 3 puntos (mayor urgencia)

        # 3. Limitamos el valor para que siempre esté entre 1 y 10
        prioridad_final = min(10, max(1, score))
        return prioridad_final

    def _obtener_lista_por_nombre(self, nombre_lista):
        """Devuelve el objeto DoublyLinkedList correspondiente a un nombre de lista."""
        mapa = {
            "Alta Prioridad": self.high_priority_list,
            "Media Prioridad": self.medium_priority_list,
            "Baja Prioridad": self.low_priority_list,
        }
        return mapa[nombre_lista]

    def _lista_por_prioridad(self, prioridad):
        """Dado un valor de prioridad, devuelve (lista, nombre_lista) donde debe vivir."""
        if prioridad >= 8:
            return self.high_priority_list, "Alta Prioridad"
        elif prioridad >= 4:
            return self.medium_priority_list, "Media Prioridad"
        else:
            return self.low_priority_list, "Baja Prioridad"

    def register_emergency(self, nombre, direccion, descripcion, heridos, muertos, tipo):
        """
        Crea la emergencia, calcula su prioridad y la encola en la lista correcta.
        """
        # 1. Crear el objeto modelo
        nueva_emergencia = Emergency(nombre, direccion, descripcion, heridos, muertos, tipo)

        # 2. Calcular y asignar la prioridad al modelo
        nueva_emergencia.prioridad = self._calculate_priority(nueva_emergencia)

        # 3. Almacenar en la estructura de datos correspondiente usando inserción ordenada
        if nueva_emergencia.prioridad >= 8:
            nodo = self.high_priority_list.insert_sorted(nueva_emergencia)
            lista_destino = "Alta Prioridad"

        elif nueva_emergencia.prioridad >= 4:
            nodo = self.medium_priority_list.insert_sorted(nueva_emergencia)
            lista_destino = "Media Prioridad"

        else:
            nodo = self.low_priority_list.insert_sorted(nueva_emergencia)
            lista_destino = "Baja Prioridad"

        return nodo, lista_destino

    def get_all_emergencies(self):
        """
        Devuelve las tres listas de emergencias (como listas de nodos),
        ya ordenadas por prioridad/ticket, listas para mostrar en la UI.
        """
        return {
            "Alta Prioridad": self.high_priority_list.to_list(),
            "Media Prioridad": self.medium_priority_list.to_list(),
            "Baja Prioridad": self.low_priority_list.to_list(),
        }

    def update_emergency(self, lista_actual_nombre, ticket, nombre, direccion, descripcion, heridos, muertos, tipo):
        """
        Actualiza los datos de una emergencia existente. Recalcula su prioridad y:
        - si el nuevo rango es el mismo, la reordena dentro de la misma lista.
        - si cambia de rango, la mueve a la lista que le corresponda ahora.
        """
        lista_actual = self._obtener_lista_por_nombre(lista_actual_nombre)
        nodo = lista_actual.search(ticket)
        if nodo is None:
            return None, None

        # 1. Sacamos el nodo de donde está (sin perder el objeto ni su ticket)
        lista_actual._desenlazar(nodo)

        # 2. Actualizamos sus datos y recalculamos prioridad
        emergencia = nodo.data
        emergencia.nombre = nombre
        emergencia.direccion = direccion
        emergencia.descripcion = descripcion
        emergencia.heridos = int(heridos)
        emergencia.muertos = int(muertos)
        emergencia.tipo_emergencia = tipo
        emergencia.prioridad = self._calculate_priority(emergencia)

        # 3. La insertamos ordenadamente en la lista que le corresponda ahora
        #    (puede ser la misma lista, o una distinta si cambió de rango)
        lista_destino, nombre_lista_destino = self._lista_por_prioridad(emergencia.prioridad)
        lista_destino._insertar_nodo_ordenado(nodo)

        return nodo, nombre_lista_destino
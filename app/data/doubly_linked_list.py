from app.data.node import Node


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.ticket_counter = 1

    def is_initial_node(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
            return True
        return False

    def insert_front(self, data):
        new_node = Node(data, self.ticket_counter)
        self.ticket_counter += 1

        if self.is_initial_node(new_node):
            return new_node

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        return new_node

    def insert_back(self, data):
        new_node = Node(data, self.ticket_counter)
        self.ticket_counter += 1

        if self.is_initial_node(new_node):
            return new_node

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node
        return new_node

    def print_forward(self):
        if self.head is None:
            print("List is empty")
            return

        current = self.head
        while current:
            print(f"Ticket #{current.ticket} - Data: {current.data}")
            current = current.next

    def print_backward(self):
        if self.tail is None:
            print("List is empty")
            return

        current = self.tail
        while current:
            print(f"Ticket #{current.ticket} - Data: {current.data}")
            current = current.prev

    def search(self, ticket):
        current = self.head
        while current:
            if current.ticket == ticket:
                return current
            current = current.next
        return None

    def _desenlazar(self, node):
        """Saca el nodo de la lista sin borrarlo (lo deja listo para reinsertar)."""
        if self.head == self.tail:  # único nodo en la lista
            self.head = None
            self.tail = None
        elif node == self.head:
            self.head = node.next
            self.head.prev = None
        elif node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.next = None
        node.prev = None

    def delete(self, ticket):
        node = self.search(ticket)
        if node is None:
            return False
        self._desenlazar(node)
        return True

    def _va_antes(self, node_actual, node_nuevo):
        """
        True si 'node_actual' debe quedar ANTES que 'node_nuevo' en la lista.
        Criterio: mayor prioridad primero; en empate, menor ticket (llegó antes) primero.
        """
        if node_actual.data.prioridad != node_nuevo.data.prioridad:
            return node_actual.data.prioridad > node_nuevo.data.prioridad
        return node_actual.ticket < node_nuevo.ticket

    def _insertar_nodo_ordenado(self, new_node):
        """Inserta un nodo (nuevo o reciclado, conservando su ticket) en la posición correcta."""
        if self.is_initial_node(new_node):
            return new_node

        current = self.head
        while current and self._va_antes(current, new_node):
            current = current.next

        # Caso 1: llegamos al final (prioridad más baja de la lista)
        if current is None:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        # Caso 2: va antes de la cabeza actual
        elif current == self.head:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        # Caso 3: en el medio (antes de 'current')
        else:
            new_node.prev = current.prev
            new_node.next = current
            current.prev.next = new_node
            current.prev = new_node

        return new_node

    def insert_sorted(self, data):
        new_node = Node(data, self.ticket_counter)
        self.ticket_counter += 1
        return self._insertar_nodo_ordenado(new_node)

    def update_priority(self, ticket, nueva_prioridad):
        """
        Actualiza la prioridad de una emergencia existente y la reubica
        en la posición correcta, respetando el desempate por ticket.
        """
        node = self.search(ticket)
        if node is None:
            return False

        self._desenlazar(node)
        node.data.prioridad = nueva_prioridad
        self._insertar_nodo_ordenado(node)
        return True

    def to_list(self):
        """Devuelve los nodos en orden, de head a tail, sin imprimir nada."""
        resultado = []
        current = self.head
        while current:
            resultado.append(current)
            current = current.next
        return resultado
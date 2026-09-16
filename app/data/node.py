class Node:
    def __init__(self, data, ticket):
        self.data = data  # Aquí guardaremos el objeto Emergency
        self.ticket = ticket  # El número de llegada (1, 2, 3...)

        # Apuntadores para la lista doblemente enlazada
        self.next = None  # Apunta al siguiente nodo
        self.prev = None  # Apunta al nodo anterior
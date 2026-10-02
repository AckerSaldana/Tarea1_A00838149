"""Queue (cola, FIFO) implementada con una lista simplemente ligada.

Se guardan referencias al frente y al final para que enqueue y dequeue
sean O(1). (Usar list.pop(0) de Python costaría O(n)).
"""


class QueueVaciaError(Exception):
    """Se lanza al hacer dequeue, front o rear sobre una cola vacía."""


class _Nodo:
    __slots__ = ("valor", "siguiente")

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


class Queue:
    def __init__(self, iterable=None):
        self._frente = None
        self._final = None
        self._tam = 0
        if iterable is not None:
            for elemento in iterable:
                self.enqueue(elemento)

    def enqueue(self, elemento):
        """Agrega un elemento al final."""
        nodo = _Nodo(elemento)
        if self._final is None:
            self._frente = self._final = nodo
        else:
            self._final.siguiente = nodo
            self._final = nodo
        self._tam += 1

    def dequeue(self):
        """Quita y regresa el elemento del frente."""
        if self.is_empty():
            raise QueueVaciaError("dequeue sobre una Queue vacía")
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:
            self._final = None
        self._tam -= 1
        return nodo.valor

    def front(self):
        """Regresa el elemento del frente sin quitarlo."""
        if self.is_empty():
            raise QueueVaciaError("front sobre una Queue vacía")
        return self._frente.valor

    def rear(self):
        """Regresa el último elemento sin quitarlo."""
        if self.is_empty():
            raise QueueVaciaError("rear sobre una Queue vacía")
        return self._final.valor

    def is_empty(self):
        return self._tam == 0

    def size(self):
        return self._tam

    def clear(self):
        self._frente = self._final = None
        self._tam = 0

    def __len__(self):
        return self._tam

    def __iter__(self):
        """Recorre del frente hacia el final."""
        actual = self._frente
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __repr__(self):
        return f"Queue(frente -> {list(self)})"

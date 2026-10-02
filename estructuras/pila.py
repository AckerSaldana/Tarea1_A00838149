"""Stack (pila, LIFO) implementada sobre un arreglo dinámico.

Complejidad: push, pop, peek, is_empty y size en O(1) (push amortizado).
"""


class StackVaciaError(Exception):
    """Se lanza al hacer pop o peek sobre una pila vacía."""


class Stack:
    def __init__(self, iterable=None):
        self._datos = []
        if iterable is not None:
            for elemento in iterable:
                self.push(elemento)

    def push(self, elemento):
        """Agrega un elemento en el tope."""
        self._datos.append(elemento)

    def pop(self):
        """Quita y regresa el elemento del tope."""
        if self.is_empty():
            raise StackVaciaError("pop sobre un Stack vacío")
        return self._datos.pop()

    def peek(self):
        """Regresa el elemento del tope sin quitarlo."""
        if self.is_empty():
            raise StackVaciaError("peek sobre un Stack vacío")
        return self._datos[-1]

    def is_empty(self):
        return len(self._datos) == 0

    def size(self):
        return len(self._datos)

    def clear(self):
        self._datos.clear()

    def __len__(self):
        return self.size()

    def __iter__(self):
        """Recorre del tope hacia la base."""
        return reversed(self._datos)

    def __repr__(self):
        return f"Stack(tope -> {list(self)})"

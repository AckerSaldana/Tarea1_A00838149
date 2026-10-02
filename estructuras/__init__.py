"""Estructuras de datos clásicas: Stack (LIFO), Queue (FIFO) y HashTable (diccionario)."""
from .pila import Stack, StackVaciaError
from .cola import Queue, QueueVaciaError
from .tabla_hash import HashTable

__all__ = ["Stack", "StackVaciaError", "Queue", "QueueVaciaError", "HashTable"]

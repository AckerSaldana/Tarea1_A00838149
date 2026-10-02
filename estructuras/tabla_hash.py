"""HashTable (diccionario) con encadenamiento y orden de inserción.

Diseño (similar al dict compacto de CPython):
  * _entradas: lista de pares [clave, valor] en orden de inserción;
    una entrada borrada se marca con None (lápida).
  * _buckets: cada bucket guarda índices hacia _entradas. Las colisiones
    se resuelven por encadenamiento (separate chaining).
  * Cuando (entradas usadas / capacidad) supera el factor de carga se
    redimensiona: se duplica la capacidad si hay muchas claves vivas, o
    solo se compacta si la mayoría eran lápidas.

Complejidad esperada: put, get, remove y contains en O(1) promedio.
Recorrer keys/values/items respeta el orden de inserción.
"""


class HashTable:
    CAPACIDAD_MINIMA = 8

    def __init__(self, capacidad=8, factor_carga=0.75):
        if not 0 < factor_carga <= 1:
            raise ValueError("factor_carga debe estar en (0, 1]")
        self._capacidad = max(self.CAPACIDAD_MINIMA, int(capacidad))
        self._factor = factor_carga
        self._buckets = [[] for _ in range(self._capacidad)]
        self._entradas = []
        self._n = 0

    # ---- utilidades internas ----
    def _indice(self, clave):
        return hash(clave) % self._capacidad

    def _buscar(self, clave):
        """Regresa (bucket, posición en _entradas o None)."""
        b = self._indice(clave)
        for pos in self._buckets[b]:
            k = self._entradas[pos][0]
            if k is clave or k == clave:
                return b, pos
        return b, None

    def _redimensionar(self, nueva_capacidad):
        vivas = [e for e in self._entradas if e is not None]
        self._capacidad = max(self.CAPACIDAD_MINIMA, nueva_capacidad)
        self._buckets = [[] for _ in range(self._capacidad)]
        self._entradas = []
        for clave, valor in vivas:
            self._buckets[self._indice(clave)].append(len(self._entradas))
            self._entradas.append([clave, valor])

    # ---- operaciones principales ----
    def put(self, clave, valor):
        """Inserta o actualiza el valor asociado a clave."""
        b, pos = self._buscar(clave)
        if pos is not None:
            self._entradas[pos][1] = valor
            return
        self._buckets[b].append(len(self._entradas))
        self._entradas.append([clave, valor])
        self._n += 1
        if len(self._entradas) / self._capacidad > self._factor:
            if self._n / self._capacidad > self._factor / 2:
                self._redimensionar(self._capacidad * 2)
            else:
                self._redimensionar(self._capacidad)  # solo compacta lápidas

    def get(self, clave, default=None):
        """Regresa el valor de clave, o default si no existe."""
        _, pos = self._buscar(clave)
        return default if pos is None else self._entradas[pos][1]

    def remove(self, clave):
        """Elimina clave y regresa su valor. Lanza KeyError si no existe."""
        b, pos = self._buscar(clave)
        if pos is None:
            raise KeyError(clave)
        valor = self._entradas[pos][1]
        self._buckets[b].remove(pos)
        self._entradas[pos] = None
        self._n -= 1
        return valor

    def contains(self, clave):
        return self._buscar(clave)[1] is not None

    def keys(self):
        return [e[0] for e in self._entradas if e is not None]

    def values(self):
        return [e[1] for e in self._entradas if e is not None]

    def items(self):
        return [(e[0], e[1]) for e in self._entradas if e is not None]

    def is_empty(self):
        return self._n == 0

    def size(self):
        return self._n

    def clear(self):
        self.__init__(self.CAPACIDAD_MINIMA, self._factor)

    @property
    def capacidad(self):
        return self._capacidad

    # ---- sintaxis de diccionario ----
    def __setitem__(self, clave, valor):
        self.put(clave, valor)

    def __getitem__(self, clave):
        _, pos = self._buscar(clave)
        if pos is None:
            raise KeyError(clave)
        return self._entradas[pos][1]

    def __delitem__(self, clave):
        self.remove(clave)

    def __contains__(self, clave):
        return self.contains(clave)

    def __len__(self):
        return self._n

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        cuerpo = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashTable({{{cuerpo}}})"

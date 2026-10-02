# Tarea 1: Stack, Queue y HashTable

**Repositorio Git:** https://github.com/AckerSaldana/Tarea1_A00838149

## Descripción breve

Implementé en Python 3 tres estructuras de datos clásicas que usaré en el mini proyecto (compilador): una pila (Stack, LIFO), una cola (Queue, FIFO) y una tabla hash (HashTable, diccionario). Además incluí un programa de demostración y un conjunto de pruebas unitarias.

**¿Las programé desde 0?** Sí. Las tres estructuras están escritas desde cero; no envuelven `collections.deque`, `queue.Queue` ni `dict`. La pila se apoya en una lista de Python como arreglo dinámico, la cola es una lista ligada propia con nodos y la tabla hash maneja sus propios buckets, colisiones y redimensionamiento.

**¿Usé alguna librería?** Ninguna librería externa. Solo se usa la biblioteca estándar de Python: el módulo `unittest` para las pruebas y la función integrada `hash()` para calcular el valor hash de las claves.

**¿Las solicité a alguna herramienta de IA?** Sí. Usé Claude (modelo Claude Opus 5.5, de Anthropic) en claude.ai. La consulta fue adjuntar una captura de pantalla con el enunciado completo de la Tarea #1 y pedir la implementación de las estructuras, junto con una descripcion y breve codigo de los test cases que queria poner y una version de este README escrita de peor manera para que la reescribiera mejor. Después revisé el código y lo ejecuté localmente para confirmar que todas las pruebas pasan.

## Estructura del proyecto

```
estructuras/
  pila.py         Stack (LIFO) sobre arreglo dinámico
  cola.py         Queue (FIFO) sobre lista ligada
  tabla_hash.py   HashTable con encadenamiento y orden de inserción
demo.py           Programa que manipula las tres estructuras
tests/
  test_estructuras.py   33 pruebas unitarias
```

Para ejecutar: `python demo.py` y `python -m unittest -v`.

## Operaciones implementadas

| Estructura | Operaciones                                                                                                      | Complejidad   |
| ---------- | ---------------------------------------------------------------------------------------------------------------- | ------------- |
| Stack      | push, pop, peek, is_empty, size, clear, iteración                                                                | O(1)          |
| Queue      | enqueue, dequeue, front, rear, is_empty, size, clear, iteración                                                  | O(1)          |
| HashTable  | put, get, remove, contains, keys, values, items, size, clear (también con sintaxis `t[k]`, `del t[k]`, `k in t`) | O(1) promedio |

La cola usa una lista ligada con referencias al frente y al final para que enqueue y dequeue sean O(1). La tabla hash resuelve colisiones por encadenamiento, conserva el orden de inserción y se redimensiona cuando el factor de carga supera 0.75. El programa `demo.py` muestra un uso típico de cada estructura en un compilador: la pila valida paréntesis y llaves balanceados, la cola representa el flujo de tokens que consume el parser y la tabla hash funciona como tabla de símbolos.

## Descripción de los test cases

Las 33 pruebas están en `tests/test_estructuras.py` y cubren tres tipos de situaciones: el funcionamiento normal de cada operación, los casos de error (operar sobre una estructura vacía o buscar algo que no existe) y casos límite como volúmenes grandes, colisiones o tipos de datos poco comunes. **Resultado: 33 de 33 pruebas aprobadas.**

### Stack (9 pruebas)

1. **Pila nueva vacía.** Se crea una pila sin elementos y se verifica que `is_empty()` regrese verdadero y `size()` regrese 0. Confirma que el estado inicial es correcto.
2. **Orden LIFO.** Se insertan 1, 2 y 3 y se hacen tres `pop()`. Deben salir en orden 3, 2, 1, lo que comprueba que el último en entrar es el primero en salir.
3. **peek no modifica la pila.** Con los elementos 1 y 2, `peek()` debe regresar 2 y el tamaño debe seguir siendo 2. Distingue consultar el tope de extraerlo.
4. **pop sobre pila vacía.** Debe lanzar `StackVaciaError` en lugar de fallar con un error genérico o regresar un valor inválido.
5. **peek sobre pila vacía.** Igual que el anterior, debe lanzar `StackVaciaError`.
6. **clear.** Se llena la pila con cinco elementos, se vacía y se verifica que quede vacía.
7. **Iteración.** Al recorrer una pila con 1, 2 y 3 se obtiene [3, 2, 1], es decir, del tope hacia la base.
8. **Volumen.** Se insertan 10 000 elementos; el tamaño debe ser 10 000 y el tope 9 999. Comprueba que la estructura escala sin perder datos.
9. **Tipos mixtos.** Se guardan un entero, un texto, `None` y una tupla, y se verifica que se recuperen intactos. Esto importa porque `None` podría confundirse con "no hay elemento".

### Queue (9 pruebas)

1. **Cola nueva vacía.** Verifica que inicie vacía y con tamaño 0.
2. **Orden FIFO.** Se encolan 1, 2 y 3 y se desencolan; deben salir 1, 2, 3, comprobando que el primero en entrar es el primero en salir.
3. **front y rear.** Con "a", "b" y "c", `front()` debe regresar "a" y `rear()` debe regresar "c", sin cambiar el tamaño.
4. **dequeue sobre cola vacía.** Debe lanzar `QueueVaciaError`.
5. **front y rear sobre cola vacía.** Ambos deben lanzar `QueueVaciaError`.
6. **Reutilizar tras vaciar.** Se encola un elemento, se desencola y luego se encola otro; frente y final deben apuntar al nuevo elemento. Detecta el error común de la lista ligada de dejar la referencia al final apuntando a un nodo ya eliminado.
7. **Operaciones intercaladas.** Se mezclan enqueue y dequeue (encolar 1 y 2, sacar 1, encolar 3) y el contenido final debe ser [2, 3].
8. **clear.** Tras vaciar la cola, debe quedar vacía y `front()` debe lanzar error.
9. **Volumen.** Se encolan 10 000 elementos; el primer dequeue debe regresar 0 y quedar 9 999 elementos.

### HashTable (15 pruebas)

1. **Tabla nueva vacía.** Verifica que inicie vacía y con tamaño 0.
2. **put y get.** Se guarda la clave "x" con valor 1 y se recupera tanto con `get("x")` como con `t["x"]`.
3. **Actualizar una clave.** Asignar dos veces la misma clave debe sustituir el valor sin crear un duplicado: el valor final es 2 y el tamaño sigue en 1.
4. **get de clave inexistente.** Debe regresar `None` o el valor por omisión indicado, sin lanzar error.
5. **Acceso con corchetes a clave inexistente.** `t["w"]` debe lanzar `KeyError`, igual que un diccionario de Python.
6. **remove.** Al borrar una clave se regresa su valor, la clave deja de existir y el tamaño baja a 0.
7. **remove de clave inexistente.** Debe lanzar `KeyError`.
8. **contains con valor None.** Se guarda una clave cuyo valor es `None` y se verifica que `in` la encuentre. Asegura que la tabla distingue entre "la clave existe con valor None" y "la clave no existe".
9. **Colisiones forzadas.** Se usa una clase de prueba cuyo hash siempre es 42, de modo que 20 claves distintas caen en el mismo bucket. Todas deben recuperarse con su valor correcto, y al borrar una las demás deben seguir accesibles. Es la prueba principal del encadenamiento.
10. **Redimensión.** Se insertan 1 000 claves; la capacidad debe crecer respecto a la inicial y todos los valores deben seguir siendo correctos tras el rehash.
11. **Orden de inserción.** Se insertan "c", "a" y "b", se borra "a" y se inserta "d". `keys()`, `values()` e `items()` deben respetar el orden c, b, d.
12. **Muchos borrados.** Se insertan y borran 500 claves una por una. La tabla debe quedar vacía y compactarse en lugar de crecer sin control por las entradas eliminadas.
13. **Distintos tipos de clave.** Se usan como claves el entero `1`, el texto `"1"` y la tupla `(1, 2)`. Las tres deben coexistir como claves distintas.
14. **Clave no hasheable.** Usar una lista como clave debe lanzar `TypeError`, ya que una clave mutable rompería la tabla.
15. **clear.** Tras insertar 50 claves y vaciar la tabla, el tamaño debe ser 0 y no debe haber claves.

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2022). _Introduction to Algorithms_ (4a ed.). MIT Press. Capítulos 10 y 11.

Python Software Foundation. _unittest: Unit testing framework_. https://docs.python.org/3/library/unittest.html

# Tarea 1: Stack, Queue y HashTable

Implementación desde cero, en Python 3, de tres estructuras de datos clásicas que se usarán en el mini proyecto (compilador): una pila (LIFO), una cola (FIFO) y una tabla hash (diccionario). No se usan librerías externas.

## Estructura del repositorio

```
estructuras/
  pila.py         Stack (LIFO) sobre arreglo dinámico
  cola.py         Queue (FIFO) sobre lista ligada
  tabla_hash.py   HashTable con encadenamiento y orden de inserción
demo.py           Programa que manipula las tres estructuras
tests/
  test_estructuras.py   33 pruebas unitarias (unittest)
```

## Cómo ejecutar

```
python demo.py
python -m unittest -v
```

## Operaciones implementadas

| Estructura | Operaciones                                                                                         | Complejidad   |
| ---------- | --------------------------------------------------------------------------------------------------- | ------------- |
| Stack      | push, pop, peek, is_empty, size, clear, iteración                                                   | O(1)          |
| Queue      | enqueue, dequeue, front, rear, is_empty, size, clear, iteración                                     | O(1)          |
| HashTable  | put / `t[k]=v`, get, `t[k]`, remove / `del t[k]`, contains / `in`, keys, values, items, size, clear | O(1) promedio |

**Stack** usa una lista de Python como arreglo dinámico; el tope es el final de la lista. **Queue** usa una lista ligada con referencias al frente y al final, para que tanto enqueue como dequeue sean O(1) (usar `list.pop(0)` sería O(n)). **HashTable** resuelve colisiones por encadenamiento: cada bucket guarda índices hacia un arreglo de entradas que conserva el orden de inserción. Al borrar se deja una lápida, y cuando el factor de carga supera 0.75 la tabla se redimensiona al doble o solo se compacta si la mayoría eran lápidas.

El programa `demo.py` muestra además un uso típico de cada estructura en un compilador: la pila valida paréntesis y llaves balanceados, la cola representa el flujo de tokens que consume el parser y la tabla hash funciona como tabla de símbolos.

## Test cases

### Stack (9 pruebas)

| Caso          | Qué valida                    | Resultado esperado                 |
| ------------- | ----------------------------- | ---------------------------------- |
| Pila nueva    | Estado inicial                | `is_empty()` verdadero, `size()` 0 |
| Orden LIFO    | push 1, 2, 3 y pop tres veces | 3, 2, 1                            |
| peek          | Consultar el tope             | Regresa 2 y el tamaño no cambia    |
| pop en vacía  | Caso de error                 | `StackVaciaError`                  |
| peek en vacía | Caso de error                 | `StackVaciaError`                  |
| clear         | Vaciar la pila                | Queda vacía                        |
| Iteración     | Orden de recorrido            | Del tope a la base                 |
| Volumen       | 10 000 elementos              | Tamaño correcto y tope 9 999       |
| Tipos mixtos  | int, str, None, tupla         | Se recuperan intactos              |

### Queue (9 pruebas)

| Caso                     | Qué valida                           | Resultado esperado                |
| ------------------------ | ------------------------------------ | --------------------------------- |
| Cola nueva               | Estado inicial                       | Vacía, tamaño 0                   |
| Orden FIFO               | enqueue 1, 2, 3 y dequeue tres veces | 1, 2, 3                           |
| front y rear             | Consultar extremos                   | "a" y "c" sin modificar el tamaño |
| dequeue en vacía         | Caso de error                        | `QueueVaciaError`                 |
| front/rear en vacía      | Caso de error                        | `QueueVaciaError`                 |
| Reutilizar tras vaciar   | Que front y rear se reinicien bien   | Ambos apuntan al nuevo elemento   |
| Operaciones intercaladas | enqueue y dequeue mezclados          | Contenido final [2, 3]            |
| clear                    | Vaciar la cola                       | Vacía y front lanza error         |
| Volumen                  | 10 000 elementos                     | Primer dequeue regresa 0          |

### HashTable (15 pruebas)

| Caso                    | Qué valida                     | Resultado esperado                                |
| ----------------------- | ------------------------------ | ------------------------------------------------- |
| Tabla nueva             | Estado inicial                 | Vacía, tamaño 0                                   |
| put y get               | Inserción y consulta           | Regresa el valor guardado                         |
| Actualizar clave        | Reasignar una clave existente  | Nuevo valor, tamaño sigue en 1                    |
| get inexistente         | Valor por omisión              | None o el default indicado                        |
| `t[k]` inexistente      | Caso de error                  | `KeyError`                                        |
| remove                  | Borrar una clave               | Regresa el valor y ya no existe                   |
| remove inexistente      | Caso de error                  | `KeyError`                                        |
| contains con valor None | No confundir None con ausencia | `in` es verdadero                                 |
| Colisiones forzadas     | 20 claves con el mismo hash    | Todas recuperables, también tras borrar una       |
| Redimensión             | 1 000 inserciones              | Capacidad crece y todos los valores son correctos |
| Orden de inserción      | Insertar, borrar e insertar    | keys, values e items respetan el orden            |
| Muchos borrados         | 500 inserciones y borrados     | Se compacta sin crecer de más                     |
| Tipos de clave          | int, str y tupla               | `1` y `"1"` son claves distintas                  |
| Clave no hasheable      | Usar una lista como clave      | `TypeError`                                       |
| clear                   | Vaciar la tabla                | Tamaño 0 y sin claves                             |

Resultado: **33 de 33 pruebas aprobadas.**

## Uso de IA

**Herramienta:** Claude (modelo Claude Opus 5.5, de Anthropic), a través de claude.ai.

**Consulta realizada (prompt):** Se adjuntó una captura de pantalla con el enunciado completo de la Tarea #1 (implementar STACK, QUEUE y TABLE/HASH/DICTIONARY con sus operaciones clásicas, un programa de demostración y la descripción de los test cases) junto con un codigo ya medio hecho para generar correcciones y comentarios

**Qué generó la IA:** el código de las tres estructuras, el programa de demostración, las pruebas unitarias y escribio de mejor manera este README. El código fue revisado y ejecutado localmente para verificar que todas las pruebas pasan.

## Referencias

Cormen, T. H., Leiserson, C. E., Rivest, R. L. y Stein, C. (2022). _Introduction to Algorithms_ (4a ed.). MIT Press. Capítulos 10 (estructuras elementales) y 11 (tablas hash).

Python Software Foundation. _unittest: Unit testing framework_. https://docs.python.org/3/library/unittest.html

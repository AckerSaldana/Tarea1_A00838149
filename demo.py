"""Programa de demostración de Stack, Queue y HashTable.

Además de las operaciones básicas, muestra un uso típico de cada
estructura dentro de un compilador:
  Stack     -> validar paréntesis/llaves balanceados
  Queue     -> flujo de tokens que consume el parser
  HashTable -> tabla de símbolos (variables y sus tipos)
"""
from estructuras import Stack, Queue, HashTable, StackVaciaError, QueueVaciaError


def titulo(t):
    print(f"\n{'=' * 50}\n{t}\n{'=' * 50}")


def demo_stack():
    titulo("STACK (LIFO)")
    s = Stack()
    for x in [10, 20, 30]:
        s.push(x)
        print(f"push({x}) -> {s}")
    print("peek() =", s.peek())
    print("pop()  =", s.pop(), "->", s)
    print("size() =", s.size(), "| is_empty() =", s.is_empty())
    s.clear()
    try:
        s.pop()
    except StackVaciaError as e:
        print("Error controlado:", e)

    def balanceado(expr):
        pares = {")": "(", "]": "[", "}": "{"}
        pila = Stack()
        for c in expr:
            if c in "([{":
                pila.push(c)
            elif c in pares:
                if pila.is_empty() or pila.pop() != pares[c]:
                    return False
        return pila.is_empty()

    for expr in ["if (a[i] > {b}) {}", "(a + b]", "((x)"]:
        print(f"Balanceado {expr!r}: {balanceado(expr)}")


def demo_queue():
    titulo("QUEUE (FIFO)")
    q = Queue()
    for x in ["A", "B", "C"]:
        q.enqueue(x)
        print(f"enqueue({x!r}) -> {q}")
    print("front() =", q.front(), "| rear() =", q.rear())
    print("dequeue() =", q.dequeue(), "->", q)
    q.clear()
    try:
        q.dequeue()
    except QueueVaciaError as e:
        print("Error controlado:", e)

    tokens = Queue([("INT", "int"), ("ID", "x"), ("ASSIGN", "="), ("NUM", "5"), ("SEMI", ";")])
    print("Parser consumiendo tokens en orden:")
    while not tokens.is_empty():
        print("  ", tokens.dequeue())


def demo_hash():
    titulo("HASHTABLE / DICTIONARY")
    t = HashTable()
    t.put("x", "int")
    t["y"] = "float"
    t["z"] = "bool"
    print("Tabla:", t)
    print("get('y') =", t.get("y"), "| get('w', 'N/A') =", t.get("w", "N/A"))
    print("'x' in t =", "x" in t, "| 'w' in t =", "w" in t)
    t["x"] = "char"
    print("Actualizar x -> char:", t)
    print("remove('y') =", t.remove("y"), "->", t)
    print("keys:", t.keys(), "| values:", t.values())
    try:
        t["no_existe"]
    except KeyError as e:
        print("Error controlado: KeyError", e)

    grande = HashTable()
    for i in range(100):
        grande[f"var{i}"] = i
    print(f"100 inserciones -> size={grande.size()}, capacidad={grande.capacidad}")


if __name__ == "__main__":
    demo_stack()
    demo_queue()
    demo_hash()

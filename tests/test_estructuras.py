"""Pruebas unitarias. Ejecutar con: python -m unittest -v"""
import unittest
from estructuras import Stack, Queue, HashTable, StackVaciaError, QueueVaciaError


class TestStack(unittest.TestCase):
    def test_nueva_vacia(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(s.size(), 0)

    def test_orden_lifo(self):
        s = Stack([1, 2, 3])
        self.assertEqual([s.pop(), s.pop(), s.pop()], [3, 2, 1])

    def test_peek_no_modifica(self):
        s = Stack([1, 2])
        self.assertEqual(s.peek(), 2)
        self.assertEqual(s.size(), 2)

    def test_pop_vacia_lanza_error(self):
        with self.assertRaises(StackVaciaError):
            Stack().pop()

    def test_peek_vacia_lanza_error(self):
        with self.assertRaises(StackVaciaError):
            Stack().peek()

    def test_clear(self):
        s = Stack(range(5))
        s.clear()
        self.assertTrue(s.is_empty())

    def test_iteracion_tope_a_base(self):
        self.assertEqual(list(Stack([1, 2, 3])), [3, 2, 1])

    def test_volumen(self):
        s = Stack()
        for i in range(10_000):
            s.push(i)
        self.assertEqual(len(s), 10_000)
        self.assertEqual(s.pop(), 9_999)

    def test_tipos_mixtos(self):
        s = Stack([1, "a", None, (2, 3)])
        self.assertEqual(s.pop(), (2, 3))
        self.assertIsNone(s.pop())


class TestQueue(unittest.TestCase):
    def test_nueva_vacia(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_orden_fifo(self):
        q = Queue([1, 2, 3])
        self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])

    def test_front_y_rear(self):
        q = Queue(["a", "b", "c"])
        self.assertEqual(q.front(), "a")
        self.assertEqual(q.rear(), "c")
        self.assertEqual(q.size(), 3)

    def test_dequeue_vacia_lanza_error(self):
        with self.assertRaises(QueueVaciaError):
            Queue().dequeue()

    def test_front_rear_vacia_lanzan_error(self):
        with self.assertRaises(QueueVaciaError):
            Queue().front()
        with self.assertRaises(QueueVaciaError):
            Queue().rear()

    def test_reutilizar_tras_vaciar(self):
        q = Queue([1])
        q.dequeue()
        q.enqueue(2)
        self.assertEqual(q.front(), 2)
        self.assertEqual(q.rear(), 2)

    def test_intercalado(self):
        q = Queue()
        q.enqueue(1); q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)
        self.assertEqual(list(q), [2, 3])

    def test_clear(self):
        q = Queue(range(5))
        q.clear()
        self.assertTrue(q.is_empty())
        with self.assertRaises(QueueVaciaError):
            q.front()

    def test_volumen(self):
        q = Queue(range(10_000))
        self.assertEqual(q.dequeue(), 0)
        self.assertEqual(len(q), 9_999)


class ClaveColision:
    """Clave cuyo hash es siempre igual, para forzar colisiones."""
    def __init__(self, n):
        self.n = n

    def __hash__(self):
        return 42

    def __eq__(self, otra):
        return isinstance(otra, ClaveColision) and self.n == otra.n


class TestHashTable(unittest.TestCase):
    def test_nueva_vacia(self):
        t = HashTable()
        self.assertTrue(t.is_empty())
        self.assertEqual(t.size(), 0)

    def test_put_get(self):
        t = HashTable()
        t.put("x", 1)
        self.assertEqual(t.get("x"), 1)
        self.assertEqual(t["x"], 1)

    def test_actualizar_no_duplica(self):
        t = HashTable()
        t["x"] = 1
        t["x"] = 2
        self.assertEqual(t["x"], 2)
        self.assertEqual(len(t), 1)

    def test_get_inexistente_default(self):
        t = HashTable()
        self.assertIsNone(t.get("w"))
        self.assertEqual(t.get("w", -1), -1)

    def test_getitem_inexistente_keyerror(self):
        with self.assertRaises(KeyError):
            HashTable()["w"]

    def test_remove(self):
        t = HashTable()
        t["a"] = 1
        self.assertEqual(t.remove("a"), 1)
        self.assertNotIn("a", t)
        self.assertEqual(len(t), 0)

    def test_remove_inexistente_keyerror(self):
        with self.assertRaises(KeyError):
            HashTable().remove("w")

    def test_contains(self):
        t = HashTable()
        t["a"] = None  # valor None no debe confundirse con ausencia
        self.assertIn("a", t)
        self.assertNotIn("b", t)

    def test_colisiones(self):
        t = HashTable()
        claves = [ClaveColision(i) for i in range(20)]
        for i, k in enumerate(claves):
            t[k] = i
        for i, k in enumerate(claves):
            self.assertEqual(t[k], i)
        t.remove(claves[5])
        self.assertNotIn(claves[5], t)
        self.assertEqual(t[claves[6]], 6)

    def test_redimension(self):
        t = HashTable()
        cap_inicial = t.capacidad
        for i in range(1_000):
            t[i] = i * i
        self.assertGreater(t.capacidad, cap_inicial)
        self.assertEqual(len(t), 1_000)
        self.assertTrue(all(t[i] == i * i for i in range(1_000)))

    def test_orden_de_insercion(self):
        t = HashTable()
        for k in ["c", "a", "b"]:
            t[k] = k.upper()
        del t["a"]
        t["d"] = "D"
        self.assertEqual(t.keys(), ["c", "b", "d"])
        self.assertEqual(t.values(), ["C", "B", "D"])
        self.assertEqual(t.items(), [("c", "C"), ("b", "B"), ("d", "D")])

    def test_muchos_borrados_compacta(self):
        t = HashTable()
        for i in range(500):
            t[i] = i
            del t[i]
        self.assertTrue(t.is_empty())
        self.assertLessEqual(t.capacidad, 16)

    def test_tipos_de_clave(self):
        t = HashTable()
        t[1] = "int"; t["1"] = "str"; t[(1, 2)] = "tupla"
        self.assertEqual((t[1], t["1"], t[(1, 2)]), ("int", "str", "tupla"))

    def test_clave_no_hasheable(self):
        with self.assertRaises(TypeError):
            HashTable()[[1, 2]] = "lista"

    def test_clear(self):
        t = HashTable()
        for i in range(50):
            t[i] = i
        t.clear()
        self.assertEqual(len(t), 0)
        self.assertEqual(t.keys(), [])


if __name__ == "__main__":
    unittest.main()

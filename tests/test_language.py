import unittest

from core.evaluation.evaluator import Primitive
from monito import Monito


class MonitoTestCase(unittest.TestCase):

    def test_primitive_values(self):

        self.assertTrue(Monito.run('true'))
        self.assertFalse(Monito.run('false'))
        self.assertEqual(Monito.run('2'), 2)
        self.assertEqual(Monito.run('3.14'), 3.14)
        self.assertEqual(Monito.run('"hola"'), "hola")

    def test_and(self):

        self.assertTrue(Monito.run('(and true true)'))
        self.assertFalse(Monito.run('(and true false)'))
        self.assertFalse(Monito.run('(and false true)'))
        self.assertFalse(Monito.run('(and false false)'))

    def test_or(self):

        self.assertTrue(Monito.run('(or true true)'))
        self.assertTrue(Monito.run('(or true false)'))
        self.assertTrue(Monito.run('(or false true)'))
        self.assertFalse(Monito.run('(or false false)'))

    def test_if(self):

        self.assertEqual(Monito.run('(if true 2 3)'), 2)
        self.assertEqual(Monito.run('(if false 2 3)'), 3)
        self.assertEqual(Monito.run('(if (> 4 5) 100 200)'), 200)

    def test_primitive_application(self):

        self.assertTrue(Monito.run('(not false)'))
        self.assertEqual(Monito.run('(sqrt 4)'), 2)
        self.assertEqual(Monito.run('(* 5 (/ 10 2))'), 25)
        self.assertEqual(Monito.run('(list 3 4 5 2 1)'), [3, 4, 5, 2, 1])
        self.assertEqual(Monito.run('(max (list 3 4 5 2 1))'), 5)
        self.assertEqual(Monito.run('(min (list 3 4 5 2 1))'), 1)
        self.assertEqual(Monito.run('(map abs (list 1 -2 3))'), [1, 2, 3])

    def test_closures(self):

        self.assertTrue(Monito.run('((fun (x) x) true)'))
        self.assertEqual(Monito.run(
            '((fun (x y) (+ (* x x) (* y y))) 3 4)'
        ), 25)

    def test_environment(self):

        bindings = {
            'x': 4,
            'hola': Monito.run('(max (list 1 3 2))'),
            '+': Primitive(lambda x, y: x * y)
        }
        runtime = Monito()
        new_env = runtime.environment.new_environment(bindings)

        self.assertEqual(Monito.run('(- 3 x)', new_env), -1)
        self.assertEqual(Monito.run('(- 10 hola)', new_env), 7)
        self.assertEqual(Monito.run('(+ 2 3)', new_env), 6)

    def test_add_python_functions(self):

        def fibonacci(n):
            assert n >= 0

            if n == 0:
                return 0
            if n == 1:
                return 1
            return fibonacci(n - 1) + fibonacci(n - 2)

        runtime = Monito()
        runtime.environment.add_primitives({'fibo': fibonacci})
        self.assertEqual(runtime.eval('(fibo 4)'), 3)
        self.assertEqual(runtime.eval('(fibo 7)'), 13)

    def test_nesting(self):

        code = """
            (if (> (* 0.3 (+ 10 23)) 10)
                esto-no-sera-evaluado-asi-que-pico
                (and
                     (= (head (map abs (list -1 -2 -3))) 1)
                     (<= 11 (/ 100 6))
                )
             )
        """
        self.assertTrue(Monito.run(code))

    def test_define(self):

        code = """
            (define x 2)
            (define y 3)
            (+ x y)
        """
        self.assertEqual(Monito.run(code), 5)

        code = """
            (define factorial
                (fun (n)
                    (if (equal? n 0)
                        1
                        (* n (factorial (- n 1)))
                    )
                )
            )
            (factorial 5)
        """
        self.assertEqual(Monito.run(code), 120)

    def test_begin(self):

        code = """
            (begin
                (define x 1)
                (define y 2)
                (+ x y)
            )
        """
        self.assertEqual(Monito.run(code), 3)

    def test_local_definitions(self):

        code = """
            (local
                (
                    (f (fun (x y) (* x y)))
                    (x (* 2 3))
                )
                (f x 2)
            )
        """
        self.assertEqual(Monito.run(code), 12)

    def test_recursion(self):

        code = """
            (local
                ((factorial
                    (fun (n)
                        (if (equal? n 1)
                            n
                            (* n (factorial (- n 1)))
                        )
                    )
                ))
                (factorial 5)
            )
        """
        self.assertEqual(Monito.run(code), 120)

    def test_first_order_functions(self):

        code = """
            (begin
                (define f
                    (fun (n)
                        (fun (x) (+ n x))
                    )
                )
                (define g (f 3))

                (+ (g 3) (g 2))
            )
        """
        self.assertEqual(Monito.run(code), 11)
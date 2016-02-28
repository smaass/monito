import unittest

from core.ast.ast import App, Number
from core.evaluation.evaluator import Evaluator
from core.evaluation.values import Primitive, Closure
from monito import Monito


class ValuesTestCase(unittest.TestCase):

    def test_fun_representations(self):

        runtime = Monito()
        env = runtime.environment
        primitive = Primitive('miau', lambda x: print(x), '(Dyn -> Void)', env)
        self.assertTrue('function miau' in primitive.__repr__())

        closure = Closure([], App([], Number(1)), env, Evaluator())
        self.assertTrue('function at' in closure.__repr__())

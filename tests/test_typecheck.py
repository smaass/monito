import unittest

from core.ast.types import *
from core.parser import Parser
from monito import Monito


class TypeCheckerTestCase(unittest.TestCase):

    def check_type(self, code_string, expected_result):

        ast = Parser.parse(code_string)
        self.assertEqual(Monito().typecheck(ast), expected_result)

    def test_typecheck(self):

        self.check_type('3', NumType())
        self.check_type('"hola"', StringType())
        self.check_type('false', BoolType())
        self.check_type('(if true "hola" "chao")', StringType())
        # self.check_type('(if (equal? 4 3) 2 3)', NumType())
        # self.check_type('(if (equal? 2 2) 1 "a")', DynamicType())
        # self.check_type('(+ 3 2)', NumType())
        # self.check_type('(* 3 (- 4 2))', NumType())
        # self.check_type('(equal? (- 5 10) -5)', BoolType())
        # self.check_type('(equal? 4 0)', BoolType())
        # self.check_type('(not false)', BoolType())
        # self.check_type('(and (> 4 3) (< -3 1))', BoolType())
        # self.check_type('(length "hola")', NumType())
        # self.check_type('(append "ho" "la")', StringType())
        #
        # self.check_type('(fun (x) x)', DynamicType())
        # self.check_type('(fun ([x: Num]) x)', NumType())
        #

import unittest

from core.ast.ast import Argument, App
from core.ast.types import *
from core.parser import Parser


class ParserTestCase(unittest.TestCase):

    def test_balanced_parens(self):

        self.assertTrue(Parser.balanced_parens('()')[0])
        self.assertFalse(Parser.balanced_parens('(')[0])
        self.assertFalse(Parser.balanced_parens(')')[0])
        self.assertTrue(Parser.balanced_parens('(a)')[0])
        self.assertTrue(Parser.balanced_parens('[][]')[0])
        self.assertTrue(Parser.balanced_parens('(a [b] (c {d}))')[0])
        self.assertTrue(Parser.balanced_parens('(ab [c e (e) {a}] [d])')[0])
        self.assertFalse(Parser.balanced_parens('(a))')[0])
        self.assertFalse(Parser.balanced_parens('([][]}')[0])
        self.assertFalse(Parser.balanced_parens('{[[]}')[0])
        self.assertFalse(Parser.balanced_parens(')ab(')[0])

    def test_string_to_sexpr(self):

        self.assertEqual(Parser.string_to_sexpr('true'), True)

        sexpr = Parser.string_to_sexpr('(and true false)')
        self.assertEqual(sexpr, ['and', True, False])

        sexpr = Parser.string_to_sexpr('(+ (- 3 2) (sum 1 2 3 4))')
        self.assertEqual(sexpr, ['+', ['-', 3, 2], ['sum', 1, 2, 3, 4]])

        sexpr = Parser.string_to_sexpr('(f (g (h 2 3 4) "hola") i)')
        self.assertEqual(sexpr, ['f', ['g', ['h', 2, 3, 4], '"hola"'], 'i'])

        sexpr = Parser.string_to_sexpr('''
            {local
                [ (a 3) (b 2) ]
                (f a b)
            }
        ''')
        self.assertEqual(sexpr, ['local', [['a', 3], ['b', 2]], ['f', 'a', 'b']])

    def test_separate_sexpr_strings(self):

        code = '''
            (define x 3)
            (define f (x) (+ x 4))
            (f x)
        '''
        sexpr_strings = Parser.separate_sexpr_strings(code)
        self.assertEqual(len(sexpr_strings), 3)
        self.assertEqual(sexpr_strings[0], '(define x 3)')
        self.assertEqual(sexpr_strings[1], '(define f (x) (+ x 4))')
        self.assertEqual(sexpr_strings[2], '(f x)')

    def to_arg(self, arg_string):

        sexpr = Parser.string_to_sexpr(arg_string)
        return Parser.parse_arg(sexpr)

    def test_parse_arg(self):

        num_arg1 = Parser.string_to_sexpr('[x : Num]')
        num_arg2 = Parser.string_to_sexpr('[x: Num]')
        self.assertEqual(num_arg1, num_arg2)

        num_arg = Parser.parse_arg(num_arg1)
        self.assertEqual(num_arg.identifier, 'x')
        self.assertEqual(num_arg.type, NumType())

        string_arg = self.to_arg('[s: Str]')
        self.assertEqual(string_arg.identifier, 's')
        self.assertEqual(string_arg.type, StringType())

        bool_arg = self.to_arg('[x: Bool]')
        self.assertEqual(bool_arg.identifier, 'x')
        self.assertEqual(bool_arg.type, BoolType())

        list_arg = self.to_arg('[l: (List Str)]')
        self.assertEqual(list_arg.identifier, 'l')
        self.assertEqual(list_arg.type, ListType(StringType()))

        dynamic_arg = self.to_arg('d')
        self.assertEqual(dynamic_arg.identifier, 'd')
        self.assertEqual(dynamic_arg.type, DynamicType())

        fun_arg = self.to_arg('[f: (Str -> Num)]')
        self.assertEqual(fun_arg.identifier, 'f')
        self.assertEqual(fun_arg.type, FunType([StringType()], NumType()))

        fun_arg = self.to_arg('[g: (Num Str -> Bool)]')
        self.assertEqual(fun_arg.identifier, 'g')
        self.assertEqual(
            fun_arg.type,
            FunType([NumType(), StringType()], BoolType())
        )

        fun_arg = self.to_arg('[h: ((Num -> Num) -> (Str -> Num))]')
        self.assertEqual(fun_arg.identifier, 'h')
        self.assertEqual(
            fun_arg.type,
            FunType(
                [FunType([NumType()], NumType())],
                FunType([StringType()], NumType())
            )
        )

    def test_parse_args(self):

        args_str = '([x: (Num -> Str)] [y: (List Num)] z)'
        args = Parser.parse_args(Parser.string_to_sexpr(args_str))

        self.assertEqual(len(args), 3)
        self.assertEqual(args[0].type, FunType([NumType()], StringType()))
        self.assertEqual(args[0].identifier, 'x')

        self.assertEqual(args[1].type, ListType(NumType()))
        self.assertEqual(args[1].identifier, 'y')

        self.assertEqual(args[2].type, DynamicType())
        self.assertEqual(args[2].identifier, 'z')

    def test_parse_function_with_types(self):

        definition = '(fun ([x: Num] [y: Num]) (+ x y))'
        fun_node = Parser.parse(definition)
        fun_args = fun_node.args

        self.assertEqual(len(fun_args), 2)
        self.assertTrue(isinstance(fun_args[0], Argument))

        self.assertEqual(fun_args[0].type, NumType())
        self.assertEqual(fun_args[0].identifier, 'x')

        self.assertEqual(fun_args[1].type, NumType())
        self.assertEqual(fun_args[1].identifier, 'y')

        self.assertTrue(isinstance(fun_node.body, App))

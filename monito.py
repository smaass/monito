from __future__ import print_function
from core.environment import Environment
from core.evaluation.evaluator import Evaluator
from core.parser import Parser
from core.type_checking.type_checker import TypeChecker


class Monito(object):

    import math
    import operator as op

    # MATH_BINDINGS = vars(math)
    OP_BINDINGS = {
        '+': (op.add, '(Num Num -> Num)'),
        '-': (op.sub, '(Num Num -> Num)'),
        '*': (op.mul, '(Num Num -> Num)'),
        '/': (lambda x, y: x / y, '(Num Num -> Num)'),
        '>': (op.gt, '(Num Num -> Bool)'),
        '<': (op.lt, '(Num Num -> Bool)'),
        '>=': (op.ge, '(Num Num -> Bool)'),
        '<=': (op.le, '(Num Num -> Bool)'),
        '=': (op.eq, '(Dyn Dyn -> Bool)'),
        'abs': (abs, '(Num -> Num)'),
        'append': (op.add, '(Dyn Dyn -> Dyn)'),
        'equal?': (op.eq, '(Dyn Dyn -> Bool)'),
        'head': (lambda x: x[0], '((List Dyn) -> Dyn)'),
        'tail': (lambda x: x[1:], '(List Dyn) -> (List Dyn))'),
        'length': (len, '((List Dyn) -> Num)'),
        'list': (lambda *x: list(x), '(Dyn -> Dyn)'), #TODO: add support for variable size arguments
        'map': (lambda f, l: list(map(f, l)), '((List Dyn) -> (List Dyn))'),
        'max': (max, '((List Num) -> Num)'),
        'min': (min, '((List Num) -> Num)'),
        'not': (op.not_, '(Bool -> Bool)'),
        'print': (print, '(Dyn -> Void)')
    }

    def __init__(self, environment=None):
        if not environment:
            environment = self.create_base_environment()
        self.environment = environment
        self.active = True

    def exit_function(self):
        def monito_exit():
            self.active = False
        return monito_exit

    def create_base_environment(self):
        env = Environment()
        # env.add_primitives(self.MATH_BINDINGS)
        env.add_primitives(self.OP_BINDINGS)
        env.add_primitives({'exit': (self.exit_function(), 'Void -> Void')})
        return env

    def eval(self, code_string):
        try:
            ast = Parser.parse(code_string)
            return self.interpret(ast)
        except Exception as e:
            name = e.__class__.__name__
            message = e.args[0]
            return '{0}: {1}'.format(name, message)

    def interpret(self, ast):
        return ast.accept(Evaluator(), self.environment)

    def typecheck(self, ast):
        return ast.accept(TypeChecker(), self.environment)

    @classmethod
    def run(cls, code_string, environment=None):
        return Monito(environment).eval(code_string)

    @classmethod
    def input(cls, prompt):
        '''
        Disgusting trick, because of python's decision of renaming raw_input
        to input in version 3
        '''
        if hasattr(__builtins__, 'raw_input'):
            return raw_input(prompt)
        else:
            return input(prompt)

    @classmethod
    def repl(cls):
        print('Welcome to the Monito REPL\n')
        runtime = Monito()
        line_breaks = 0
        code_input = ''

        while runtime.active:

            if line_breaks == 0:
                prompt = '>> '
            else:
                prompt = '\t'

            code_input += cls.input(prompt)
            balanced, fail_index = Parser.balanced_parens(code_input)
            if not balanced and fail_index == len(code_input):
                line_breaks += 1
                continue

            value = runtime.eval(code_input)
            if value is not None:
                print(value)
            line_breaks = 0
            code_input = ''


if __name__ == '__main__':
    Monito.repl()

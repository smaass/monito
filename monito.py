from core.parser import Parser
from core.evaluation import Evaluator
from core.environment import Environment

class Monito(object):

    import math, operator as op

    MATH_BINDINGS = vars(math)
    OP_BINDINGS = {
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': lambda x, y: x / y,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'equal?': op.eq,
        'head': lambda x: x[0],
        'tail': lambda x: x[1:],
        'length': len,
        'list': lambda *x: list(x),
        'map': lambda f, l: list(map(f, l)),
        'max': max,
        'min': min,
        'not': op.not_
    }

    def __init__(self, environment=None):
        if not environment:
            environment = self.create_base_environment()
        self.environment = environment

    def create_base_environment(self):
        env = Environment()
        env.add_primitives(self.MATH_BINDINGS)
        env.add_primitives(self.OP_BINDINGS)
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

    @classmethod
    def run(cls, code_string, environment=None):
        return Monito(environment).eval(code_string)

    @classmethod
    def repl(cls):
        print 'Welcome to the Monito REPL\n'
        runtime = Monito()
        line_breaks = 0
        code_input = ''

        while True:

            if line_breaks == 0:
                prompt = '>> '
            else:
                prompt = '\t'

            code_input += raw_input(prompt)
            if code_input.strip() == '(exit)':
                break

            balanced, fail_index = Parser.balanced_parens(code_input)
            if not balanced and fail_index == len(code_input):
                line_breaks += 1
                continue

            value = runtime.eval(code_input)
            if value is not None:
                print value
            line_breaks = 0
            code_input = ''


if __name__ == '__main__':
    Monito.repl()

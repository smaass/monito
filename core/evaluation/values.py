class FunVal(object):
    """
    First-order function values
    """
    def __call__(self, *args):
        return self.apply(*args)

    def apply(self, *args):
        raise NotImplementedError('Must implement apply(*args)')


class Primitive(FunVal):
    """
    Primitive function
    """
    def __init__(self, proc, env):
        self.proc = proc
        self.env = env

    def apply(self, *args):
        return self.proc(*args)

    def __repr__(self):
        return '<built-in function {0}>'.format(self.env.get_name(self))


class Closure(FunVal):
    """
    Lexical closure
    """
    def __init__(self, params, body, env, evaluator):
        self.params = params
        self.body = body
        self.env = env
        self.evaluator = evaluator

    def apply(self, *values):
        new_bindings = {
            self.params[i]: v for i, v in enumerate(values)
        }
        return self.body.accept(
            self.evaluator,
            self.env.new_environment(new_bindings)
        )

    def __repr__(self):
        name = self.env.get_name(self)

        if name is None:
            return '<anonymous function>'

        return '<function {0} at {1}>'.format(name, hex(id(self)))

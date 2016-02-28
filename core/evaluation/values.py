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
    def __init__(self, name, proc, fun_type, env):
        self.name = name
        self.proc = proc
        self.fun_type = fun_type
        self.env = env

    def apply(self, *args):
        return self.proc(*args)

    def __repr__(self):
        return '<built-in function {0}>'.format(self.name)


class Closure(FunVal):
    """
    Lexical closure
    """
    def __init__(self, args, body, env, evaluator):
        self.arg_names = [arg.identifier for arg in args]
        self.arg_types = [arg.type for arg in args]
        self.body = body
        self.env = env
        self.evaluator = evaluator

    def apply(self, *values):
        new_bindings = {
            self.arg_names[i]: v for i, v in enumerate(values)
        }
        return self.body.accept(
            self.evaluator,
            self.env.new_environment(new_bindings)
        )

    def __repr__(self):
        return '<function at {0}>'.format(hex(id(self)))

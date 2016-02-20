from core.evaluation.evaluator import Primitive


class Environment(object):
    """
    Environment (scope)
    """
    def __init__(self, bindings={}, previous=None):
        self.previous = previous
        self.bindings = bindings

    def lookup(self, var_name):
        result = self.bindings.get(var_name, None)
        if result is not None:
            return result
        if self.previous:
            return self.previous.lookup(var_name)
        raise NameError("name '{0}' is not defined".format(var_name))

    def update(self, bindings):
        self.bindings.update(bindings)
        return self

    def add_primitives(self, bindings):
        return self.update({k: Primitive(v) for k, v in bindings.items()})

    def new_environment(self, bindings={}):
        return Environment(bindings, previous=self)

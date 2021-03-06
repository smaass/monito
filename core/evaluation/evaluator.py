from core.ast.visitor import Visitor
from core.evaluation.values import *


class Evaluator(Visitor):
    """
    AST visitor for evaluation
    """

    def visit_number(self, number_node, env):
        """
        Number expression evaluation
        """
        return number_node.value

    def visit_boolean(self, boolean_node, env):
        """
        Boolean expression evaluation
        """
        return boolean_node.value

    def visit_string(self, string_node, env):
        """
        String expression evaluation
        """
        return string_node.value

    def visit_if(self, if_node, env):
        """
        'If' construct evaluation
        """
        if if_node.cond.accept(self, env):
            return if_node.if_true.accept(self, env)
        else:
            return if_node.if_false.accept(self, env)

    def visit_and(self, and_node, env):
        """
        Logical 'and' evaluation
        """
        return and_node.cond1.accept(self, env)\
               and and_node.cond2.accept(self, env)

    def visit_or(self, or_node, env):
        """
        Logical 'or' evaluation
        """
        return or_node.cond1.accept(self, env)\
               or or_node.cond2.accept(self, env)

    def visit_id(self, id_node, env):
        """
        Identifier (variable name) resolution
        """
        return env.lookup(id_node.identifier)

    def visit_fun(self, fun_node, env):
        """
        Function expression evaluation.
        Returns closure
        """
        return Closure(fun_node.args, fun_node.body, env, self)

    def visit_app(self, app_node, env):
        """
        Function application evaluation
        """
        fun_val = app_node.fun_expr.accept(self, env)
        arg_vals = [arg.accept(self, env) for arg in app_node.arg_exprs]
        return fun_val.apply(*arg_vals)

    def visit_body(self, body_node, env):
        """
        Evaluation of a sequence of expressions
        """
        for expr in body_node.expressions[0:-1]:
            expr.accept(self, env)
        return body_node.expressions[-1].accept(self, env)

    def visit_definition(self, def_node, env):
        """
        Definition evaluation.

        Mutates the environment with this definition.
        Evaluates the definition body with the same environment
        that is mutated, which allows recursion.
        Doesn't return a value.
        """
        env.update({def_node.name: def_node.expr.accept(self, env)})

    def visit_local(self, local_node, env):
        """
        Local definition evaluation
        """
        new_env = env.new_environment()
        for definition in local_node.definitions:
            definition.accept(self, new_env)
        return local_node.body.accept(self, new_env)

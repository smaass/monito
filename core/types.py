class Type(object):

    def is_consistent_with(self, another_type):
        raise NotImplementedError

    def is_consistent_with_num(self):
        return False

    def is_consistent_with_bool(self):
        return False

    def is_consistent_with_string(self):
        return False

    def is_consistent_with_list(self, inner_type):
        return False

    def is_consistent_with_fun_type(self, fun_type):
        return False


class NumType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_num()

    def is_consistent_with_num(self):
        return True


class BoolType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_bool()

    def is_consistent_with_bool(self):
        return True


class StringType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_string()

    def is_consistent_with_string(self):
        return True


class ListType(Type):

    def __init__(self, inner_type):
        self.inner_type = inner_type

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_list(self.inner_type)

    def is_consistent_with_list(self, inner_type):
        return self.inner_type.is_consistent_with(inner_type)


class FunType(Type):

    def __init__(self, arg_types, return_type):
        self.arg_types = arg_types
        self.return_type = return_type

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_fun_type(self)

    def is_consistent_with_fun_type(self, fun_type):

        if len(self.arg_types) != len(fun_type.arg_types):
            return False

        for i in range(0, len(fun_type.arg_types)):
            if not self.arg_types[i].is_consistent_with(fun_type.arg_types[i]):
                return False

        return self.return_type.is_consistent_with(fun_type.return_type)


class DynamicType(Type):

    def __init__(self, last_type=None):
        self.last_type = last_type

    def is_consistent_with(self, another_type):
        """
        Mutates this DynamicType assigning another_type
        to self.last_type after the first consistency check.
        This is used to ensure that the consistency relation is
        not transitive.
        """
        if self.last_type is not None:
            return self.last_type.is_consistent_with(another_type)
        self.last_type = another_type
        return True

    def is_consistent_with_num(self):
        return self.is_consistent_with(NumType())

    def is_consistent_with_bool(self):
        return self.is_consistent_with(BoolType())

    def is_consistent_with_string(self):
        return self.is_consistent_with(StringType())

    def is_consistent_with_list(self, inner_type):
        return self.is_consistent_with(ListType(inner_type))

    def is_consistent_with_fun_type(self, fun_type):
        return self.is_consistent_with(fun_type)

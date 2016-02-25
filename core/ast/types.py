class Type(object):

    def __eq__(self, other):
        return self.is_consistent_with(other)

    def consistency(self, other_type):
        if self.is_consistent_with(other_type):
            return self

    def is_consistent_with(self, other_type):
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

    def is_consistent_with_unit(self):
        return False


class UnitType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_unit()

    def is_consistent_with_unit(self):
        return True


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


class DynamicType(Type):

    def consistency(self, other_type):
        return other_type

    def is_consistent_with(self, another_type):
        return True

    def is_consistent_with_num(self):
        return True

    def is_consistent_with_bool(self):
        return True

    def is_consistent_with_string(self):
        return True

    def is_consistent_with_list(self, inner_type):
        return True

    def is_consistent_with_fun_type(self, fun_type):
        return True

    def is_consistent_with_unit(self):
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

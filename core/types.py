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


class NumType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_num()


class BoolType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_bool()


class StringType(Type):

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_string()


class ListType(Type):

    def list_type(self, inner_type):
        self.inner_type

    def is_consistent_with(self, another_type):
        return another_type.is_consistent_with_list(self.inner_type)

    def is_consistent_with_list(self, inner_type):
        return self.inner_type.is_consistent_with(inner_type)


class DynamicType(Type):

    def __init__(self, last_type=None):
        self.last_type = last_type

    def is_consistent_with(self, another_type):
        if self.last_type is not None:
            self.last_type.is_consistent_with(another_type)
        return True


class FunType(Type):

    def __init__(self, arg_types, return_type):
        self.arg_types = arg_types
        self.return_type = return_type

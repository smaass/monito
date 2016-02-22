import unittest

from core.ast.types import *


class TypesTestCase(unittest.TestCase):

    def test_num_consistency(self):

        self.assertTrue(NumType().is_consistent_with(NumType()))
        self.assertTrue(NumType().is_consistent_with(DynamicType()))
        self.assertFalse(NumType().is_consistent_with(BoolType()))
        self.assertFalse(NumType().is_consistent_with(StringType()))
        self.assertFalse(NumType().is_consistent_with(ListType(NumType())))
        self.assertFalse(NumType().is_consistent_with(FunType([], NumType())))

    def test_bool_consistency(self):

        self.assertTrue(BoolType().is_consistent_with(BoolType()))
        self.assertTrue(BoolType().is_consistent_with(DynamicType()))
        self.assertFalse(BoolType().is_consistent_with(NumType()))
        self.assertFalse(BoolType().is_consistent_with(StringType()))
        self.assertFalse(BoolType().is_consistent_with(ListType(BoolType())))
        self.assertFalse(BoolType().is_consistent_with(FunType([], BoolType())))

    def test_string_consistency(self):

        self.assertTrue(StringType().is_consistent_with(StringType()))
        self.assertTrue(StringType().is_consistent_with(DynamicType()))
        self.assertFalse(StringType().is_consistent_with(BoolType()))
        self.assertFalse(StringType().is_consistent_with(NumType()))
        self.assertFalse(StringType().is_consistent_with(ListType(StringType())))
        self.assertFalse(StringType().is_consistent_with(FunType([], StringType())))

    def test_list_consistency(self):

        list_of_nums = ListType(NumType())
        list_of_strings = ListType(StringType())
        list_of_dynamic = ListType(DynamicType())

        self.assertTrue(list_of_nums.is_consistent_with(ListType(NumType())))
        self.assertTrue(list_of_nums.is_consistent_with(DynamicType()))
        self.assertTrue(list_of_nums.is_consistent_with(list_of_dynamic))
        self.assertFalse(list_of_nums.is_consistent_with(list_of_strings))
        self.assertFalse(list_of_nums.is_consistent_with(NumType()))

    def test_fun_consistency(self):

        self.assertTrue(
            FunType([], StringType()).is_consistent_with(FunType([], StringType()))
        )
        self.assertFalse(
            FunType([], StringType()).is_consistent_with(FunType([], NumType()))
        )

        fun1 = FunType([BoolType(), NumType()], NumType())
        fun2 = FunType([BoolType(), NumType()], NumType())
        self.assertTrue(fun1.is_consistent_with(fun2))

        fun2 = FunType([NumType(), BoolType()], NumType())
        self.assertFalse(fun1.is_consistent_with(fun2))

        fun3 = FunType([BoolType(), NumType()], StringType())
        self.assertFalse(fun1.is_consistent_with(fun3))

        fun4 = FunType([fun1], fun3)
        fun5 = FunType([fun1], fun3)
        fun6 = FunType([fun2], fun4)
        self.assertTrue(fun4.is_consistent_with(fun5))
        self.assertFalse(fun4.is_consistent_with(fun6))

    def test_dynamic_consistency(self):

        self.assertTrue(DynamicType().is_consistent_with(NumType()))
        self.assertTrue(DynamicType().is_consistent_with(BoolType()))
        self.assertTrue(DynamicType().is_consistent_with(StringType()))
        self.assertTrue(
            DynamicType().is_consistent_with(ListType(StringType()))
        )
        self.assertTrue(
            DynamicType().is_consistent_with(FunType([], NumType()))
        )

        self.assertEqual(DynamicType().consistency(NumType()), NumType())
        self.assertEqual(NumType().consistency(DynamicType()), NumType())
        self.assertEqual(
            DynamicType().consistency(DynamicType()), DynamicType()
        )
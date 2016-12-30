# pylint: disable=missing-docstring,invalid-name,expression-not-assigned
# pylint: disable=no-member,no-self-use,too-many-public-methods

import unittest

from symbexpr import Expression


class ExpressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.var = Expression('self.var')

    # Left operators

    def test_left_add_operator(self):
        self.assertEqual((self.var + 2).__expr__, 'self.var+(2)')

    def test_left_and_operator(self):
        self.assertEqual((self.var & 2).__expr__, 'self.var&(2)')

    def test_left_eq_operator(self):
        self.assertEqual((self.var == 2).__expr__, 'self.var==(2)')

    def test_left_floordiv_operator(self):
        self.assertEqual((self.var // 2).__expr__, 'self.var//(2)')

    def test_left_ge_operator(self):
        self.assertEqual((self.var >= 2).__expr__, 'self.var>=(2)')

    def test_left_gt_operator(self):
        self.assertEqual((self.var > 2).__expr__, 'self.var>(2)')

    def test_left_le_operator(self):
        self.assertEqual((self.var <= 2).__expr__, 'self.var<=(2)')

    def test_left_lshift_operator(self):
        self.assertEqual((self.var << 2).__expr__, 'self.var<<(2)')

    def test_left_lt_operator(self):
        self.assertEqual((self.var < 2).__expr__, 'self.var<(2)')

    def test_left_matmul_operator(self):
        self.assertEqual((self.var @ 2).__expr__, 'self.var@(2)')

    def test_left_mod_operator(self):
        self.assertEqual((self.var % 2).__expr__, 'self.var%(2)')

    def test_left_mul_operator(self):
        self.assertEqual((self.var * 2).__expr__, 'self.var*(2)')

    def test_left_ne_operator(self):
        self.assertEqual((self.var != 2).__expr__, 'self.var!=(2)')

    def test_left_or_operator(self):
        self.assertEqual((self.var | 2).__expr__, 'self.var|(2)')

    def test_left_pow_operator(self):
        self.assertEqual((self.var ** 2).__expr__, 'self.var**(2)')

    def test_left_rshift_operator(self):
        self.assertEqual((self.var >> 2).__expr__, 'self.var>>(2)')

    def test_left_sub_operator(self):
        self.assertEqual((self.var - 2).__expr__, 'self.var-(2)')

    def test_left_truediv_operator(self):
        self.assertEqual((self.var / 2).__expr__, 'self.var/(2)')

    def test_left_xor_operator(self):
        self.assertEqual((self.var ^ 2).__expr__, 'self.var^(2)')

    # Right operators

    def test_right_radd_operator(self):
        self.assertEqual((2 + self.var).__expr__, '(2)+self.var')

    def test_right_rand_operator(self):
        self.assertEqual((2 & self.var).__expr__, '(2)&self.var')

    def test_rflooright_rfloordiv_operator(self):
        self.assertEqual((2 // self.var).__expr__, '(2)//self.var')

    def test_rlsright_rlshift_operator(self):
        self.assertEqual((2 << self.var).__expr__, '(2)<<self.var')

    def test_rmaright_rmatmul_operator(self):
        self.assertEqual((2 @ self.var).__expr__, '(2)@self.var')

    def test_right_rmod_operator(self):
        self.assertEqual((2 % self.var).__expr__, '(2)%self.var')

    def test_right_rmul_operator(self):
        self.assertEqual((2 * self.var).__expr__, '(2)*self.var')

    def test_right_ror_operator(self):
        self.assertEqual((2 | self.var).__expr__, '(2)|self.var')

    def test_right_rpow_operator(self):
        self.assertEqual((2 ** self.var).__expr__, '(2)**self.var')

    def test_right_rrshift_operator(self):
        self.assertEqual((2 >> self.var).__expr__, '(2)>>self.var')

    def test_right_rsub_operator(self):
        self.assertEqual((2 - self.var).__expr__, '(2)-self.var')

    def test_right_rtruediv_operator(self):
        self.assertEqual((2 / self.var).__expr__, '(2)/self.var')

    def test_right_rxor_operator(self):
        self.assertEqual((2 ^ self.var).__expr__, '(2)^self.var')

    # Unary operators

    def test_invert_unary_operator(self):
        self.assertEqual((~self.var).__expr__, '~(self.var)')

    def test_neg_unary_operator(self):
        self.assertEqual((-self.var).__expr__, '-(self.var)')

    def test_pos_unary_operator(self):
        self.assertEqual((+self.var).__expr__, '+(self.var)')

    # Built in functions

    def test_abs_built_in_function(self):
        self.assertEqual((abs(self.var)).__expr__, 'abs(self.var)')

    def test_round_built_in_function(self):
        self.assertEqual((round(self.var, 2)).__expr__, 'round(self.var, 2)')

    def test_reversed_built_in_function(self):
        # pylint: disable=bad-reversed-sequence
        self.assertEqual(reversed(self.var).__expr__, 'reversed(self.var)')

    # Attribute and item access

    def test__getattr__method(self):
        self.assertEqual(self.var.attribute.__expr__, '(self.var).attribute')
        attribute = getattr(self.var, 'attribute')
        self.assertEqual(attribute.__expr__, '(self.var).attribute')

    def test__getitem__method(self):
        self.assertEqual(self.var[1].__expr__, "(self.var)[1]")
        self.assertEqual(self.var[1, 2].__expr__, "(self.var)[(1, 2)]")
        self.assertEqual(self.var['key'].__expr__, "(self.var)['key']")

    def test__repr__method(self):
        self.assertEqual(repr(self.var), "self.var")


if __name__ == '__main__':
    unittest.main()

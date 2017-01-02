"""Python 3 functional programing experiments."""


__all__ = ["Expression"]


_LEFT_OPERATOR = {
    '__add__': '%s+(%s)',
    '__and__': '%s&(%s)',
    '__eq__': '%s==(%s)',
    '__floordiv__': '%s//(%s)',
    '__ge__': '%s>=(%s)',
    '__gt__': '%s>(%s)',
    '__le__': '%s<=(%s)',
    '__lshift__': '%s<<(%s)',
    '__lt__': '%s<(%s)',
    '__matmul__': '%s@(%s)',
    '__mod__': '%s%%(%s)',
    '__mul__': '%s*(%s)',
    '__ne__': '%s!=(%s)',
    '__or__': '%s|(%s)',
    '__pow__': '%s**(%s)',
    '__rshift__': '%s>>(%s)',
    '__sub__': '%s-(%s)',
    '__truediv__': '%s/(%s)',
    '__xor__': '%s^(%s)',
}


_RIGHT_OPERATOR = {
    '__radd__': '(%s)+%s',
    '__rand__': '(%s)&%s',
    '__rfloordiv__': '(%s)//%s',
    '__rlshift__': '(%s)<<%s',
    '__rmatmul__': '(%s)@%s',
    '__rmod__': '(%s)%%%s',
    '__rmul__': '(%s)*%s',
    '__ror__': '(%s)|%s',
    '__rpow__': '(%s)**%s',
    '__rrshift__': '(%s)>>%s',
    '__rsub__': '(%s)-%s',
    '__rtruediv__': '(%s)/%s',
    '__rxor__': '(%s)^%s',
}


_UNARY_OPERATOR = {
    '__invert__': '~(%s)',
    '__neg__': '-(%s)',
    '__pos__': '+(%s)',
}


_BUILT_IN_FUNCTIONS = {
    '__abs__': 'abs(%s%s%s)',
    '__round__': 'round(%s%s%s)',
    '__reversed__': 'reversed(%s%s%s)',
}


def _left_operator(template):
    """Return a function that make an expression
    string with a binary left operator.
    """
    def operator(self, other):
        """Store an string in the self.__expr__ attribute that
        represent a binary left operator.
        """
        if hasattr(other, "__expr__"):
            return Expression(template % (self.__expr__, other.__expr__))
        else:
            return Expression(template % (self.__expr__, repr(other)))
    return operator


def _right_operator(template):
    """Return a function that make an expression string with
    an binary operator placed at the right of the variable.
    """
    def operator(self, other):
        """Store an string in the self.__expr__ attribute that
        represent a binary righ operator.
        """
        if hasattr(other, "__expr__"):
            return Expression(template % (other.__expr__, self.__expr__))
        else:
            return Expression(template % (repr(other), self.__expr__))
    return operator


def _unary_operator(template):
    """Return a function that make an
    expression string with an unary operator.
    """
    def operator(self):
        """Store an string in the self.__expr__ attribute
        that represent a unary operator.
        """
        return Expression(template % self.__expr__)
    return operator


def _built_in_function(template, separator=', '):
    """Return a function that make an
    expression with an built in function.
    """
    def function(self, *args, **kwds):
        """Store an string in the self.__expr__ attribute
        that represent a builtin function.
        """
        formated_kwds, formated_args = "", ""
        if args != ():
            formated_args = separator + repr(args)[1:][:-2]
        if kwds != {}:
            add_equal = (f'{key}={value}' for key, value in kwds.items())
            formated_kwds = ', ' + ', '.join(add_equal)
        return Expression(
            template % (self.__expr__, formated_args, formated_kwds))
    return function


class _Operators(type):
    """All operators of the new class will
    return an instance of the Expression class.
    """
    def __new__(mcs, name, bases, namespace):
        new_namespace = {
            **namespace,
            **{function: _left_operator(template) for function, template in
               _LEFT_OPERATOR.items()},
            **{function: _right_operator(template) for function, template in
               _RIGHT_OPERATOR.items()},
            **{function: _unary_operator(template) for function, template in
               _UNARY_OPERATOR.items()},
            **{function: _built_in_function(template) for function, template in
               _BUILT_IN_FUNCTIONS.items()}
        }
        new_class = super().__new__(mcs, name, bases, new_namespace)
        return new_class


class Expression(metaclass=_Operators):
    """Create an object that store all
    math operations in which it is involved.
    """
    def __init__(self, name):
        self.__expr__ = name

    def __repr__(self):
        return self.__expr__

    def __getattr__(self, attr):
        return Expression(f'({self.__expr__}).{attr}')

    def __getitem__(self, attr):
        return Expression(f'({self.__expr__})[{attr!r}]')

    def __hash__(self):
        return hash(self.__expr__)

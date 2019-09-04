"""The culmination of experiment results."""

from decimal import Decimal
from typing import Union

import pyparsing as pp


# Real number -----------------------------------------------------------------
def to_int_or_decimal(number: str) -> Union[int, Decimal]:
    """ParseAction to convert a string into an integer or decimal."""
    return Decimal(number) if '.' in number else int(number)


real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))
real_number = pp.Combine(pp.Optional(pp.oneOf('+ -')) + (real_number_type_1 | real_number_type_2))
real_number.setParseAction(lambda toks: to_int_or_decimal(toks[0]))
# ---


# Named variable --------------------------------------------------------------
# Note: This needs a ParseAction for conversion to a numeric value.
named_variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)
# ---


# Arithmetic operator ---------------------------------------------------------
multiplicative_arithmetic_operator = pp.oneOf('^ * / mod')
multiplicative_arithmetic_operator.setParseAction(lambda toks: '%' if toks[0] == 'mod' else toks[0])
additive_arithmetic_operator = pp.oneOf('+ -')
# ---


# Arithmetic expression -------------------------------------------------------
expression = pp.Forward()
term = ((real_number | named_variable | expression)
        + pp.ZeroOrMore(multiplicative_arithmetic_operator
                        + (real_number | named_variable | expression)))
expression <<= (
        (
            '(' + term + pp.ZeroOrMore(additive_arithmetic_operator + term) + ')'
            + pp.ZeroOrMore((multiplicative_arithmetic_operator + expression) | (additive_arithmetic_operator + term))
        )
        | (term + pp.ZeroOrMore(additive_arithmetic_operator + term))
)
# ---


if __name__ == '__main__':
    real_number_tests = (
        '''
        # real number tests:
        
        42
        42.69
        0.42
        .42
        -2
        -.45
        -1.34

        # to fail:

        42..
        ..42
        42..69
        '''
    )
    real_number.runTests(real_number_tests)

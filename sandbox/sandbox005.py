"""Experiment 005

Goal: integrate [sandbox001 - sandbox004].
"""


import operator
from decimal import Decimal
from typing import Callable, Optional, Union

import pyparsing as pp


def convert_to_int_or_Decimal(number: str) -> Union[int, Decimal]:
    return Decimal(number) if '.' in number else int(number)


def check_variable(number: str):
    return number + ' <var>'


def get_arithmetic_operation(op: str) -> Optional[Callable]:
    if op == '+':
        return operator.add
    if op == '-':
        return operator.sub
    if op == '*':
        return operator.mul
    if op == '/':
        return operator.truediv
    if op == '^':
        return operator.pow
    return None


def get_conditional_operand(op: str) -> Optional[Callable]:
    if op == '>':
        return operator.gt
    if op == '<':
        return operator.lt
    if op == '>=':
        return operator.ge
    if op == '<=':
        return operator.le
    if op == '==':
        return operator.eq
    if op == '!=':
        return operator.ne
    if op == '&':
        return operator.and_
    if op == '|':
        return operator.or_
    return None


# define a variable
variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)
variable.setParseAction(lambda toks: check_variable(toks[0]))

# parse a real number
real_number = (pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
               | pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums)))
real_number.setParseAction(lambda toks: convert_to_int_or_Decimal(toks[0]))


# parse a binary arithmetic operator
binary_arithmetic_operator_in_term = pp.oneOf('^ * /')
binary_arithmetic_operator_in_term.setParseAction(lambda toks: get_arithmetic_operation(toks[0]))
binary_arithmetic_operator_not_in_term = pp.oneOf('+ -')
binary_arithmetic_operator_not_in_term.setParseAction(lambda toks: get_arithmetic_operation(toks[0]))

# parse a binary arithmetic operator
conditional_operands = pp.oneOf('> < >= <= == !=')
conditional_operands.setParseAction(lambda toks: get_conditional_operand(toks[0]))
conditional_operands_and_or = pp.oneOf('& |')
conditional_operands_and_or.setParseAction(lambda toks: get_conditional_operand(toks[0]))


class ArithmeticParser:
    # forward declare a parse rule
    expression = pp.Forward()

    # parse a term
    term = (real_number | variable | expression) + pp.ZeroOrMore(binary_arithmetic_operator_in_term + (real_number | variable | expression))

    # parse the expression
    expression <<= (('(' + term + pp.ZeroOrMore(binary_arithmetic_operator_not_in_term + term) + ')' + pp.ZeroOrMore(
        (binary_arithmetic_operator_in_term + expression) | (binary_arithmetic_operator_not_in_term + term)))
                    | (term + pp.ZeroOrMore(binary_arithmetic_operator_not_in_term + term)))

    if __name__ == '__main__':
        # real_number.runTests(
        #     '''
        #     42
        #     42.69
        #     0.42
        #     .42
        #     # failing tests:
        #     42..
        #     ..42
        #     42..69
        #     '''
        # )
        expression.runTests(
            '''
            42
            42 + 69
            ($x + 69)
            (42 + 69) + $x + 500
            (42 + 69) * 420 + 500
            (42 + 69) + (420 + 500)
            (42 + $ff) * (420 + 500)
            ((42 + 69) * 420) + 500
            42 + 69 * (420 + 500)
            '''
        )


class ConditionalParser:
    # parse a binary arithmetic operator
    conditional_operands = pp.oneOf('> < >= <= == !=')
    conditional_operands.setParseAction(lambda toks: get_conditional_operand(toks[0]))
    conditional_operands_and_or = pp.oneOf('& |')
    conditional_operands_and_or.setParseAction(lambda toks: get_conditional_operand(toks[0]))

    # forward declare a parse rule
    expression = pp.Forward()

    # parse a term
    term = (real_number | variable | expression)

    # parse the expression
    expression <<= (('(' + term + pp.ZeroOrMore(conditional_operands + term) + ')' + pp.ZeroOrMore(conditional_operands_and_or + expression))
                    | (term + conditional_operands + term + pp.ZeroOrMore(conditional_operands_and_or + expression)) | term)

    if __name__ == '__main__':
        # real_number.runTests(
        #     '''
        #     42
        #     42.69
        #     0.42
        #     .42
        #     # failing tests:
        #     42..
        #     ..42
        #     42..69
        #     '''
        # )
        expression.runTests(
            '''
            42
            42 > 69
            (42 > 69)
            42 < 69
            (42 < 69)
            42 >= 69
            (42 >= 69)
            42 <= 69
            (42 <= 69)
            42 != 69
            (42 != 69)
            (42 != 69) & ($x<3)
            ((42 != 69) & (42<3))
            42 != 69 & 42<3 | $c == 2
            '''
        )


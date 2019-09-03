"""Experiment 004

Goal: define a conditional expression parser.
"""

import operator
from decimal import Decimal
from typing import Callable, Optional, Union

import pyparsing as pp


def convert_to_int_or_Decimal(number: str) -> Union[int, Decimal]:
    return Decimal(number) if '.' in number else int(number)


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


# parse a real number
real_number = (pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
               | pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums)))
real_number.setParseAction(lambda toks: convert_to_int_or_Decimal(toks[0]))

# parse a binary arithmetic operator
conditional_operands = pp.oneOf('> < >= <= == !=')
conditional_operands.setParseAction(lambda toks: get_conditional_operand(toks[0]))
conditional_operands_and_or = pp.oneOf('& |')
conditional_operands_and_or.setParseAction(lambda toks: get_conditional_operand(toks[0]))

# forward declare a parse rule
expression = pp.Forward()

# parse a term
term = (real_number | expression)

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
        (42 != 69) & (42<3)
        ((42 != 69) & (42<3))
        42 != 69 & 42<3 | 45>2
        '''
    )

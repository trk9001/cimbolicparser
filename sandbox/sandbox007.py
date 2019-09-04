"""Experiment 007.

Goal: Evaluate arithmetic expressions.
"""

from decimal import Decimal
from typing import List, Union

import pyparsing as pp

from sandbox.sandbox000 import real_number, named_variable as variable


def iter_value():
    var_values = [0.1, 2.0, 42, 69, 420, 500]
    for val in var_values:
        yield val


val_iter = iter_value()

variable.setParseAction(lambda toks: next(val_iter))


binary_arithmetic_operator_in_term = pp.oneOf('^ * / mod')
binary_arithmetic_operator_in_term.setParseAction(lambda toks: '%' if toks[0] == 'mod' else toks[0])
binary_arithmetic_operator_not_in_term = pp.oneOf('+ -')

expression = pp.Forward()

# parse a term
term = (real_number | variable | expression) + pp.ZeroOrMore(binary_arithmetic_operator_in_term + (real_number | variable | expression))

# parse the expression
expression <<= (('(' + term + pp.ZeroOrMore(binary_arithmetic_operator_not_in_term + term) + ')' + pp.ZeroOrMore(
    (binary_arithmetic_operator_in_term + expression) | (binary_arithmetic_operator_not_in_term + term)))
                | (term + pp.ZeroOrMore(binary_arithmetic_operator_not_in_term + term)))


def evalu(toks: List) -> Union[int, Decimal]:
    s = ''.join([str(tok) for tok in toks])
    print(s)
    return eval(s)


if __name__ == '__main__':
    x = input()
    result = evalu(expression.parseString(x))
    from pprint import pprint
    pprint(result)

"""Experiment 009.

Goal: Develop a condition parser.
"""

from sandbox.sandbox000 import *


def print_toks(toks):
    from pprint import pprint
    pprint(toks.asList())
    return toks


def iter_value():
    var_values = [0.1, 2.0, 42, 69, 420, 500, 0.1, 2.0, 42, 69, 420, 500]
    for val in var_values:
        yield val


val_iter = iter_value()

named_variable.setParseAction(lambda toks: next(val_iter))

aggregate_macro.addParseAction(print_toks)


conditional_operator_equality = pp.oneOf('== !=')
conditional_operator_inequality = pp.oneOf('< > <= >=')
conditional_operator_all = conditional_operator_equality | conditional_operator_inequality

logical_combination_operator = pp.oneOf('and or')
logical_negation_operator = pp.Literal('not')

boolean_value = pp.oneOf('true false')
null = pp.Literal('null').setParseAction(lambda toks: None)

conditional_term = arithmetic_expression

condition = (
    ('(' + conditional_term + conditional_operator_equality + (boolean_value | null) + ')')
    | ('(' + conditional_term + conditional_operator_all + conditional_term + ')')
    | (conditional_term + conditional_operator_equality + (boolean_value | null))
    | (conditional_term + conditional_operator_all + conditional_term)
)

condition.runTests(
    '''
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
    42 == true
    69 != false
    $x == null
    (42 + 69 < 420)
    ((42 + 69) < 420)
    (($x + 69) < 420)
    (($x + 69) == ($y + 3 -2))
    (max($x, 34, $y+3, (3/$g)) < min(23, 45))
    
    # to fail:
    
    (($x + 69) == ($y + 3 -2)))
    true == 42
    false == null
    69 < false
    '''
)

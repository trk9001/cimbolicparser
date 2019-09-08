"""Experiment 010.

Goal: Develop a conditional expression evaluator.
"""

from sandbox.sandbox009 import *

del pp
import pyparsing as pp


def print_toks(toks):
    from pprint import pprint
    pprint(toks.asList())
    return toks


def iter_value():
    var_values = [0.1, 2.0, 42, 69, 420, 500, 0.1, 2.0, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500, 42, 69, 420, 500]
    for val in var_values:
        yield val


val_iter = iter_value()

named_variable.setParseAction(lambda toks: next(val_iter))

aggregate_macro.addParseAction(print_toks)


conditional_operator_equality = pp.oneOf('== !=')
conditional_operator_inequality = pp.oneOf('< > <= >=')
conditional_operator_all = conditional_operator_equality | conditional_operator_inequality

logical_combination_operator = pp.Keyword('and') | pp.Keyword('or')
logical_negation_operator = pp.Keyword('not')

boolean_value = pp.oneOf('true false').setParseAction(lambda toks: True if toks[0] == 'true' else False)
null = pp.Literal('null').setParseAction(lambda toks: None)

conditional_term = arithmetic_expression

condition = (
    ('(' + conditional_term + conditional_operator_equality + (boolean_value | null) + ')')
    | ('(' + conditional_term + conditional_operator_all + conditional_term + ')')
    | (conditional_term + conditional_operator_equality + (boolean_value | null))
    | (conditional_term + conditional_operator_all + conditional_term)
)

conditional_expression = pp.Forward()
conditional_expression <<= (
    ('(' + logical_negation_operator + conditional_expression + ')')
    | ('(' + condition + pp.ZeroOrMore(logical_combination_operator + conditional_expression) + ')')
    | (logical_negation_operator + conditional_expression)
    | (condition + pp.ZeroOrMore(logical_combination_operator + conditional_expression))
) + pp.ZeroOrMore(logical_combination_operator + conditional_expression)
conditional_expression.setParseAction(print_toks)

conditional_expression.runTests(
    '''
    42 > 69
    not (42 > 69)
    42 < 69
    (42 < 69)
    42 >= 69
    (42 >= 69)
    42 <= 69
    (42 <= 69)
    42 != 69
    (42 != 69)
    (42 != 69) and (42<3)
    (42 != 69) and not (42<3)
    ((42 != 69) and (42<3))
    ((42 != 69) and not (42<3))
    42 != 69 and 42<3 or 45>2
    
    # to fail:
    
    42
    '''
)

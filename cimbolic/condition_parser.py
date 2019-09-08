import pyparsing as pp

from .rule_parser import arithmetic_expression

# Quoted string grammar -------------------------------------------------------
allowed_chars_in_string = list(pp.printables)
allowed_chars_in_string.remove('"')
allowed_chars_in_string.append(' ')
quoted_string = pp.Combine('"' + pp.Word(''.join(allowed_chars_in_string)) + '"')
# ---


# Conditional operator grammar ------------------------------------------------
conditional_operator_equality = pp.oneOf('== !=')
conditional_operator_inequality = pp.oneOf('< > <= >=')
conditional_operator_all = conditional_operator_equality | conditional_operator_inequality
# ---


# Logical operator grammar ----------------------------------------------------
logical_combination_operator = pp.Keyword('and') | pp.Keyword('or')
logical_negation_operator = pp.Keyword('not')
# ---


# Boolean and null value grammar ----------------------------------------------
boolean_value = pp.oneOf('true false').setParseAction(lambda toks: True if toks[0] == 'true' else False)
null = pp.Literal('null').setParseAction(lambda toks: None)
# ---


# Conditional expression grammar ----------------------------------------------
conditional_term = arithmetic_expression

condition = (
    ('(' + conditional_term + conditional_operator_equality + (quoted_string | boolean_value | null) + ')')
    | ('(' + conditional_term + conditional_operator_all + conditional_term + ')')
    | (conditional_term + conditional_operator_equality + (quoted_string | boolean_value | null))
    | (conditional_term + conditional_operator_all + conditional_term)
)

conditional_expression = pp.Forward()
conditional_expression <<= (
    ('(' + logical_negation_operator + conditional_expression + ')')
    | ('(' + conditional_expression + ')')
    | (logical_negation_operator + conditional_expression)
    | (condition + pp.ZeroOrMore(logical_combination_operator + conditional_expression))
) + pp.ZeroOrMore(logical_combination_operator + conditional_expression)
# ---


class ConditionParser():
    pass

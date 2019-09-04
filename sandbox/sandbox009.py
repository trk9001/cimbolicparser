# conditional_operator = pp.oneOf('> < >= <= == !=')
# logical_operator = pp.oneOf('and or')
#
# conditional_expression = pp.Forward()
#
# negation_macro_name = pp.Literal('not')
# negation_macro = pp.Combine(aggregate_macro_name + pp.Suppress('(')) + conditional_expression + pp.Suppress(')')
#
# conditional_term = (real_number | named_variable | aggregate_macro | arithmetic_expression)
#
# conditional_expression <<= (('(' + conditional_term + pp.ZeroOrMore(conditional_operator + conditional_term) + ')' + pp.ZeroOrMore(logical_operator + conditional_expression))
#                 | (conditional_term + conditional_operator + conditional_term + pp.ZeroOrMore(logical_operator + conditional_expression)) | conditional_term)

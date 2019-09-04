"""Experiment 008.

Goal: Add aggregate macros to arithmetic expressions.
"""

from decimal import Decimal
from typing import List, Optional, Union

import pyparsing as pp


def evalu(toks: List) -> Union[int, Decimal]:
    s = ''.join([str(tok) for tok in toks])
    print(s)
    return eval(s)


def to_int_or_decimal(number: str) -> Union[int, Decimal]:
    return Decimal(number) if '.' in number else int(number)


real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))
real_number = pp.Combine(pp.Optional(pp.oneOf('+ -')) + (real_number_type_1 | real_number_type_2))
real_number.setParseAction(lambda toks: to_int_or_decimal(toks[0]))


def iter_value():
    var_values = [0.1, 2.0, 42, 69, 420, 500]
    for val in var_values:
        yield val


val_iter = iter_value()

named_variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)
named_variable.setParseAction(lambda toks: next(val_iter))

multiplicative_arithmetic_operator = pp.oneOf('^ * / mod')
multiplicative_arithmetic_operator.setParseAction(lambda toks: '%' if toks[0] == 'mod' else toks[0])
additive_arithmetic_operator = pp.oneOf('+ -')

arithmetic_expression = pp.Forward()

aggregate_macro_name_string = 'max min'


# def aggregate_macro_handler(toks: List) -> Optional[Union[int, Decimal]]:
#     name, args = tuple(toks)
#     print(name, args)
#     one_comma_done = True
#     last_arith_expr_index = 0
#     i = 0
#     while i < len(args):
#         if args[i] == ',':
#             if not one_comma_done:
#                 one_comma_done = True
#                 last_arith_expr_index = i + 1
#                 i += 1
#                 continue
#             else:
#                 arith_expr_toks = args[last_arith_expr_index:i]
#                 print(arith_expr_toks)
#                 arith_val = eval(''.join([str(tok) for tok in arith_expr_toks]))
#                 args = args[i+1:]
#                 args.insert(0, arith_val)
#                 one_comma_done = False
#                 last_arith_expr_index = 0
#                 i = 2
#         else:
#             i += 1
#     print(name, args)
#     for macro_name in aggregate_macro_name_string.split():
#         if name == macro_name:
#             return eval(f'{name}({str(args)})')
#     return None


def aggregate_macro_handler(toks: List) -> Optional[Union[int, Decimal]]:
    name, args = tuple(toks)
    print(name, args)
    temp = ''
    tokens = []
    for i in range(len(args)):
        if args[i] != ',':
            temp += str(args[i])
        else:
            tokens.append(eval(temp))
            temp = ''
    tokens.append(eval(temp))
    print(name, tokens)
    for macro_name in aggregate_macro_name_string.split():
        if name == macro_name:
            return eval(f'{name}({str(tokens)})')
    return None


aggregate_macro_name = pp.oneOf(aggregate_macro_name_string)
aggregate_macro = (
        pp.Combine(aggregate_macro_name + pp.Suppress('('))
        + pp.Group(arithmetic_expression + pp.ZeroOrMore(pp.Literal(',') + arithmetic_expression))
        + pp.Suppress(')')
)

aggregate_macro.setParseAction(lambda toks: aggregate_macro_handler(toks))

arithmetic_term = ((real_number | named_variable | aggregate_macro | arithmetic_expression)
        + pp.ZeroOrMore(multiplicative_arithmetic_operator
                        + (real_number | named_variable | aggregate_macro | arithmetic_expression)))

arithmetic_expression <<= (
        (
            '(' + arithmetic_term + pp.ZeroOrMore(additive_arithmetic_operator + arithmetic_term) + ')'
            + pp.ZeroOrMore((multiplicative_arithmetic_operator + arithmetic_expression) | (additive_arithmetic_operator + arithmetic_term))
        )
        | (arithmetic_term + pp.ZeroOrMore(additive_arithmetic_operator + arithmetic_term))
)


if __name__ == '__main__':
    tests = [
        ('42', 42),
        ('42 + 69', 111),
        ('(42 + 69)', 111),
        ('(42 + 69) + 420 + 500', 1031),
        ('(42 + 69) * 420 + 500', 47120),
        ('(42 + 69) + (420 + 500)', 1031),
        ('(42 + 69) * (420 + 500)', 102120),
        ('((42 + 69) * 420) + 500', 47120),
        ('42 + 69 * (420 + 500)', 63522),
        ('4 mod 4', 0),
        ('(4 + 5) mod 4 mod 4', 1),
        ('(4 + 5) mod 4 mod min(1,2,$x, $x+1, $y * $z)', 0.09999999999999995),
    ]
    for test in tests:
        result = evalu(arithmetic_expression.parseString(test[0]))
        # from pprint import pprint
        # pprint(result)
        # print()
        if result == test[1]:
            print('SUCCESS')
        else:
            print('FAIL')


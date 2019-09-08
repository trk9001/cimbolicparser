"""The culmination of experiment results."""

from decimal import Decimal
from typing import Iterable, Union

import pyparsing as pp


def evaluator(tokens: Union[str, Iterable]) -> Union[int, Decimal]:
    """Evaluate a string or a ParseResult containing a reduced expression."""
    if not isinstance(tokens, str):
        tokens = ' '.join([str(tok) for tok in tokens])
    result = eval(tokens)
    return result


# Real number grammar ---------------------------------------------------------
real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))
real_number = pp.Combine(pp.Optional(pp.oneOf('+ -')) + (real_number_type_1 | real_number_type_2))
real_number.setParseAction(lambda toks: Decimal(toks[0]) if '.' in toks[0] else int(toks[0]))
# ---


# Named variable grammar ------------------------------------------------------
# TODO: Add a ParseAction for conversion to a numerical value
named_variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)
# ---


# Arithmetic operator grammar -------------------------------------------------
multiplicative_arithmetic_operator = pp.oneOf('^ * / %')
additive_arithmetic_operator = pp.oneOf('+ -')
# ---


# Arithmetic expression grammar (forward-declared) ----------------------------
arithmetic_expression = pp.Forward()
# ---


# Aggregate macro grammar -----------------------------------------------------
aggregate_macro_names_allowed = 'max min'


def aggregate_macro_evaluator(toks: Iterable) -> Union[int, Decimal]:
    """Recursively evaluate the arguments to an aggregate macro."""
    macro_name, macro_args = tuple(toks)
    sub_expression = ''
    parsed_args = []
    for arg in macro_args:
        if arg != ',':
            sub_expression += str(arg)
        else:
            parsed_args.append(evaluator(sub_expression))
            sub_expression = ''
    parsed_args.append(evaluator(sub_expression))
    result = evaluator(f'{macro_name}({str(parsed_args)})')
    return result


aggregate_macro_name = pp.oneOf(aggregate_macro_names_allowed)
aggregate_macro = (
    pp.Combine(aggregate_macro_name + pp.Suppress('('))
    + pp.Group(arithmetic_expression + pp.ZeroOrMore(pp.Literal(',') + arithmetic_expression))
    + pp.Suppress(')')
)
aggregate_macro.setParseAction(lambda toks: aggregate_macro_evaluator(toks))
# ---


# Arithmetic term grammar -----------------------------------------------------
arithmetic_term = (
    (real_number | named_variable | aggregate_macro | arithmetic_expression)
    + pp.ZeroOrMore(
        multiplicative_arithmetic_operator
        + (real_number
           | named_variable
           | aggregate_macro
           | arithmetic_expression)
    )
)
# ---


# Arithmetic expression grammar -------------------------------------------------------
# TODO: Add rigorous testing
arithmetic_expression <<= (
    (
        '(' + arithmetic_term + pp.ZeroOrMore(additive_arithmetic_operator + arithmetic_term) + ')'
        + pp.ZeroOrMore(
            (multiplicative_arithmetic_operator + arithmetic_expression)
            | (additive_arithmetic_operator + arithmetic_term)
        )
    )
    | (arithmetic_term + pp.ZeroOrMore(additive_arithmetic_operator + arithmetic_term))
)
# ---

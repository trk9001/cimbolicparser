from decimal import Decimal
from typing import Union

import pyparsing as pp

from ..exceptions import VariableNotFoundError
from .utils import evaluator


# Real number grammar ---------------------------------------------------------
real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))
real_number = pp.Combine(pp.Optional(pp.oneOf('+ -')) + (real_number_type_1 | real_number_type_2))
real_number.setParseAction(lambda toks: Decimal(toks[0]) if '.' in toks[0] else int(toks[0]))
# ---


# Named variable grammar ------------------------------------------------------
def to_value(toks: pp.ParseResults) -> Union[int, Decimal]:
    """Fetch the variable from the database and return its value."""
    from django.apps import apps
    Variable = apps.get_model('cimbolic', 'Variable')
    var_name = toks[0]
    try:
        var = Variable.objects.get(name=var_name)
    except Variable.DoesNotExist:
        raise VariableNotFoundError(f'Variable {var_name} not found in the database')
    else:
        return var.to_value()


named_variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)
named_variable.setParseAction(to_value)
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


def aggregate_macro_evaluator(toks: pp.ParseResults) -> Union[int, Decimal]:
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
aggregate_macro.setParseAction(aggregate_macro_evaluator)
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


def evaluate_rule(rule: str) -> Union[int, Decimal]:
    """Parse the input string and return a corresponding value."""
    result = evaluator(arithmetic_expression.parseString(rule))
    return result

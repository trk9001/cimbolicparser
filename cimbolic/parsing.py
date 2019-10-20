"""The core parsing functionality of Cimbolic.

The public API consists of two classes, Condition and Rule, that do the
parsing, evaluation and any required context passing (for pre-defined
system variables, for example). Note that this module has two external
dependencies. (1) PyParsing is used to define the grammar (tokenization).
(2) Variable values are sourced from a Django model.

The code in this module aims to be maintainable by making extensive use of
type hints, comments and docstrings. The code also aims to conform to PEP8,
but fails. :)
"""

# So that one may import * from this module.
__all__ = ['Condition', 'Rule']

from decimal import Decimal
from typing import Any, Callable, Dict, Optional, Union

import pyparsing as pp


# The following are custom type hints used in this module.
# --------------------------------------------------------


Numeric = Union[int, Decimal]
StrMapping = Dict[str, Any]
Tokens = pp.ParseResults


# The following are common functions used in this module.
# -------------------------------------------------------


def evaluator(tokens: Union[str, Tokens]) -> Union[bool, Numeric]:
    """Evaluate a string or a ParseResult containing a reduced expression."""
    if not isinstance(tokens, str):
        tokens = ' '.join([str(tok) for tok in tokens])
    result = eval(tokens)
    return result


def print_tokens(tokens: Tokens) -> Tokens:
    """Callable ParseAction to print tokens for debugging purposes."""
    from pprint import pprint
    pprint(tokens.asList())
    return tokens


# The following tokens belong to a Rule.
# --------------------------------------


# Real number grammar ---------------------------------------------------------
real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))
real_number = pp.Combine(pp.Optional(pp.oneOf('+ -')) + (real_number_type_1 | real_number_type_2))
real_number.setParseAction(lambda toks: Decimal(toks[0]) if '.' in toks[0] else int(toks[0]))
# ---

# Named variable grammar ------------------------------------------------------
# TODO: After test coverage, rewrite to use the other args in pp.Word.__init__.
named_variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
    + pp.WordEnd()
)
# See the ContextMixin class for a ParseAction to set dynamically.
# ---

# Arithmetic operator grammar -------------------------------------------------
multiplicative_arithmetic_operator = pp.oneOf('^ * / %')
additive_arithmetic_operator = pp.oneOf('+ -')
# ---

# Arithmetic expression grammar (forward-declared) ----------------------------
arithmetic_expression = pp.Forward()
# ---

# Aggregate macro grammar -----------------------------------------------------
aggregate_macro_name = pp.oneOf('max min', caseless=True)
aggregate_macro = (
    pp.Combine(aggregate_macro_name + pp.Suppress('('))
    + pp.Group(arithmetic_expression + pp.ZeroOrMore(pp.Literal(',') + arithmetic_expression))
    + pp.Suppress(')')
)


def aggregate_macro_evaluator(toks: Tokens) -> Numeric:
    """Recursively evaluate the arguments to an aggregate macro.

    Note: Named variables are already parsed before entering this function.
    """
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


aggregate_macro.setParseAction(aggregate_macro_evaluator)
# ---

# Arithmetic term grammar -----------------------------------------------------
arithmetic_term = (
    (real_number | named_variable | aggregate_macro | arithmetic_expression)
    + pp.ZeroOrMore(
        multiplicative_arithmetic_operator
        + (
            real_number
            | named_variable
            | aggregate_macro
            | arithmetic_expression
        )
    )
)
# ---

# Arithmetic expression grammar -----------------------------------------------
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


# The following tokens belong to a Condition.
# -------------------------------------------


# Quoted string grammar -------------------------------------------------------
# TODO: After test coverage, rewrite to use the excludeChars arg.
#   See: https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html#word
allowed_chars_in_string = list(pp.printables)
allowed_chars_in_string.remove('"')
allowed_chars_in_string.append(' ')
quoted_string = pp.Combine('"' + pp.Optional(pp.Word(''.join(allowed_chars_in_string))) + '"')
# ---

# Conditional operator grammar ------------------------------------------------
conditional_operator_equality = pp.oneOf('== !=')
conditional_operator_inequality = pp.oneOf('< > <= >=')
conditional_operator_all = conditional_operator_equality | conditional_operator_inequality
# ---

# Logical operator grammar ----------------------------------------------------
logical_combination_operator = pp.CaselessKeyword('and') | pp.CaselessKeyword('or')
logical_negation_operator = pp.CaselessKeyword('not')
# ---

# Boolean and null value grammar ----------------------------------------------
boolean_value = (
    pp.oneOf('true false', caseless=True)
    .setParseAction(lambda toks: True if toks[0].upper() == 'TRUE' else False)
)
null = pp.CaselessLiteral('null').setParseAction(lambda toks: None)
# ---

# Conditional expression grammar ----------------------------------------------
conditional_term = arithmetic_expression.copy()

simple_condition = (
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
    | (simple_condition + pp.ZeroOrMore(logical_combination_operator + conditional_expression))
) + pp.ZeroOrMore(logical_combination_operator + conditional_expression)
# ---


# The following mixin class is used to set the context where needed.
# ------------------------------------------------------------------


class ContextMixin:
    """Mixin to set ParseActions for elements that need a dynamic context."""
    def __init__(self, context: Optional[StrMapping] = None):
        self.context: StrMapping = context or {}

    def get_named_variable_parse_action(self) -> Callable[[Tokens], Numeric]:
        """Return a ParseAction callable for a named_variable token."""
        def to_value(toks: Tokens) -> Numeric:
            """Fetch the variable from the database and return its value."""
            var_name: str = toks[0]
            from cimbolic.models import Variable
            try:
                var = Variable.objects.get(name=var_name)
            except Variable.DoesNotExist:
                raise LookupError(f'Variable {var_name} not found in the database')
            else:
                value = var.to_value(self.context)
                return value
        return to_value


# The following classes are the API to Cimbolic's parsing functionality.
# ----------------------------------------------------------------------


class Condition(ContextMixin):
    """Encapsulation of a condition object."""
    def __init__(self, condition: str, context: Optional[StrMapping] = None):
        super().__init__(context)
        self.condition: str = condition

    def evaluate(self) -> bool:
        """Parse self.condition and return a corresponding boolean value."""
        if self.condition.strip().upper() == 'NULL':
            return True
        else:
            named_variable.setParseAction(self.get_named_variable_parse_action())
            parse_results = conditional_expression.parseString(self.condition)
            named_variable.setParseAction(None)
            result: bool = evaluator(parse_results)
            return result


class Rule(ContextMixin):
    """Encapsulation of an arithmetic rule object."""
    def __init__(self, rule: str, context: Optional[StrMapping] = None):
        super().__init__(context)
        self.rule: str = rule

    def evaluate(self) -> Numeric:
        """Parse self.rule and return a corresponding value."""
        named_variable.setParseAction(self.get_named_variable_parse_action())
        parse_results = arithmetic_expression.parseString(self.rule)
        named_variable.setParseAction(None)
        result: Numeric = evaluator(parse_results)
        return result

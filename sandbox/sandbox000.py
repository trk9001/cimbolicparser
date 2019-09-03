"""The culmination of experiment results."""

from decimal import Decimal
from typing import Callable, Optional, Union

import pyparsing as pp


# Real number -----------------------------------------------------------------
def to_int_or_decimal(number: str) -> Union[int, Decimal]:
    """ParseAction to convert a string into an integer or decimal."""
    return Decimal(number) if '.' in number else int(number)


real_number_type_1 = pp.Combine(pp.Word(pp.nums) + pp.Optional('.' + pp.Word(pp.nums)))  # 1, 1.23
real_number_type_2 = pp.Combine(pp.Optional(pp.Word(pp.nums)) + '.' + pp.Word(pp.nums))  # .1, 2.1
real_number = real_number_type_1 | real_number_type_2
real_number.setParseAction(lambda toks: to_int_or_decimal(toks[0]))
# ---

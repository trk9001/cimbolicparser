from decimal import Decimal
from typing import Union

from pyparsing import ParseResults


def evaluator(tokens: Union[str, ParseResults]) -> Union[bool, int, Decimal]:
    """Evaluate a string or a ParseResult containing a reduced expression."""
    if not isinstance(tokens, str):
        tokens = ' '.join([str(tok) for tok in tokens])
    result = eval(tokens)
    return result


def print_tokens(tokens: ParseResults) -> ParseResults:
    """Callable ParseAction to print tokens for debugging purposes."""
    from pprint import pprint
    pprint(tokens.asList())
    return tokens

from decimal import Decimal
from typing import Iterable, Union


def evaluator(tokens: Union[str, Iterable]) -> Union[bool, int, Decimal]:
    """Evaluate a string or a ParseResult containing a reduced expression."""
    if not isinstance(tokens, str):
        tokens = ' '.join([str(tok) for tok in tokens])
    result = eval(tokens)
    return result


def print_tokens(tokens):
    """Callable ParseAction to print tokens for debugging purposes."""
    from pprint import pprint
    pprint(tokens.asList())
    return tokens

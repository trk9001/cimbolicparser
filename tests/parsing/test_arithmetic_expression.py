from decimal import Decimal
from typing import Any

import pyparsing as pp
import pytest

from cimbolic import parsing


def parse(parser_element: pp.ParserElement, string_to_parse: str) -> Any:
    """Helper function to parse a string using the given ParserElement."""
    parse_results: pp.ParseResults = parser_element.parseString(string_to_parse)
    return parse_results[0]


def test_real_number():
    real_number: pp.ParserElement = parsing._real_number
    test_cases = {
        '0': 0,
        '1': 1,
        '10': 10,
        '0.0': Decimal('0.0'),
        '0.1': Decimal('0.1'),
        '1.0': Decimal('1.0'),
        '.0': Decimal('0.0'),
        '.1': Decimal('0.1'),
        '.10': Decimal('0.10'),
        '-0': 0,
        '-1': -1,
        '-10': -10,
        '-0.0': Decimal('0.0'),
        '-0.1': Decimal('-0.1'),
        '-1.0': Decimal('-1.0'),
        '-.0': Decimal('0.0'),
        '-.1': Decimal('-0.1'),
        '-.10': Decimal('-0.10'),
    }
    for test in test_cases:
        assert parse(real_number, test) == test_cases[test]



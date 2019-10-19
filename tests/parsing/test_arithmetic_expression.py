from decimal import Decimal

import pyparsing as pp
import pytest

from .util import parse
from cimbolic import parsing


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


def test_named_variable_without_parse_action():
    named_variable = parsing._named_variable
    test_cases = {
        '$FOO': 'FOO',
        '$foo': 'foo',
        '$Foo': 'Foo',
        '$_fOO': '_fOO',
        '$FoO123': 'FoO123',
        '$_foo_bar': '_foo_bar',
        '$_foo_1_2_3_': '_foo_1_2_3_',
        '$__foo__': '__foo__',
        '$X': 'X',
        '$_': '_',
    }
    for test in test_cases:
        assert parse(named_variable, test) == test_cases[test]
    erroneous_cases = [
        'FOO',
        '$$FOO',
        '$1FOO',
        '$FOO$',
        '$FOO@',
        '$FOO+',
    ]
    for test in erroneous_cases:
        with pytest.raises(pp.ParseException):
            parse(named_variable, test)

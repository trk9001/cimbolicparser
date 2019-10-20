from decimal import Decimal

from .util import ParsingElementTester
from cimbolic import parsing


def test_real_number():
    tester = ParsingElementTester('real_number', parsing.real_number)
    tester.legal_test_cases = {
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
    tester.illegal_test_cases = [
        'F',
        '0F',
        'F0',
        '.',
        '0..1',
        '.1.',
        '..1',
    ]
    tester.test_all()


def test_named_variable_without_parse_action():
    tester = ParsingElementTester('named_variable', parsing.named_variable)
    tester.legal_test_cases = {
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
    tester.illegal_test_cases = [
        'FOO',
        '$$FOO',
        '$1FOO',
        '$FOO$',
        '$FOO@',
        '$FOO+',
        '$1',
    ]
    tester.test_all()

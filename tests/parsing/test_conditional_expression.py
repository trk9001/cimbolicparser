import pyparsing as pp

from .util import parse
from cimbolic import parsing


def test_quoted_string():
    quoted_string: pp.ParserElement = parsing._quoted_string
    test_cases = {
        '""': '""',
        '"hello"': '"hello"',
        '"hello world"': '"hello world"',
        '"\'"': '"\'"',
    }
    for test in test_cases:
        assert parse(quoted_string, test) == test_cases[test]
    # TODO: Add erroneous test cases for this and other parsing tests.

# TODO: Since the parsing tests are following a similar pattern, perhaps
#   they can be rewritten to use a class-based approach.

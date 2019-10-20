from .util import ParsingElementTester
from cimbolic import parsing


def test_quoted_string():
    tester = ParsingElementTester(
        'quoted_string',
        parsing.quoted_string,
    )
    tester.legal_test_cases = {
        '""': '""',
        '"hello"': '"hello"',
        '"hello world"': '"hello world"',
        '"\'"': '"\'"',
    }
    tester.test_legal()
    # TODO: Add erroneous test cases for this and other parsing tests.

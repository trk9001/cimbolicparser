from .util import ParsingElementTester
from cimbolic import parsing


class TestQuotedString:
    """Test suite to test parsing by `cimbolic.parsing.quoted_string`."""
    tester = ParsingElementTester('quoted_string', parsing.quoted_string)

    def test_legal_cases(self):
        test_cases = {
            '""': '""',
            '"hello"': '"hello"',
            '"hello world"': '"hello world"',
            '"\'"': '"\'"',
        }
        self.tester.legal_test_cases = test_cases
        self.tester.test_legal()

    # TODO: Add illegal test cases for this and other parsing tests.

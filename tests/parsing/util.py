from typing import Any, Dict, List

import pyparsing as pp
import pytest


class ParsingElementTester:
    """Encapsulation of test properties of a `cimbolic.parsing` element."""
    def __init__(self, identifier: str, element: pp.ParserElement):
        self.element = element
        self.identifier = identifier
        self.legal_test_cases: Dict[str, Any] = {}  # tests with legal inputs
        self.illegal_test_cases: List[str] = []  # tests with illegal inputs

    def __str__(self):
        return f'{self.__class__.__name__}({self.identifier})'

    def test_legal(self):
        """Check that the element correctly parses legal inputs."""
        for test in self.legal_test_cases:
            print(f'{self} > test_legal > test: {repr(test)}')
            parse_results: pp.ParseResults = self.element.parseString(test)
            assert parse_results[0] == self.legal_test_cases[test]

    def test_illegal(self):
        """Check that the element raises exceptions for illegal inputs."""
        for test in self.illegal_test_cases:
            print(f'{self} > test_illegal > test: {repr(test)}')
            with pytest.raises(pp.ParseException):
                self.element.parseString(test)

    def test_all(self):
        """Run all the test methods."""
        self.test_legal()
        self.test_illegal()

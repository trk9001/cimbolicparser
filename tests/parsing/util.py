from typing import Any

import pyparsing as pp


def parse(parser_element: pp.ParserElement, string_to_parse: str) -> Any:
    """Helper function to parse a string using the given ParserElement."""
    parse_results: pp.ParseResults = parser_element.parseString(string_to_parse)
    return parse_results[0]

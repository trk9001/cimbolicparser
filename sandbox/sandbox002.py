"""Experiment 002.

Goal: parse an expression of the form `42 + 69 + ...`.
Additional: also maybe evaluate it.
"""

import operator

import pyparsing as pp


def operation(op):
    if op == '+':
        return operator.add
    if op == '-':
        return operator.sub
    return None


# define an integer
integer = pp.Word(pp.nums).setParseAction(lambda toks: int(toks[0]))


# define an addition operator
operator_ = (pp.Literal('+') | pp.Literal('-')).setParseAction(lambda toks: operation(toks[0]))

# define the expression
expr = integer + pp.ZeroOrMore(operator_ + integer)

if __name__ == '__main__':
    expr.runTests(
        '''
        42
        42 + 69
        42 + 69 + 420
        42 + 42 - 0 - 69 + 500
        # Next one should fail
        42 + 42 - 0 - 69 + 500 +
        '''
    )

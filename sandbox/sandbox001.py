"""Experiment 001.

Goal 1: parse an expression of the form `$VAR = 42 + 69`.
Goal 2: parse an expression of the form `$VAR = (42 + 69)`.
Additional: also maybe evaluate it.

Notes:
    - variables start with a '$'
    - the expression is denoted by `expr` in the code
"""

import operator as pyop

import pyparsing as pp


def operation(op):
    if op == '+':
        return pyop.add
    if op == '-':
        return pyop.sub
    return None


# define a variable
variable = pp.Combine(
    pp.Suppress('$')
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)

# define an integer
integer = pp.Word(pp.nums).setParseAction(lambda toks: int(toks[0]))

# define an addition operator
operator = (pp.Literal('+') | pp.Literal('-')).setParseAction(lambda toks: operation(toks[0]))

# define the expression
expr = variable('var') + '=' + pp.Optional(pp.Literal('(')) + integer('int1') + operator('op') + integer('int2') + pp.Optional(pp.Literal(')'))

if __name__ == '__main__':
    expr.runTests(
        '''
        $x = 42 + 69
        $y = (420 + 786)
        '''
    )

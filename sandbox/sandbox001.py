"""Experiment 001.

Goal: parse an expression of the form `$VAR = 42 + 69`.
Additional: also maybe evaluate it.

Notes:
    - variables start with a '$'
    - the expression is denoted by `expr` in the code
"""

import pyparsing as pp

# define a variable
variable = pp.Combine(
    pp.Word('$', exact=1)
    + pp.Word(pp.alphas + '_', exact=1)
    + pp.Optional(pp.Word(pp.alphanums + '_'))
)

# define an integer
integer = pp.Word(pp.nums)

# define an addition operator
operator = pp.Literal('+') | pp.Literal('-')

# define the expression
expr = variable + '=' + integer + operator + integer

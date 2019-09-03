"""Experiment 006.

Goal: define a parser for aggregate system macros.
"""

import pyparsing as pp

from sandbox.sandbox005 import ArithmeticParser

expr = ArithmeticParser.expression

macro_name = pp.oneOf('max min')
macro = pp.Combine(macro_name + pp.Suppress('(')) + expr + pp.ZeroOrMore(pp.Suppress(',') + expr) + pp.Suppress(')')

macro.runTests(
    '''
    max(2, 4, $x)
    min(2, 4, $x)
    max(2,4,$x)
    max(2)
    max((2+4), 3)
    max(2 + 4, ($x +3), 8)
    
    # to fail:
    
    max (1, 2, 3)
    max(2 + 4, ($x +3), 8
    max(1 2 3)
    max()
    '''
)

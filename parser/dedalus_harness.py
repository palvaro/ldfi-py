import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from pprint import pprint
import unittest
from dedalus import DedalusSemantics, TrivialSemantics
import sys


grammar = open('dedalus.tatsu').read()
parser = tatsu.compile(grammar)


with open(sys.argv[1], 'r') as prog:
    ast = parser.parse(prog.read(), trace=False, colorize=True, semantics=DedalusSemantics())
    print ast
    



import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from pprint import pprint
import unittest
from dedalus_parser import DedalusParser
import sys
import os


grammar = open('dedalus_asmodel.tatsu').read()
parser = tatsu.compile(grammar, asmodel = True)


dp = DedalusParser()
prog = dp.expand_file(sys.argv[1])

print "POGO " + prog
w = dp.parse(prog)
pfx = os.path.basename(sys.argv[1])
w.to_dot().render(pfx + "_dataflow")


    



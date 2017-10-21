import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from pprint import pprint
import unittest
from dedalus import TrivialSemantics, DedalusSemantics


class GrammarTest(unittest.TestCase):

    def setUp(self):
        self.grammar = open('dedalus.tatsu').read()
        self.parser = tatsu.compile(self.grammar)


    def test_simple(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def test_simple2(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload), frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)


    # this test is failing
    def test_simple3(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload), notin frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)


    def test_simple4(self):
        prog = 'log(Node, Pload + 1)@next :- log(Node, Pload), frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def test_simple5(self):
        prog = "a(X, Y) :- b(X, Z), c(Z, Y), d(Y, W);"
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)
    
    def test_assign(self):
        prog = "a(X, Y, A) :- b(X, Z), c(Z, Y), d(Y, W), A = Y / Z;"
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)
    
    def test_2pc(self):
        prog = """include "./2pc_edb.ded";
prepare(Agent, Coord, Xact)@async :- running(Coord, Xact), agent(Coord, Agent);"""
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)


    def Ntest_dedalus1(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=DedalusSemantics())
        print "AST " + str(ast)

    def test_fact(self):
        prog = 'bcast("a", 1)@1;';
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def test_qual(self):
        prog = 'a(X, Y) :- b(X, Y), Y != X;';
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

if __name__ == '__main__':
    unittest.main()

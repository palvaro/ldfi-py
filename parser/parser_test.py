import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from tatsu.model import ModelBuilderSemantics
from pprint import pprint
import unittest
from dedalus import TrivialSemantics, DedalusSemantics
from codegen import C4CodeGenerator

from dedalus_parser import NegNodeWalker


class GrammarTest(unittest.TestCase):

    def setUp(self):
        self.grammar = open('dedalus.tatsu').read()
        self.parser = tatsu.compile(self.grammar)

        self.grammar_asmodel = open('dedalus_asmodel.tatsu').read()
        self.parser_asmodel = tatsu.compile(self.grammar_asmodel, asmodel=True)


    def Ntest_simple(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def Ntest_simple2(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload), frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def Ntest_simple3(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload), notin frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)


    def Ntest_simple4(self):
        prog = 'log(Node, Pload + 1)@next :- log(Node, Pload), frog(Node);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def Ntest_simple5(self):
        prog = "a(X, Y) :- b(X, Z), c(Z, Y), d(Y, W);"
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)
    
    def Ntest_assign(self):
        prog = "a(X, Y, A) :- b(X, Z), c(Z, Y), d(Y, W), A = Y / Z;"
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)
    
    def Ntest_2pc(self):
        prog = """include "./2pc_edb.ded";
prepare(Agent, Coord, Xact)@async :- running(Coord, Xact), agent(Coord, Agent);"""
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)


    def Ntest_dedalus1(self):
        prog = 'log(Node, Pload)@next :- log(Node, Pload);'
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=DedalusSemantics())
        print "AST " + str(ast)

    def Ntest_fact(self):
        prog = 'bcast("a", 1)@1;';
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

    def test_negation(self):
        print "TEST NEGATION"
        #prog = 'log(Node, Pload)@next :- log(Node, Pload), notin frog(Node); frog(Node)@next :- bob(Node);'
        prog = 'log(Node, Pload)@next :- log(Node, Pload), notin frog(Node); frog(Node) :- bob(Node);'
        model = self.parser_asmodel.parse(prog)
        walker = NegNodeWalker()
        w = walker.walk(model)
        #print "walked " + str(model)
        print "walked2 " + str(w)

        

        #w.to_dot().render("FOO")
        text = C4CodeGenerator().render(model)

        print "TEXT " + text

    def Ntest_qual(self):
        prog = 'a(X, Y) :- b(X, Y), Y != X;';
        ast = self.parser.parse(prog, trace=False, colorize=True, semantics=TrivialSemantics())
        self.assertEqual(str(ast), prog)

if __name__ == '__main__':
    unittest.main()

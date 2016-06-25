import unittest2
import pbool
import psat
import pilp
from pytest import *

class MyTest(unittest2.TestCase):
    
    def basic(self):
        return pbool.OrFormula(pbool.AndFormula(pbool.Literal("a"), pbool.Literal("b")), pbool.AndFormula(pbool.Literal("c"), pbool.Literal("d")))

   

    def test_size(self):
        fg = pbool.FormulaGenerator(10, 8)
        fst = fg.formula(10)
        snd = fg.formula(20)

        #nprint "snd " + str(len(snd.variables()))
        assert(snd.clauses() > fst.clauses())

        assert(snd.depth() == 20)
        assert(fst.depth() == 10)
        assert(len(snd.variables()) == 11)

    def test_simpleConvert(self):
        base = self.basic()
        #pbool.OrFormula(pbool.AndFormula(pbool.Literal("a"), pbool.Literal("b")), pbool.AndFormula(pbool.Literal("c"), pbool.Literal("d")))        
        cnf = pbool.CNFFormula(base)
        print str(cnf.formula)
        assert(cnf.formula.isCNF())
        

    def test_convert(self):
        fg = pbool.FormulaGenerator(10, 8)
        fst = fg.formula(7)
        c = pbool.CNFFormula(fst)
        cnf = c.formula
        assert(cnf.variables() == fst.variables())
        #assert(cnf.clauses() > fst.clauses())
        #assert(cnf.depth() > fst.depth())

        assert(not fst.isCNF())
        assert(cnf.isCNF())
        c = cnf.conjuncts()

    def test_solve(self):
        fg = pbool.FormulaGenerator(50, 8)
        fst = fg.formula(4)
        s = psat.Solver(fst)
        for soln in  s.minimal_solutions():
            print "SOLN " + str(soln)

    def test_basic_solve(self):
        base = self.basic()
        cnf = pbool.CNFFormula(base)
        s = psat.Solver(cnf)
        for soln in s.minimal_solutions():
            print "SOLN " + str(soln)


    def test_basic_ilp(self):
        base = self.basic()
        cnf = pbool.CNFFormula(base)
        s = pilp.Solver(cnf)
    
        for soln in s.solutions():
            print "SOL: "  + str(soln)

    def Ntest_big_ilp(self):
        fg = pbool.FormulaGenerator(100, 8)
        fst = fg.formula(8)
        cnf = pbool.CNFFormula(fst)
        s = pilp.Solver(cnf)
        

        for soln in s.solutions():
            print "SOL: "  + str(soln)

    def test_ilp_sat_equivalence(self):
        fg = pbool.FormulaGenerator(20, 8)
        fst = fg.formula(4)

        #print "FORMO: " + str(fst)

        cnf = pbool.CNFFormula(fst)

        s = psat.Solver(cnf)
        i = pilp.Solver(cnf)

        ssols = sorted(list(s.solutions()))
        isols = sorted(list(i.solutions()))

        print "LENs " + str(len(ssols)) + " vs " + str(len(isols))
        print "SOLs " + str(ssols) + " vs " + str(isols)

        #assert(ssols == isols)


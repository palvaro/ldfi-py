import pbool
import pilp
import psat
from datetime import datetime
from timeit import timeit
from timeout import timeout_timeit
import sys

import pdb

vocab = 100
seed = 177


def do_experiment(fg, i, j):
    formula = fg.formula(i)
    ctm = timeout_timeit(lambda: pbool.CNFFormula(formula), number=1, timeo=15)

    if ctm == -1:
        return;
    cnf = pbool.CNFFormula(formula)

    
    ssolv = psat.Solver(cnf)
    isolv = pilp.Solver(cnf)

    ssolv2 = psat.Solver(cnf)
    isolv2 = pilp.Solver(cnf)


    ssolv3 = psat.Solver(cnf)
    isolv3 = pilp.Solver(cnf)



    imtm = timeout_timeit(lambda: next(isolv.solutions()), number=1)
    smtm = timeout_timeit(lambda: next(ssolv.minimal_solutions()), number=1)
    sftm = timeout_timeit(lambda: next(ssolv2.solutions()), number=1)
    #iftm = timeout_timeit(lambda: next(isolv2.solutions()), number=1)

    ssiz = len(next(ssolv3.solutions()))
    isiz = len(next(isolv3.solutions()))

    if smtm == -1:
        solns = -1
    else: 
        solns = len(list(ssolv2.solutions()))

    return map(str, [i, j, formula.clauses(), cnf.formula.clauses(), len(formula.variables()), solns, ssiz, isiz, ctm, sftm, smtm, imtm])
    

def benchmark():
    print "depth, iteration, clauses, CNF clauses, variables, solutions, size of 1st SAT solution, size of 1st ILP solution, CNF time, SAT 1st, SAT minimal, ILP minimal"

    fg = pbool.FormulaGenerator(vocab, seed)
    for i in range(5, 15):
        for j in range(0, 50):
            yield do_experiment(fg, i, j)

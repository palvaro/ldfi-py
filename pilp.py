import pbool
from pulp import *


class SATVars:
    def __init__(self):
        self.name2var = {}
        self.var2name = {}

    def lookupName(self, name):
        if not self.name2var.has_key(name):
            lpv = LpVariable(name, 0, 1, "Integer")
            #print "LPV " + str(lpv)
            self.name2var[name] = lpv
            self.var2name[lpv] = name
            
        return self.name2var[name]

    def lookupVar(self, var):
        return self.var2name[var]
    
    def allVars(self):
        for key in self.var2name:
            yield key

class Solver:
    def __init__(self, cnf):
        #cnf = pbool.CNFFormula(formula)
        self.problem = LpProblem("LDFI", LpMinimize)

        self.vars = SATVars()
        self.satformula = []
        for clause in cnf.conjuncts():
            satclause = map(self.vars.lookupName, clause)
            #print "SATCLAUSE " + str(satclause)
            self.satformula.append(list(satclause))
            self.problem += sum(satclause) >= 1

        
        
        self.problem += sum(self.vars.allVars())

        

    def solutions(self):
        def unVar(var):
            if value(var) == 1.0:
                return var
            else:
                return 1 - var

        while True: 
            status = self.problem.solve()
            #print "STATUS " + str(LpStatus[status])
            if status != 1:
                return
            ret = filter(lambda x: value(x) == 1.0, self.vars.allVars())
            newsum = sum(map(unVar, self.vars.allVars()))
            yield ret
            self.problem += (newsum <= len(list(self.vars.allVars())) - 1)


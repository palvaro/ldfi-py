import abc
import random
from graphviz import Digraph

class BooleanFormula:
    def __init__(self, left=None, right=None, val=None):
        self.val = val
        self.left = left
        self.right = right
        self.sign = "UNIMPLEMENTED"

    #def __eq__(self, other):
    def __cmp__(self, other):
        # this method sucks my ass
        if other is None:
            return 1
        elif self.val is not None:
            return cmp(self.val, other.val)
        else:
            if self.sign == other.sign:
                if self.left == other.left and self.right == other.right:
                    return 0
                else:
                    return 1
            else:
                return 1


    @abc.abstractmethod
    def me(self):
        return "UNIMPLEMENTED"

    @abc.abstractmethod
    def convertToCNF(self):
        return

    @abc.abstractmethod
    def isCNF(self):
        return

    def graph(self, file):
        dot = Digraph(comment="LDFI", format='png')
        edges = self.edgeset()

        dot.edges(edges)
        dot.render(file)
        

    def variables(self):
        if self.val is not None:
            return set([self.val])
        else:
            return self.left.variables().union(self.right.variables())

    def clauses(self):
        if self.val is not None:
            return 1 
        else:
            return 1 + self.left.clauses() + self.right.clauses()

    def depth(self):
        if self.val is not None:
            return 1
        else:
            lft = self.left.depth()
            rgh = self.right.depth()
            if lft > rgh:
                return 1 + lft
            else:
                return 1 + rgh

    def nodeset(self):
        if self.val is not None:
            return set((self.ident(), self.val))
        else:
            sub = self.left.nodeset().union(self.right.nodeset())
            return sub.add((self.ident(), self.sign))

    def edgeset(self):
        if self.val is not None:
            return set()
        else:
            sub = self.left.edgeset().union(self.right.edgeset())
            sub.add((self.ident(), self.left.ident()))
            sub.add((self.ident(), self.right.ident()))
            return sub

    def ident(self):
        return str(self)

    def __str__(self):
        if self.val is not None:
            return self.val
        else:
            return "(" + str(self.left) + " " + self.sign + " " + str(self.right) + ")"

    @abc.abstractmethod
    def conjuncts(self):
        print "ONO"
        raise Exception("you fucked up.")
        return set()
            


class AndFormula(BooleanFormula):
    def __init__(self, left, right):
        BooleanFormula.__init__(self, left, right)
        self.sign = "AND"

    def convertToCNF(self):
        return AndFormula(self.left.convertToCNF(), self.right.convertToCNF())  

    def isCNF(self):
        return self.left.isCNF() and self.right.isCNF()

    def disjuncts(self):
        # P.A.A. ????
        print "FOOGAR"
        return set()

    def conjuncts(self):
        # an AND node should return a set of sets of disjuncts
        ret = set()
        if self.left.sign == "OR":
            ret.add(frozenset(self.left.disjuncts()))
        else:
            ret = ret.union(self.left.conjuncts())

        if self.right.sign == "OR":
            ret.add(frozenset(self.right.disjuncts()))
        else:
            ret = ret.union(self.right.conjuncts())

        return ret
           
        

class OrFormula(BooleanFormula):
    def __init__(self, left, right):
        BooleanFormula.__init__(self, left, right)
        self.sign = "OR"

    def convertToCNF(self):
        if self.right.sign == "AND":
            lft = self.left.convertToCNF()
            return AndFormula(OrFormula(lft, self.right.left.convertToCNF()), OrFormula(lft, self.right.right.convertToCNF()))
        elif self.left.sign == "AND":
            rgh = self.right.convertToCNF()
            return AndFormula(OrFormula(self.left.left.convertToCNF(), rgh), OrFormula(self.left.right.convertToCNF(), rgh))
        else:
            return OrFormula(self.left.convertToCNF(), self.right.convertToCNF())

    def isCNF(self):
        if (self.left.sign == "AND") or (self.right.sign == "AND"):
            print "ONO: witness to non-cnf: " + self.left.sign + " and " + self.right.sign
            return False
        else:
            return self.left.isCNF() and self.right.isCNF()
    
    def disjuncts(self):
        if not self.isCNF():
            raise Exception("Formula not CNF")
        else:
            return self.left.disjuncts().union(self.right.disjuncts())

    def conjuncts(self):
        # vacuous case!
        return frozenset([frozenset(self.left.disjuncts().union(self.right.disjuncts()))])

class Literal(BooleanFormula):
    def __init__(self, val):
        BooleanFormula.__init__(self, None, None, val)

    def convertToCNF(self):
        return self

    def isCNF(self):
        return True

    def disjuncts(self):
        return set([self.val])

    def conjuncts(self):
        return set([frozenset([self.val])])

class FormulaGenerator:
    def __init__(self, cardinality, seed):
        random.seed(seed)
        self.cardinality = cardinality

    def formula(self, depth):
        if depth == 1:
            # pick a random string
            stri = "I" + str(random.randint(0, self.cardinality))
            return Literal(stri)
        else:
            long = self.formula(depth-1)
            short = self.formula(random.randint(1, depth-1))
            if random.randint(0,1) == 1:
                left = long
                right = short
            else:
                right = long
                left = short
    
            # either an AND or an OR
            if random.randint(0,1) == 1:
                # AND
                return AndFormula(left, right)
            else:
                return OrFormula(left, right)


class CNFFormula:
    def __init__(self, formula):
        self.formula = None
        form = formula
        i = 0
        while form != self.formula:
            #print str(form) + " IS NOT = " + str(self.formula)
            self.formula = form
            form = form.convertToCNF()
            #print "iteration %d" % i
            i += 1

        self.formula = form.convertToCNF()

    
    def conjuncts(self):
        return self.formula.conjuncts()            

    def __str__(self):
        return self.formula.__str__()


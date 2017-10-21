import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from pprint import pprint


class TrivialSemantics(object):
    def mergeit(self, merge):
        if merge is None:
            return ''
        else:
            return merge

    def stringup(self, var, basetype, delimiter):
        print "VAR IS " + str(var)
        if type(var) == basetype:
            return var
        else:
            return delimiter.join(var)

    def include(self, ast):
        return "include \"" + ast.file + "\"" + ";"
        

    def start(self, ast):
        if ast.includes != []:
            incs = self.stringup(ast.includes, unicode, "\n") + "\n"
        else:
            incs = ""
        #return self.stringup(ast.includes, unicode, "\n") + "\n" + self.stringup(ast.rules, unicode, "\n")
        return incs + self.stringup(ast.rules, unicode, "\n")

    def fact(self, ast):
        return ast.pred + "@" + ast.time + ";"

    def var(self, ast):
        return str(ast)

    def expr(self, ast):
        if 'op' in ast:
            return " ".join([ast.lexp, ast.op, ast.rexp])
        return str(ast)

    def predicate(self, ast):
        if type(ast.args) == str:
            args = ast.args
        else:
            args = ", ".join(ast.args)
    
        return ast.table +  '(' + args + ')'

    def notin(self,ast):
        print "I hit a notin " + str(ast)
        return "notin " + ast.pred 

    def assignment(self, ast):
        return ast.var + ' = ' + ast.expr

    def qual(self, ast):
        return ast.left + " " + ast.qop + " " + ast.right

    def rule(self, ast):
        print "AST is " + str(ast)
        lhs = ast.lhs + (ast.merge or "")
        if type(ast.rhs) == unicode:
            rhs = ast.rhs
        else:
            rhs = ", ".join(ast.rhs)

        return lhs + " :- " + rhs + ";"


class DedalusSemantics(TrivialSemantics):

    def predicate(self, ast):
        if type(ast.args) == str:
            args = ast.args
        else:
            args = ", ".join(ast.args)
    
        return ast.table +  '(' + args + ', Time)'

    def rule(self, ast):
        print "AST is " + str(ast)

        lhs = ast.lhs + (ast.merge or "")
        if type(ast.rhs) == unicode:
            rhs = ast.rhs
        else:
            print "JOIN ME " + str(ast.rhs)
            rhs = ", ".join(ast.rhs)

        return lhs + " :- " + rhs + ";"


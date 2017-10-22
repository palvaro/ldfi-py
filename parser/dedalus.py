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

    def Nlhs(self, ast):
        print "IN LHS " + str(ast)
        if type(ast.args) == str:
            args = ast.args
        else:
            args = ", ".join(ast.args)
    
        return ast.table +  '(' + args + ', NewTime)'

    def Nrhspredicate(self, ast):
        if type(ast.args) == str:
            args = ast.args
        else:
            args = ", ".join(ast.args)
    
        return ast.table +  '(' + args + ', Time)'


    def predicate(self, ast):
        return ast;
        #pass;
    

    def check_rhs(self, ast):
        # check a couple of well-formedness conditions for dedalus rules.
        print "TYPE of rhs is "  + str(type(ast))
        running = None
        for subg in ast:
            print "SUBG is " + str(subg)
            if running is None:
                running = subg.first
            if subg.first != running:
                raise Exception("Local knowledge - " + subg.first + " vs " + running)

        


    def rule(self, ast):
        print "AST is " + str(ast)
        self.check_rhs(ast.rhs)
        print "OK "  + str(ast.rhs[0])
        node_id = ast.rhs[0].args[0]

        print "NODE id " + node_id

        lhs = ast.lhs + (ast.merge or "")
        # 'type' check
        running = None
        for subg in ast.rhs:
            if running is None:
                running = subg.first
            if subg.first != running:
                raise Exception("Local knowledge - " + subg.first + " vs " + running)

        

        if type(ast.rhs) == unicode:
            rhs = ast.rhs
            node = ast.rhs.first
        else:
            print "JOIN ME " + str(ast.rhs)
            rhs = ", ".join(ast.rhs)

        

        return lhs + " :- " + rhs + ";"


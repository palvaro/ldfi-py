import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from pprint import pprint
import os


class TrivialSemantics(object):
    # recognize a dedalus program, and transform it into the same program yay
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
    # Translate a dedalus program into a c4lang program, yay

    def predicate(self, ast):
        return ast;

    def include(self, ast):
        return ""
        # the 'semantics' of the include statement are to parse, then hoist the program referred to into this program.
        print "CWD " + str(os.getcwd())
        grammar = open('dedalus.tatsu').read()
        prog = open(ast.file).read()
        parser = tatsu.compile(grammar)
        ast = parser.parse(prog.read(), trace=False, colorize=True, semantics=DedalusSemantics())
        return ast
        
        

    def check_rhs(self, ast):
        # check a couple of well-formedness conditions for dedalus rules.
        running = None
        for subg in ast:
            # if the subgoal is a notin, we have already parsed it and don't need to check it now
            # GET RID OF ME!!!
            if type(subg) != unicode:
                if running is None:
                    running = subg.first
                if subg.first != running:
                    raise Exception("Local knowledge - " + subg.first + " vs " + running)

    def tableify(self, ast, timevar):
        print "TABLEIFY " + str(ast)

        # grrr, this is annoying
        if u'pred' in ast:
            return ((ast.notin + " ") or "") + ast.pred.table + '(' + ", ".join(ast.pred.args + [timevar]) + ')'
        else:
            return ast.table + '(' + ", ".join(ast.args + [timevar]) + ')'

    def notin(self,ast):
        return ast

    def fact(self, ast):
        print "FACT " +  str(ast)
        #return ast.pred + "@" + ast.time + ";"
        return self.tableify(ast.pred, ast.time)

    def rule(self, ast):
        self.check_rhs(ast.rhs)
        node_id = ast.rhs[0].args[0]

        lhs = self.tableify(ast.lhs, "NewTime")
        rhs = ", ".join(map(lambda x : self.tableify(x, "Time"), ast.rhs))
        if ast.merge == "@next":
            clock = ', localclock(' + node_id  + ", Time, NewTime)"
        elif ast.merge == "@async":
            other_id = ast.lhs.args[0]
            clock = ', clock(' + ", ".join([node_id, other_id])  + ", Time, NewTime)"
        else:
            clock = ''
        
        return lhs + " :- " + rhs + clock + ";"


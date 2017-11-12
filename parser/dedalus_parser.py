import tatsu
from tatsu.ast import AST
from tatsu.walkers import NodeWalker
from tatsu.model import ModelBuilderSemantics
from pprint import pprint
from graphviz import Digraph
import os
import re
import sys

from dedalus import TrivialSemantics

class Subgoal(object):
    def __init__(self):
        raise Exception("Nope")

class GoalNode(Subgoal):
    def __init__(self, predicate, valence):
        self.predicate = predicate
        self.rules = []
        self.valence = valence

    def add_rule(self, rule):
        self.rules.append(rule)

    def __str__(self):
        return "Goal(" + self.predicate + ")"


class Bindings(Subgoal):
    # associates a list of named variables with a predicate of the same arity
    def __init__(self, predicate, bindings):
        self.predicate = predicate
        self.bindings = bindings

class Qual(Subgoal):
    def __init__(self, expr):
        self.expr = expr


class RuleNode(object):
    def __init__(self, head, merge):
        self.goals = []
        self.head = head
        self.merge = merge

    def add_goal(self, goal):
        self.goals.append(goal)

    def reset_goals(self, goals):
        self.goals = goals

class RuleGoalGraph(object):
    def __init__(self):
        self.goals = {}
        self.rules = []

    def get_goal(self, goal):
        if goal.predicate in self.goals:
            return self.goals[goal.predicate]
        else:
            self.goals[goal.predicate] = goal
            return goal

        
    def add_rule(self, rule):
        hg = self.get_goal(rule.head)
        new_goals = []
        for goal in rule.goals:
            # change later
            if isinstance(goal, GoalNode):
                new_goals.append(self.get_goal(goal))
            
        rule.reset_goals(new_goals)
        self.rules.append(rule)

    def to_dot(self):
        graph = Digraph(comment="RGG")
        graph.node("S", shape="diamond")
        graph.node("T", shape="diamond")
        for goal in self.goals:
            graph.node(goal)

        for rule in self.rules:
            rulestr = str(rule)
            if rule.merge == "@next":
                lbl = "+"
            elif rule.merge == "@async":
                lbl = "~"
            else:
                lbl = "="
            graph.node(rulestr, shape="rectangle", label = lbl)
            graph.edge(rule.head.predicate, rulestr)
            rule.head.add_rule(rule)
            for subg in rule.goals:
                graph.edge(rulestr, subg.predicate)

        for goal in self.goals:
            if len(self.goals[goal].rules) == 0:
                graph.edge(goal, "S")

        goalset = set(map(lambda x: self.goals[x], self.goals))
        usedset = set()
        for rule in self.rules:
            if not rule.merge == "@next":
                usedset = usedset.union(set(rule.goals))

        unref = goalset.difference(usedset)
        for u in unref:
            graph.edge("T", u.predicate)
        
            
        return graph
        

class NegNodeWalker(NodeWalker):

    def walk_program(self,node):
        rgg = RuleGoalGraph()
        # Walk the includes
        #print self.walk(node.includes)
        # Walk the rules
        print self.walk(node.rules)
    
        for rule in self.walk(node.rules):
            if rule != "":
                rgg.add_rule(rule)

        return rgg
            

    def walk_stmlist(self,node):
        ret = []
        # Walk each statment in the statement list.
        for stmt in node.stmts:
            ret.append(self.walk(stmt[0]))
        return ret

    def walk_includelist(self, node):
        ret = ""
        for include in node.includelist:
            ret += self.walk(include) + ";\n"
        return ret

    def walk_statement(self, node):
        return self.walk(node.stmt)

    def walk_rule(self, node):
        lhs = self.walk(node.lhs)
        rhs = self.walk(node.rhs)
        if "merge" in dir(node):
            merge = self.walk(node.merge)
        else:
            merge = None

        rule = RuleNode(lhs, merge)
        for s in rhs:
            rule.add_goal(s)

        return rule


    def walk_rhs(self, node):
        return self.walk(node.rhs)

    def walk_lhs(self, node):
        return self.walk(node.predicate)

    def walk_subgoallist(self, node):
        if isinstance(node.subgoals, list):
            ret = []
            for subgoal in node.subgoals:
                ret.append(self.walk(subgoal))
            return ret
        else:
            return [ self.walk(node.subgoals) ]

    def walk_subgoal(self, node):
        return self.walk(node.subgoal)

    def walk_catalog_entry(self, node):
        return node.entry

    def walk_rhspredicate(self, node):
        return self.walk(node.pred)

    def walk_predicate(self, node):
        return GoalNode(self.walk(node.table), True)

    def walk_exprlist(self, node):
        if isinstance(node.exprs, list):
            ret = ""
            for expr in node.exprs:
                ret += self.walk(expr) + ", "
            return ret[:len(ret)-2]
        else:
            return self.walk(node.exprs)

    def walk_expr(self, node):
        return self.walk(node.expr)

    def walk_var(self, node):
        return node.val

    def walk_notin(self, node):
        #return 'notin ' + self.walk(node.pred)
        #return Goal(self.walk(node.pred), False)
        pred = self.walk(node.pred)
        pred.valence = False
        return pred
        

    def walk_merge(self, node):
        return node.merge

    # Here to check if a node being used hasn't been defined yet.
    def walk_Node(self, node):
        print "node undefined"
        #print node
        return ""

class DedalusParser(object):
    def __init__(self):
        self.grammar = open('dedalus_asmodel.tatsu').read()
        self.parser = tatsu.compile(self.grammar, asmodel = True)
        

    def parse(self, program):
        model = self.parser.parse(program)
        walker = NegNodeWalker()
        walked = walker.walk(model)
        return walked


    def expand_file(self, file):
        # do macro expansion.
        program = ""
        p = re.compile('include \"(\S+)\";')

        relpath = os.path.dirname(file)
        with open(file, 'r') as prog: 
            for line in prog:
                m = p.match(line)
                if m:
                    program += self.expand_file(relpath + "/" + m.group(1))
                else:
                    program += line
   
    
        #return self.parse(program)
        return program
    

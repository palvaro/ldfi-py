import sys
from tatsu.codegen import ModelRenderer
from tatsu.codegen import CodeGenerator

THIS_MODULE =  sys.modules[__name__]

class C4CodeGenerator(CodeGenerator):
    def __init__(self):
        print "YO"
        super(C4CodeGenerator, self).__init__(modules=[THIS_MODULE])

class rule(ModelRenderer):
        print "RULE"
        template = '''\
        {lhs} :- {rhs}'''

class plainlhs(ModelRenderer):
    template = '''\
    {predicate.table}({predicate.args}, Time'''


class inductivelhs(ModelRenderer):
    template = '''\
    {predicate.table}({predicate.args}, Time + 1)'''


class asynclhs(ModelRenderer):
    template = '''\
    {predicate.table}({predicate.args}, NewTime)'''


class merge(ModelRenderer):
    template = "{merge}"

class subgoallist(ModelRenderer):
    template = "{subgoals::, :}"

class subgoal(ModelRenderer):
    template = "{subgoal}"

class rhs(ModelRenderer):
    template = '''\
    {rhs}, clock('''

class rhspredicate(ModelRenderer):
    template = "{pred.table}({pred.args}, Time)"

class notin(ModelRenderer):
    template = "notin {pred}"

class predicate(ModelRenderer):
    template = '''\
    {table}({args:::})'''

class table(ModelRenderer):
    template = "{table}"

class catalog_entry(ModelRenderer):
    template = "{entry}"

class exprlist(ModelRenderer):
    template = "{exprs::, :}"

class expr(ModelRenderer):
    template = "{expr}"

class var(ModelRenderer):
    template = "{val}"


class program(ModelRenderer):
        print "PRTO"
        template = '''\
        {rules}'''


class statement(ModelRenderer):
    template = '''\
    {stmt:::}'''    
    

class stmlist(ModelRenderer):
        template = '''\
        {stm::;\n:}'''




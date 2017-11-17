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

class program(ModelRenderer):
        print "PRTO"
        template = '''\
        {rules}'''

class stmt(ModelRenderer):
    template = "safd"

class statement(ModelRenderer):
    template = "ya motha"

class stmlist(ModelRenderer):
        print "UH"
        #print "UM " + str(stmts)
        template = '''\
        S:{stmts}'''




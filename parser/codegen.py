import sys
from tatsu.codegen import ModelRenderer
from tatsu.codegen import CodeGenerator

THIS_MODULE =  sys.modules[__name__]

class C4CodeGenerator(CodeGenerator):
    def __init__(self):
        super(C4CodeGenerator, self).__init__(modules=[THIS_MODULE])

    #def rule(ModelRenderer):
    #    template = '''\
    #    {lhs} :- {rhs}'''

    def program(ModelRenderer):
        template = '''\
        FOO'''





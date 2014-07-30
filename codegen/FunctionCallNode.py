from codegen.Node import *
from codegen.Token import *


class FunctionCallNode(Node):
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_FUNCTION)
        
        self.header = tokens.pop(0)
        
        assert(self.header.type == TOKEN_FUNCTION_CALL)
        
    def execute(self, locals):
        self.context.getFunction(self.header.name).call(self.header.params, locals)
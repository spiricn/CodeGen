from Node import *
from Token import *


class FunctionCallNode(Node):
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_FUNCTION)
        
        self.header = tokens.pop(0)
        
        assert(self.header.type == TOKEN_FUNCTION_CALL)
        
    def execute(self):
        self.context.getFunction(self.header.name).call(self.header.params)
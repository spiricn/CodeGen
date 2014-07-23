from Node import *
from Token import *

class FunctionDefNode(Node):
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_FUNCTION)
        
        self.header = tokens.pop(0)
        
        assert(self.header.type == TOKEN_FUNCTION_BEGIN)
        
        self.body = self.context.createContainer()
        
        currToken = None
        
        while True:
            currToken = tokens[0]
            
            if currToken.type == TOKEN_FUNCTION_END:
                tokens.pop(0)
                break
            else:
                self.body.addChild(tokens)
        
        self.context.addFunction(self.header.name, self)
        
    def call(self, args, locals):
        l = {}
        # Expose arguments
        for c, arg in enumerate(args):
            l[ self.header.params[c] ] = eval(arg, self.context.workspace, locals)
            
        # Execute body
        self.body.execute(l)            
        
    def execute(self, locals):
        pass
        
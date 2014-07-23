from Node import *
from Token import *

class WhileLoopNode(Node):
    '''
    Node representing a while loop
    '''
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_WHILE_LOOP)
        
        self.startToken = tokens.pop(0)
        
        # Sanity check 
        assert(self.startToken.type == TOKEN_WHILE_LOOP_START)
        
        self.body = self.context.createContainer()
        
        while True:
            token = tokens[0]
            
            if token.type == TOKEN_WHILE_LOOP_END:
                tokens.pop(0)
                break
            else:
                self.body.addChild( tokens )
        
    def execute(self, locals):
        while eval(self.startToken.condition, self.context.workspace, locals):
            self.body.execute(locals)
        
    def __str__(self):
        return '<TextNode>'
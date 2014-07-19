from Node import *
from Token import *

class TextNode(Node):
    '''
    Node representing a single chunk of text
    '''
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_TEXT)
       
        # We're only using the first token
        self.token = tokens.pop(0)
        
        # Sanity check
        assert(self.token.type == TOKEN_TEXT) 
        
    def execute(self):
        self.context.result += self.token.body
        
    def __str__(self):
        return '<TextNode>'
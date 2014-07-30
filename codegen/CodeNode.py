from codegen.Node import *
from codegen.Token import *
import sys
import traceback

class CodeNode(Node):
    '''
    Node presenting a code expression to be executed.
    '''
    
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_CODE)
        
        start = tokens[0]
        
        # Sanity check
        assert( start.type == TOKEN_CODE_START )
        
        if start.inlineCode:
            self.inline = True
            
            tokens.pop(0)
            self.code = start.inlineCode
        else:
            self.inline = False
            self.code, end = tokens[1:3]
            
            # TODO an error message        
            assert(self.code.type == TOKEN_TEXT and end.type == TOKEN_CODE_END)
            
            tokens.pop(0)
            tokens.pop(0)
            tokens.pop(0)
        
    def execute(self, locals):
        try:
            code = self.code.body if not self.inline else self.code
            
            exec(code, self.context.workspace)
        except Exception as e:
            print('Error executing expression; reason %s' % (e))
            traceback.print_exc(file=sys.stdout)
            raise
        
    def __str__(self):
        return '<CodeNode>'
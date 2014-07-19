from Node import *
from Token import *

class CodeNode(Node):
    '''
    Node presenting a code expression to be executed.
    '''
    
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_CODE)
        
        start, self.code, end = tokens[:3]

        # TODO an error message        
        assert(start.type == TOKEN_CODE_START and self.code.type == TOKEN_TEXT and end.type == TOKEN_CODE_END)
        
        tokens.pop(0)
        tokens.pop(0)
        tokens.pop(0)
        
    def execute(self):
        try:
            exec(self.code.body, self.context.workspace)
        except Exception as e:
            print('Error executing expression "%s"; reason %s' % (self.code.body, e))
            traceback.print_exc(file=sys.stdout)
            raise
        
    def __str__(self):
        return '<CodeNode>'
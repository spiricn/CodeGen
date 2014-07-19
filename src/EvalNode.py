from Node import *
from Token import *

class EvalNode(Node):
    '''
    Node representing an evaluation expression.
    '''
    def __init__(self, context, tokens):
        Node.__init__(self, context, NODE_EVAL)
        
        # We only need the first token
        self.token = tokens.pop(0)
        
        # Sanity check
        assert(self.token.type == TOKEN_EVAL)
        
    def execute(self):
        try:
            # Try to evaluate the expression
            self.context.result += str( eval(self.token.expression, self.context.workspace) )
        except Exception as e:
            # Expression could not be evalulated
            print('Error evaluating expression "%s"; reason: %s' % (self.token.expression, e))
            traceback.print_exc(file=sys.stdout)
            raise
        
    def __str__(self):
        return '<EvalNode>'
                